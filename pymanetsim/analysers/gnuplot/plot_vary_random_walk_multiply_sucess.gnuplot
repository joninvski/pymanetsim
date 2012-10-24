#Success
set terminal png
set data style linespoints
set key reverse Left outside
set decimalsign '.'

set output "results/images/vary_random_walk_multiply_result_success.png"

set title "Success varying the random walks spread Queries - ?? Max Hop - ??"
set xlabel "Number of random walks"
set ylabel "Number of Routes Found"

plot 'results/data_processed/bfg_normal_random_walk_multiply_routes_found.txt' using 1:2 ti "BFG 100"
