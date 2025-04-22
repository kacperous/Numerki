package org.example;

import java.util.function.Function;

public class FunctionUtil {

    public static double evaluatePolynomialHorner(double[] coeffs, double x) {
        double result = coeffs[0];
        for (int i = 1; i < coeffs.length; i++) {
            result = result * x + coeffs[i];
        }
        return result;
    }

    public static Function<Double, Double> getFunction(int choice) {
        switch (choice) {
            case 1: // Liniowa: 2x + 1
                return x -> 2 * x + 1;
            case 2: // Wartość bezwzględna: |x|
                return Math::abs;
            case 3: // Wielomian: x^3 - 2x^2 + 0x + 1 (coeffs = [1, -2, 0, 1])
                double[] polyCoeffs = {1, -2, 0, 1};
                // Użycie Hornera do *obliczania wartości* tej funkcji
                return x -> evaluatePolynomialHorner(polyCoeffs, x);
            case 4: // Trygonometryczna: sin(x)
                return Math::sin;
            // Można dodać złożenia, np. case 5: return x -> Math.sin(x*x);
            default:
                System.out.println("Nieznany wybór, używam f(x) = x");
                return x -> x;
        }
    }

    public static String getFunctionLabel(int choice) {
        switch (choice) {
            case 1: return "f(x) = 2x + 1";
            case 2: return "f(x) = |x|";
            case 3: return "f(x) = x^3 - 2x^2 + 1";
            case 4: return "f(x) = sin(x)";
            default: return "f(x) = x";
        }
    }
}
