package org.example;

import java.util.function.Function;

public class InterpolationService {

    public double[] generateEquidistantNodes(double a, double b, int n) {
        if (n < 2) {
            throw new IllegalArgumentException("Liczba węzłów musi być >= 2");
        }
        double[] nodes = new double[n];
        double h = (b - a) / (n - 1); // Krok
        for (int i = 0; i < n; i++) {
            nodes[i] = a + i * h;
        }
        if (n > 1) {
            nodes[n - 1] = b;
        }
        return nodes;
    }

    public double[] calculateNodeValues(Function<Double, Double> f, double[] xNodes) {
        double[] yNodes = new double[xNodes.length];
        for (int i = 0; i < xNodes.length; i++) {
            yNodes[i] = f.apply(xNodes[i]);
        }
        return yNodes;
    }

    public double lagrangeInterpolation(double[] xNodes, double[] yNodes, double x) {
        double interpolatedValue = 0.0;
        int n = xNodes.length;

        for (int i = 0; i < n; i++) {
            double basisPolynomial = 1.0; // L_i(x)
            for (int j = 0; j < n; j++) {
                if (i != j) {
                    if (Math.abs(xNodes[i] - xNodes[j]) < 1e-15) {
                        System.err.println("Ostrzeżenie: Węzły " + i + " i " + j + " są bardzo blisko.");
                        continue;
                    }
                    basisPolynomial *= (x - xNodes[j]) / (xNodes[i] - xNodes[j]);
                }
            }
            interpolatedValue += yNodes[i] * basisPolynomial;
        }
        return interpolatedValue;
    }
}
