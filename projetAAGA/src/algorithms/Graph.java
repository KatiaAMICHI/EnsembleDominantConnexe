package algorithms;

import java.awt.Point;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

public class Graph
{
	public HashMap<Point, HashSet<Point>> adjacency;

	public HashMap<Point, HashSet<Point>> getAdjacency(){
		return adjacency;
	}


	public Graph(ArrayList<Point> points, int edgeThreshold)
	{

		this.adjacency = new HashMap<>();


		for (Point p : points)
			adjacency.put(p, new HashSet<>());

		int size = points.size();
		for (int i = 0; i < size; ++i)
		{
			for (int j = i + 1; j < size; ++j)
			{
				Point p1 = points.get(i);
				Point p2 = points.get(j);
				if(p1.distance(p2) <= edgeThreshold)
				{
					adjacency.get(p1).add(p2);
					adjacency.get(p2).add(p1);
				}
			}
		}
	}

	public HashSet<Point> getNeighbors(Point p)
	{
		return adjacency.get(p);
	}



	public int degree(Point p)
	{
		return adjacency.get(p).size();
	}


}
