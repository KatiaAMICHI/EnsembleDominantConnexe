package algorithms;

import java.awt.Point;
import java.util.ArrayList;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class DefaultTeam {
	public ArrayList<Point> calculConnectedDominatingSet(ArrayList<Point> points, int edgeThreshold) {
		// REMOVE >>>>>
		ArrayList<Point> result = (ArrayList<Point>) points.clone();
		
		result = readFromFile("output0.points");
		// else saveToFile("output",result);
		// <<<<< REMOVE
		// System.out.println(IsValid(points, result, edgeThreshold));
		
		
		
				Point p = points.get(0);
		// Point q = points.get(42);
		System.out.println("edgeThreshold : " + edgeThreshold);
		
		System.out.println(neighbor(p, points, edgeThreshold).size() );

		
		
		return result;
	}

	private boolean IsValid(ArrayList<Point> vertices, ArrayList<Point> DS, int edgeThreshold) {
		for (Point p : vertices)
			System.out.println("p : " + p + " | nbV : " + neighbor(p, vertices, edgeThreshold).size());
		for (Point p : DS) {
			vertices.remove(p);
			// vertices.removeAll(neighbor(p, vertices, edgeThreshold));
		}
		Boolean isv = vertices.size() == 0;
		// System.out.println("vertices : " + vertices.size());

		return vertices.size() == 0;
	}

	public ArrayList<Point> neighbor(Point p, ArrayList<Point> vertices, int edgeThreshold) {
		ArrayList<Point> result = new ArrayList<Point>();
		for (Point point : vertices)
			if (point.distance(p) <= edgeThreshold && !point.equals(p))
				result.add(point);

		return result;
	}

	// FILE PRINTER
	private void saveToFile(String filename, ArrayList<Point> result) {
		int index = 0;
		try {
			while (true) {
				BufferedReader input = new BufferedReader(
						new InputStreamReader(new FileInputStream(filename + Integer.toString(index) + ".points")));
				try {
					input.close();
				} catch (IOException e) {
					System.err.println(
							"I/O exception: unable to close " + filename + Integer.toString(index) + ".points");
				}
				index++;
			}
		} catch (FileNotFoundException e) {
			printToFile(filename + Integer.toString(index) + ".points", result);
		}
	}

	private void printToFile(String filename, ArrayList<Point> points) {
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

	// FILE LOADER
	private ArrayList<Point> readFromFile(String filename) {
		String line;
		String[] coordinates;
		ArrayList<Point> points = new ArrayList<Point>();
		try {
			BufferedReader input = new BufferedReader(new InputStreamReader(new FileInputStream(filename)));
			try {
				while ((line = input.readLine()) != null) {
					coordinates = line.split("\\s+");
					points.add(new Point(Integer.parseInt(coordinates[0]), Integer.parseInt(coordinates[1])));
				}
			} catch (IOException e) {
				System.err.println("Exception: interrupted I/O.");
			} finally {
				try {
					input.close();
				} catch (IOException e) {
					System.err.println("I/O exception: unable to close " + filename);
				}
			}
		} catch (FileNotFoundException e) {
			System.err.println("Input file not found.");
		}
		return points;
	}
}
