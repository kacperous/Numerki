package org.example;

import org.knowm.xchart.style.markers.SeriesMarkers;
import org.knowm.xchart.XYChart;
import org.knowm.xchart.XYChartBuilder;
import org.knowm.xchart.XYSeries;
import org.knowm.xchart.SwingWrapper;


import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

public class Plotter {

    public void plot(Function<Double, Double> originalFunc, String functionLabel,
                     double[] xNodes, double[] yNodes, double a, double b) {

        List<Double> xOriginal = new ArrayList<>();
        List<Double> yOriginal = new ArrayList<>();
        int plotPoints = 200;
        double step = (b - a) / (plotPoints - 1);
        for (int i = 0; i < plotPoints; i++) {
            double x = a + i * step;
            xOriginal.add(x);
            yOriginal.add(originalFunc.apply(x));
        }
        if (plotPoints > 1) {
            xOriginal.set(plotPoints - 1, b);
            yOriginal.set(plotPoints - 1, originalFunc.apply(b));
        }


        InterpolationService interpolationService = new InterpolationService();
        List<Double> xInterpolated = new ArrayList<>();
        List<Double> yInterpolated = new ArrayList<>();
        for (int i = 0; i < plotPoints; i++) {
            double x = a + i * step;
            xInterpolated.add(x);
            yInterpolated.add(interpolationService.lagrangeInterpolation(xNodes, yNodes, x));
        }
        if (plotPoints > 1) {
            xInterpolated.set(plotPoints - 1, b);
            yInterpolated.set(plotPoints - 1, interpolationService.lagrangeInterpolation(xNodes, yNodes, b));
        }


        List<Double> xNodeList = new ArrayList<>();
        List<Double> yNodeList = new ArrayList<>();
        for (int i = 0; i < xNodes.length; i++) {
            xNodeList.add(xNodes[i]);
            yNodeList.add(yNodes[i]);
        }

        XYChart chart = new XYChartBuilder()
                .width(800).height(600)
                .title("Interpolacja Lagrange'a")
                .xAxisTitle("X")
                .yAxisTitle("Y")
                .build();

        chart.addSeries("Funkcja oryginalna (" + functionLabel + ")", xOriginal, yOriginal).setMarker(SeriesMarkers.NONE);
        chart.addSeries("Wielomian interpolacyjny", xInterpolated, yInterpolated).setMarker(SeriesMarkers.NONE);
        XYSeries nodesSeries = chart.addSeries("Węzły interpolacji", xNodeList, yNodeList);
        nodesSeries.setXYSeriesRenderStyle(XYSeries.XYSeriesRenderStyle.Scatter);
        nodesSeries.setMarker(SeriesMarkers.CIRCLE);

        new SwingWrapper<>(chart).displayChart();
    }
}

