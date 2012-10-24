set terminal png
set output "results/images/eee_vary_number_of_nodes_result_messages.png"

set data style linespoints
set key 1200,115000
set decimalsign '.'

set lmargin 12
set rmargin 4

#set title "Messages Varying the number of nodes."
set xlabel "Number of nodes"
set ylabel "Number of messages"

plot 'results/data_raw/dsr.txt' using 1:2 title "DSR",\
     'results/data_processed/eee_bfg_nodes_normal_number_of_nodes_follow_heat_messages.txt' using 1:2 title "BFG Follow Heat",\
     'results/data_processed/eee_bfg_nodes_normal_number_of_nodes_random_walk_messages.txt' using 1:2 title "BFG Random Walk",\
     'results/data_processed/eee_bfg_nodes_normal_number_of_nodes_dsr_messages.txt' using 1:2 title "BFG DSR Messages"

#plot 'results/data_processed/eee_bfg_nodes_normal_number_of_nodes_total_messages.txt' using 1:2 title "Total",\
