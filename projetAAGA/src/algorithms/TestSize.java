package algorithms;

import java.awt.Point;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Random;
import java.util.Set;
import java.util.Stack;



public class TestSize {
	public ArrayList<Point> removePoints(ArrayList<Point> points, int edgeThreshold){
		//bfs over the graph
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
		 
		 //return max compo
		 int max_size = 0;
		 ArrayList<Point> maxCompo = null;
		 for(ArrayList<Point> c: compo.values()) {
			 if(c.size() > max_size) {
				 max_size = c.size();
				 maxCompo = c;
			 }
		 }
		 //System.out.println(compo);
		 return maxCompo;
	}
	
	public static void main(String[] args) {
		for(int nb=0; nb<100; nb++) {
			for(int e = 40; e < 140; ++e) {
				int numberOfPoints = (e+1)*10;
				System.out.println(numberOfPoints);
				ArrayList<Point> pts = GraphGenerator.generate(numberOfPoints);
				TestSize ts = new TestSize();
				pts = ts.removePoints(pts, GraphGenerator.edgeThreshold);
				String filename = "testlength/input" + pts.size() + ".points";
				DefaultTeam.printToFile(filename, pts);
				System.out.println("wrote file " + filename);
			}
			System.out.println("......................FIN..................");
		}
	}
}
