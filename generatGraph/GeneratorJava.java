package algorithms;

import java.awt.Point;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map.Entry;
import java.util.Random;
import java.util.Set;
import java.util.Stack;



public class GeneratorJava {
	private static int maxWidth = 1600;
	private static int maxHeight =1000;
	private static int radius = 150;
	static byte edgeThreshold = 55;
	
	public static void main(String[] args) {
		/**
		 * création de 1000 fichier de tests de taille entre [400, 1400] dans le répertoire JavaDB
		 */
		for(int nb=0; nb<100; nb++) {
			for(int e = 40; e < 140; ++e) {
				int numberOfPoints = (e+1)*10;
				System.out.println(numberOfPoints);
				ArrayList<Point> pts = generate(numberOfPoints);
				GeneratorJava ts = new GeneratorJava();
				pts = ts.removePoints(pts, edgeThreshold);
				String filename = "JavaDB/input" + pts.size() + ".points";
				printToFile(filename, pts);
				System.out.println("wrote file " + filename);
			}
			System.out.println("......................FIN..................");
		}
	}
	
	public static ArrayList<Point> generate(int nbPoints) {
		/**
		 * Génération des points aléatoire en utilisant le générateur pseudo-aléatoire de java
		 * 
		 * nbPoints : le nombre de points à générer
		 * return : retourne une liste de point générer aléatoirement   
		 */
		Random generator = new Random();
		ArrayList<Point> res = new ArrayList<Point>();
		for (int i = 0; i < nbPoints; ++i) {
			int x;
			int y;
			do {
				x = generator.nextInt(maxWidth);
				y = generator.nextInt(maxHeight);
			} while (distanceToCenter(x, y) >= (double) radius * 1.4D
					&& (distanceToCenter(x, y) >= (double) radius * 1.6D || 
						generator.nextInt(5) != 1)
					&& (distanceToCenter(x, y) >= (double) radius * 1.8D || 
						generator.nextInt(10) != 1)
					&& (x < maxHeight / 5 || 
							x >= 4 * maxHeight / 5 || 
							y < maxHeight / 5 || 
							y >= 4 * maxHeight / 5 || 
							generator.nextInt(100) != 1));
			res.add(new Point(x, y));
		}
		return res;
	}
	
	public ArrayList<Point> removePoints(ArrayList<Point> points, int edgeThreshold){
		/**
		 * retourne le plus grand sous-graph connecter
		 * 
		 */
		Graph g = new Graph(points, edgeThreshold);
		HashMap<Point, Boolean> marked = new HashMap<Point, Boolean>();
		Stack<Point> fifo = new Stack<Point>();
		HashMap<Integer, ArrayList<Point>> compo = new HashMap<>();

		int cpt = 0;
		fifo.add(points.get(0));
		marked.put(points.get(0), true);
		compo.put(cpt, new ArrayList<>());
		compo.get(cpt).add(points.get(0));
		
		for(Point p1: g.getAdjacency().keySet()) {
			marked.put(p1, false);
		}
		
		boolean flag = false;
		 do {
			 flag = false;
			while(!fifo.isEmpty()) {
				Point p = fifo.pop();
				Set<Point> voisins = g.getNeighbors(p);
				for(Point v: voisins) {
					if(!marked.get(v)) {
						compo.get(cpt).add(v);
						fifo.add(v);
						marked.put(v, true);
					}
				}
			}
			for(Entry<Point,Boolean> m:marked.entrySet()) {
				if(!m.getValue()) {
					fifo.add(m.getKey());
					marked.put(m.getKey(), true);
					compo.put(++cpt,new ArrayList<Point>());
					compo.get(cpt).add(m.getKey());
					flag = true;
				}
			}
		}while(flag);
		 int max_size = 0;
		 ArrayList<Point> maxCompo = null;
		 for(ArrayList<Point> c: compo.values()) {
			 if(c.size() > max_size) {
				 max_size = c.size();
				 maxCompo = c;
			 }
		 }
		 return maxCompo;
	}
	
	public static double distanceToCenter(int x, int y) {
		return Math.min(
				Math.min(
						Math.min(
								Math.sqrt(Math.pow((double) (x - maxWidth / 2), 2.0D)
										+ Math.pow((double) (y - maxHeight / 2), 2.0D)),
								Math.sqrt(Math.pow((double) x - 2.5D * (double) maxWidth / 6.0D, 2.0D)
										+ Math.pow((double) (y - 2 * maxHeight / 6), 2.0D))),
						Math.min(
								Math.sqrt(Math.pow((double) (x - 4 * maxWidth / 6), 2.0D)
										+ Math.pow((double) (y - 2 * maxHeight / 6), 2.0D)),
								Math.sqrt(Math.pow((double) (x - 2 * maxWidth / 6), 2.0D)
										+ Math.pow((double) (y - 4 * maxHeight / 6), 2.0D)))),
				Math.sqrt(Math.pow((double) (x - 4 * maxWidth / 6), 2.0D)
						+ Math.pow((double) (y - 4 * maxHeight / 6), 2.0D)));
	}
	
	
	
	class Graph{
		public HashMap<Point, HashSet<Point>> adjacency;

		public HashMap<Point, HashSet<Point>> getAdjacency(){
			return adjacency;
		}

		public Graph(ArrayList<Point> points, int edgeThreshold){
			this.adjacency = new HashMap<>();
			for (Point p : points)
				adjacency.put(p, new HashSet<>());
			int size = points.size();
			for (int i = 0; i < size; ++i){
				for (int j = i + 1; j < size; ++j){
					Point p1 = points.get(i);
					Point p2 = points.get(j);
					if(p1.distance(p2) <= edgeThreshold){
						adjacency.get(p1).add(p2);
						adjacency.get(p2).add(p1);
					}
				}
			}
		}

		public HashSet<Point> getNeighbors(Point p){
			return adjacency.get(p);
		}

		public int degree(Point p){
			return adjacency.get(p).size();
		}
	}
	
	
		public static void printToFile(String filename, ArrayList<Point> points) {
			try {
				PrintStream output = new PrintStream(new FileOutputStream(filename));
				int x, y;
				for (Point p : points)
					output.println(Integer.toString((int) p.getX()) + " " + Integer.toString((int) p.getY()));
				output.close();
			} catch (FileNotFoundException e) {
				System.err.println("I/O exception: unable to create " + filename);
			}
		}

}

