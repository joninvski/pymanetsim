#Success
set terminal png
set output "results/images/vary_random_walk_multiply_result_messages.png"
set data style linespoints
set key reverse Left outside
set decimalsign '.'

set title "Messages varying the random walks spread in 49 Queries - MaxHop 200"
set xlabel "Number of random walks"
set ylabel "Number of Messages"

plot 'results/data_processed/bfg_normal_random_walk_multiply_total_messages.txt' using 1:2 ti "BFG Total",\
     'results/data_processed/bfg_normal_random_walk_multiply_follow_heat_messages.txt' using 1:2 ti "BFG Follow Heat",\
     'results/data_processed/bfg_normal_random_walk_multiply_random_walk_messages.txt' using 1:2 ti "BFG Random Walk",\
     'results/data_processed/bfg_normal_random_walk_multiply_go_back_messages.txt' using 1:2 ti "BFG Go Back",\
     'results/data_processed/bfg_normal_random_walk_multiply_hello_messages.txt' using 1:2 ti "BFG Hello Messages",\
     'results/data_processed/bfg_normal_random_walk_multiply_read_collision.txt' using 1:2 ti "BFG Read Collisions"
