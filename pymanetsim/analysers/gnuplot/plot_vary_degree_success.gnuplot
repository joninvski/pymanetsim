set terminal png
set data style linespoints
set key reverse Left outside
set decimalsign '.'

set output "results/images/vary_min_degree_measure_success.png"

set title "Success Varying the Degree Level"
set xlabel "Number of node neighbours"
set ylabel "Number of Routes found"

# f(x)=m*x+b
# fit f(x) "results/data_processed/dsr_normal_min_degree_routes_found.txt" using 1:2 via m,b

# y(x)=m*x+b
# fit y(x) "results/data_processed/bfg_normal_min_degree_routes_found.txt" using 1:2 via m,b


plot 'results/data_processed/dsr_normal_min_degree_routes_found.txt' using 1:2 title "DSR",\
     'results/data_processed/bfg_normal_min_degree_routes_found.txt' using 1:2 title "BFG"
#      f(x) title "DSR Approximation",\
#      y(x) title "BFG Approximation"
