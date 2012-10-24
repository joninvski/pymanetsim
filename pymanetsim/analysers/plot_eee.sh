#!/bin/sh

python analysers/parse_results.py

cd ..
pwd
gnuplot pymanetsim/analysers/gnuplot/plot_eee_vary_number_messages.gnuplot
gnuplot pymanetsim/analysers/gnuplot/plot_eee_vary_number_routes.gnuplot

eog "results/images/eee_vary_number_of_nodes_result_messages.png" &
eog "results/images/eee_vary_number_of_routes_result_messages.png" &
