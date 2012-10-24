set terminal png
set output "results/images/eee_vary_number_of_routes_result_messages.png"

set data style linespoints
#set key 1200,115000
set decimalsign '.'

set lmargin 12
set rmargin 4

#set title "Messages Varying the number of routes."
set xlabel "Number of request routes"
set ylabel "Number of messages"

set logscale y

plot 'results/data_processed/dsr_routes.txt' using 1:2 title "DSR",\
     'results/data_processed/eee_bfg_normal_routes_requests_follow_heat_messages.txt' using 1:2 title "BFG Follow Heat",\
     'results/data_processed/eee_bfg_normal_routes_requests_random_walk_messages.txt' using 1:2 title "BFG Random Walk",\
     'results/data_processed/eee_bfg_normal_routes_requests_dsr_messages.txt' using 1:2 title "BFG DSR Messages"

