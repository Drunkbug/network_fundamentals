# Gnuplot script for plotting data in experiment 1
# for throughput
system "mkdir -p pic"
set term png
set grid
set output "./pic/experiment1_throughput.png"
set title "Throughput vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Throughput(Mbps)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 2
set style line 3 lc rgb '#91278F' lt 1 lw 1.5
set style line 4 lc rgb '#5B5B5B' lt 1 lw 1.5
set key autotitle columnheader
plot 'exp1_Reno.data' using 1:($2/1000) with lines ls 1 title "Reno", "" using 1:($2/1000):($3/1000) with yerrorbars ls 1 notitle, \
'exp1_Tahoe.data' using 1:($2/1000) with lines ls 2 title "Tahoe", "" using 1:($2/1000):($3/1000) with yerrorbars ls 2 notitle, \
'exp1_NewReno.data' using 1:($2/1000) with lines ls 3 title "NewReno", "" using 1:($2/1000):($3/1000) with yerrorbars ls 3 notitle, \
'exp1_Vegas.data' using 1:($2/1000) with lines ls 4 title "Vegas", "" using 1:($2/1000):($3/1000) with yerrorbars ls 4 notitle

# for latency 
set term png
set grid
set output "./pic/experiment1_latency.png"
set title "Latency vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Latency(s)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 2
set style line 3 lc rgb '#91278F' lt 1 lw 1.5
set style line 4 lc rgb '#5B5B5B' lt 1 lw 1.5
set key autotitle columnheader
plot 'exp1_Reno.data' using 1:4 with lines ls 1 title "Reno", "" using 1:4:5 with yerrorbars ls 1 notitle, \
'exp1_Tahoe.data' using 1:4 with lines ls 2 title "Tahoe", "" using 1:4:5 with yerrorbars ls 2 notitle, \
'exp1_NewReno.data' using 1:4 with lines ls 3 title "NewReno", "" using 1:4:5 with yerrorbars ls 3 notitle, \
'exp1_Vegas.data' using 1:4 with lines ls 4 title "Vegas", "" using 1:4:5 with yerrorbars ls 4 notitle


# for packets drop rate(pdr)
set term png
set grid
set output "./pic/experiment1_pdr.png"
set title "Packets Drop Rate vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Packets Drop Rate(%)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 2
set style line 3 lc rgb '#91278F' lt 1 lw 1.5
set style line 4 lc rgb '#5B5B5B' lt 1 lw 1.5
set key autotitle columnheader
plot 'exp1_Reno.data' using 1:6 with lines ls 1 title "Reno", "" using 1:6:7 with yerrorbars ls 1 notitle, \
'exp1_Tahoe.data' using 1:6 with lines ls 2 title "Tahoe", "" using 1:6:7 with yerrorbars ls 2 notitle, \
'exp1_NewReno.data' using 1:6 with lines ls 3 title "NewReno", "" using 1:6:7 with yerrorbars ls 3 notitle, \
'exp1_Vegas.data' using 1:6 with lines ls 4 title "Vegas", "" using 1:6:7 with yerrorbars ls 4 notitle

