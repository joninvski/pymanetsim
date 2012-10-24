#!/bin/sh

python analysers/parse_results.py

#gnuplot pymanetsim/analysers/gnuplot/plotMessages.gnuplot
#gnuplot pymanetsim/analysers/gnuplot/plotSuccess.gnuplot
#gnuplot pymanetsim/analysers/gnuplot/plotVaryRandomWalkQueriesMultiplyMessages.gnuplot
#gnuplot pymanetsim/analysers/gnuplot/plotVaryRandomWalkQueriesMultiplySuccess.gnuplot

cd ..
pwd
for filename in pymanetsim/analysers/gnuplot/*.gnuplot; do
    gnuplot $filename
done


montage -geometry 800x800+0+0 -bordercolor red  "results/images/vary_min_degree_result_messages.png" "results/images/vary_min_degree_measure_success.png" results/final_images/vary_min_degree.png

montage -geometry 800x800+0+0 -bordercolor red "results/images/vary_random_walk_multiply_result_messages.png" "results/images/vary_random_walk_multiply_result_success.png"  results/final_images/vary_multiply_result.png

montage -geometry 800x800+0+0 -bordercolor red "results/images/vary_number_of_nodes_result_messages.png" "results/images/vary_number_of_nodes_result_success.png"  results/final_images/vary_multiply_result.png


eog "results/final_images/" &
