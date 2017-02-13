# Gnuplot script for plotting data in experiment 1
# for throughput
system "mkdir -p pic"
set term png
set grid
set output "./pic/experiment3_Reno_and_SACK_DropTail_and_RED_latency.png"
set title "Time vs Latency"
set xlabel "Time(second)"
set ylabel "Latency(second)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set style line 3 lc rgb '#ff0000' lt 1 lw 1.5
set style line 4 lc rgb '#ff00e9' lt 1 lw 1.5
#set yrange [*<0:0.1<*]
set key autotitle columnheader
plot "<(sed -n '1,200p' ./data/exp3_Reno_DropTail_5.data)" using 1:3 with lines ls 1 title "Reno DropTail" \
   , "<(sed -n '1,200p' ./data/exp3_SACK_DropTail_5.data)" using 1:3 with lines ls 2 title "Sack DropTail" \
   , "<(sed -n '1,200p' ./data/exp3_Reno_RED_5.data)" using 1:3 with lines ls 3 title "Reno RED" \
      , "<(sed -n '1,200p' ./data/exp3_SACK_RED_5.data)" using 1:3 with lines ls 4 title "SACK RED"
   

