package algorithms;

import java.awt.Point;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Random;
import java.util.Set;
import java.util.Stack;

import algorithms.Graph;

import java.io.*;

public class GraphGenerator {
	private static String filename = "Kinput.points";
	private static int numberOfPoints = 1000;
	private static int nbFiles = 1400;

	private static int maxWidth = 1600;
	private static int maxHeight =1000;
	private static int radius = 150;
	static byte edgeThreshold = 55;

	public GraphGenerator() {
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

	public static void generate() {

		for (int i = 1200; i < nbFiles; i++) {
			try {
				// create file
				String path = "tests/test" + i + ".points";
				File file = new File(path);

				FileWriter fw = new FileWriter(file.getAbsoluteFile());
				BufferedWriter bw = new BufferedWriter(fw);

				// commencer la génération de point
				Random generator = new Random();
				ArrayList<Point> points = new ArrayList<>();
				while (points.size() != numberOfPoints) {
					int x;
					int y;
					int deg = 0;
					do {
						do {
							x = generator.nextInt(maxWidth);
							y = generator.nextInt(maxHeight);
						} while (distanceToCenter(x, y) >= (double) radius * 1.4D
								&& (distanceToCenter(x, y) >= (double) radius * 1.6D || 
									generator.nextInt(5) != 1)
								&& (distanceToCenter(x, y) >= (double) radius * 1.8D || generator.nextInt(10) != 1)
								&& (maxHeight / 9 >= x || x >= 4 * maxHeight / 5 || maxHeight / 9 >= y
										|| y >= 7 * maxHeight / 9 || generator.nextInt(100) != 1));

						Point p = new Point(x, y);
						deg = 0;
						Iterator<Point> var11 = points.iterator();

						for (Point q : points)
							if (p.distance(q) <= (double) edgeThreshold)
								++deg;
					} while (deg >= 5);
					if (connecte(new Point(x, y), points)) {
						points.add(new Point(x, y));
						// ecriture du point dans le fichier
						bw.write(Integer.toString(x) + " " + Integer.toString(y) + "\n");
					}
				}
				// Close connection
				System.out.println("j'ai fini d'écrire" + i);
				bw.close();
			} catch (Exception ee) {
				System.out.println(ee);
			}
		}
		System.out.println("...............FIN...............");
	}

	public static boolean connecte(Point point, ArrayList<Point> points) {
		if (points.isEmpty())
			return true;
		for (Point p : points) {
			if (point.distance(p) <= (double) edgeThreshold)
				return true;
		}
		return false;
	}

	public ArrayList<Point> removePoints(ArrayList<Point> points, int edgeThreshold) {
		// bfs over the graph
		Graph g = new Graph(points, edgeThreshold);
		HashMap<Point, Boolean> marked = new HashMap<Point, Boolean>();
		Stack<Point> fifo = new Stack<Point>();
		HashMap<Integer, ArrayList<Point>> compo = new HashMap<>();

		int cpt = 0;
		fifo.add(points.get(0));
		marked.put(points.get(0), true);
		compo.put(cpt, new ArrayList<>());
		compo.get(cpt).add(points.get(0));

		for (Point p1 : g.getAdjacency().keySet()) {
			marked.put(p1, false);
		}

		boolean flag = false;
		do {
			flag = false;

			while (!fifo.isEmpty()) {
				Point p = fifo.pop();
				Set<Point> voisins = g.getNeighbors(p);
				for (Point v : voisins) {
					if (!marked.get(v)) {
						compo.get(cpt).add(v);
						fifo.add(v);
						marked.put(v, true);
					}
				}
			}
			for (Entry<Point, Boolean> m : marked.entrySet()) {
				if (!m.getValue()) {
					fifo.add(m.getKey());
					marked.put(m.getKey(), true);
					compo.put(++cpt, new ArrayList<Point>());
					compo.get(cpt).add(m.getKey());
					flag = true;

				}
			}
		} while (flag);

		// return max compo
		int max_size = 0;
		ArrayList<Point> maxCompo = null;
		for (ArrayList<Point> c : compo.values()) {
			if (c.size() > max_size) {
				max_size = c.size();
				maxCompo = c;
			}
		}
		// System.out.println(compo);
		return maxCompo;
	}

	public static ArrayList<Point> generate(int nbPoints) {
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

	public static void main(String[] args) {
		for (int e = 50; e < 120; ++e) {
			int numberOfPoints = (e + 1) * 10;
			System.out.println(numberOfPoints);
			ArrayList<Point> pts = GraphGenerator.generate(numberOfPoints);
			TestSize ts = new TestSize();
			pts = ts.removePoints(pts, GraphGenerator.edgeThreshold);
			String filename = "testlength/input" + pts.size() + ".points";
			DefaultTeam.printToFile(filename, pts);
			System.out.println("wrote file " + filename);
		}
	}

}