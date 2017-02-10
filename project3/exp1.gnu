# Gnuplot script for plotting data in experiment 1
set term png
set grid
set output "experiment1.png"
set title "Throughput vs. CBR rate"
set xlabel "CBR rate"
set ylabel "Throughput"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set key autotitle columnheader
plot 'exp1_Reno.data' using 1:2 with lines ls 2 title "throughput", "" using 1:2:3 with yerrorbars ls 1 title "std dev"

