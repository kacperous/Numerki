package org.example;

import java.util.Scanner;
import java.util.function.Function;

public class MainApp {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Wybierz funkcję do interpolacji:");
        System.out.println("1: Liniowa (f(x) = 2x + 1)");
        System.out.println("2: Wartość bezwzględna (f(x) = |x|)");
        System.out.println("3: Wielomian (f(x) = x^3 - 2x^2 + 1)"); // Przykład
        System.out.println("4: Trygonometryczna (f(x) = sin(x))");
        System.out.print("Wybór: ");
        int funcChoice = scanner.nextInt();
        Function<Double, Double> selectedFunction = FunctionUtil.getFunction(funcChoice);
        String functionLabel = FunctionUtil.getFunctionLabel(funcChoice);


        System.out.print("Podaj początek przedziału interpolacji (a): ");
        double a = scanner.nextDouble();

        System.out.print("Podaj koniec przedziału interpolacji (b): ");
        double b = scanner.nextDouble();

        System.out.print("Podaj liczbę węzłów interpolacyjnych (n >= 2): ");
        int n = scanner.nextInt();
        if (n < 2) {
            System.out.println("Liczba węzłów musi być >= 2.");
            scanner.close();
            return;
        }

        scanner.close();

        InterpolationService interpolationService = new InterpolationService();
        double[] xNodes = interpolationService.generateEquidistantNodes(a, b, n);
        double[] yNodes = interpolationService.calculateNodeValues(selectedFunction, xNodes);

        System.out.println("\nWęzły interpolacji (x, y):");
        for (int i = 0; i < n; i++) {
            System.out.printf("(%.4f, %.4f)\n", xNodes[i], yNodes[i]);
        }

        Plotter plotter = new Plotter();
        plotter.plot(selectedFunction, functionLabel, xNodes, yNodes, a, b);

        System.out.println("\nWykres został wygenerowany (jeśli skonfigurowano bibliotekę graficzną).");
    }
}
