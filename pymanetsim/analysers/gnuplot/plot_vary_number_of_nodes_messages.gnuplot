set terminal png
set output "results/images/vary_number_of_nodes_result_messages.png"

set data style linespoints
set key reverse Left outside
set decimalsign '.'

set title "Messages Varying the numbe of nodes. Number Queries: 49 Max Hop: 100 Multiple RW: 4"
set xlabel "Number of nodes"
set ylabel "Number of Messages"

# f(x)=m*x+b
# fit f(x) "results/data_processed/dsr_normal_number_of_nodes_total_messages.txt" using 1:2 via m,b

# y(x)=n*x+p
# fit y(x) "results/data_processed/bfg_normal_number_of_nodes_total_messages.txt" using 1:2 via n,p


plot 'results/data_processed/dsr_normal_number_of_nodes_total_messages.txt' using 1:2 title "DSR",\
     'results/data_processed/bfg_normal_number_of_nodes_total_messages.txt' using 1:2 title "BFG Total",\
     'results/data_processed/bfg_normal_number_of_nodes_follow_heat_messages.txt' using 1:2 title "BFG Follow Heat",\
     'results/data_processed/bfg_normal_number_of_nodes_random_walk_messages.txt' using 1:2 title "BFG Random Walk",\
     'results/data_processed/bfg_normal_number_of_nodes_go_back_messages.txt' using 1:2 title "BFG Go Back",\
     'results/data_processed/bfg_normal_number_of_nodes_hello_messages.txt' using 1:2 title "BFG Hello Messages",\
     'results/data_processed/bfg_normal_number_of_nodes_read_collision.txt' using 1:2 title "BFG Read Collision"
#      f(x) title "DSR Approximation",\
#      y(x) title "BFG Approximation"
