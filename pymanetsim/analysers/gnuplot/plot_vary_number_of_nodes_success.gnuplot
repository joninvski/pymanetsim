set terminal png
set output "results/images/vary_number_of_nodes_result_success.png"

set data style linespoints
set key reverse Left outside
set decimalsign '.'

set title "Messages Varying the numbe of nodes. Number Queries: ?? Max Hop: ?? Multiple RW: ??"
set xlabel "Number of nodes"
set ylabel "Number of Found Routes"

# f(x)=m*x+b
# fit f(x) "results/data_processed/dsr_normal_number_of_nodes_routes_found.txt" using 1:2 via m,b

# y(x)=n*x+p
# fit y(x) "results/data_processed/bfg_normal_number_of_nodes_routes_found.txt" using 1:2 via n,p


plot 'results/data_raw/dsr_normal_number_of_nodes_routes_found.txt' using 1:2 title "DSR",\
     'results/data_processed/bfg_normal_number_of_nodes_routes_found.txt' using 1:2 title "BFG Total"
#      f(x) title "DSR Approximation",\
#      y(x) title "BFG Approximation"
