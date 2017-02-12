# Gnuplot script for plotting data in experiment 1
# for throughput
system "mkdir -p pic"
set term png
set grid
set output "./pic/experiment2_NewReno_Reno_throughput.png"
set title "Throughput(NewReno/Reno) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Throughput(Mbps)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_NewReno_Reno.data)" using 1:($3/1000) with lines ls 1 title "NewReno", "" using 1:($3/1000):($4/1000) with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_NewReno_Reno.data)" using 1:($3/1000) with lines ls 2 title "Reno", "" using 1:($3/1000):($4/1000) with yerrorbars ls 2 notitle


set term png
set grid
set output "./pic/experiment2_NewReno_Vegas_throughput.png"
set title "Throughput(NewReno/Vegas) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Throughput(Mbps)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_NewReno_Vegas.data)" using 1:($3/1000) with lines ls 1 title "NewReno", "" using 1:($3/1000):($4/1000) with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_NewReno_Vegas.data)" using 1:($3/1000) with lines ls 2 title "Vegas", "" using 1:($3/1000):($4/1000) with yerrorbars ls 2 notitle

set term png
set grid
set output "./pic/experiment2_Reno_Reno_throughput.png"
set title "Throughput(Reno/Reno) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Throughput(Mbps)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_Reno_Reno.data)" using 1:($3/1000) with lines ls 1 title "Reno", "" using 1:($3/1000):($4/1000) with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_Reno_Reno.data)" using 1:($3/1000) with lines ls 2 title "Reno", "" using 1:($3/1000):($4/1000) with yerrorbars ls 2 notitle

set term png
set grid
set output "./pic/experiment2_Vegas_Vegas_throughput.png"
set title "Throughput(Vegas/Vegas) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Throughput(Mbps)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_Vegas_Vegas.data)" using 1:($3/1000) with lines ls 1 title "Vegas", "" using 1:($3/1000):($4/1000) with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_NewReno_Reno.data)" using 1:($3/1000) with lines ls 2 title "Vegas", "" using 1:($3/1000):($4/1000) with yerrorbars ls 2 notitle

# for latency
set term png
set grid
set output "./pic/experiment2_NewReno_Reno_latency.png"
set title "Latency(NewReno/Reno) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Latency(s)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_NewReno_Reno.data)" using 1:5 with lines ls 1 title "NewReno", "" using 1:5:6 with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_NewReno_Reno.data)" using 1:5 with lines ls 2 title "Reno", "" using 1:5:6 with yerrorbars ls 2 notitle


set term png
set grid
set output "./pic/experiment2_NewReno_Vegas_latency.png"
set title "Latency(NewReno/Vegas) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Latency(s)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_NewReno_Vegas.data)" using 1:5 with lines ls 1 title "NewReno", "" using 1:5:6 with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_NewReno_Vegas.data)" using 1:5 with lines ls 2 title "Vegas", "" using 1:5:6 with yerrorbars ls 2 notitle


set term png
set grid
set output "./pic/experiment2_Reno_Reno_latency.png"
set title "Latency(Reno/Reno) vs. CBR rate"
set xlabel "CBR rate(s)"
set ylabel "Latency(s)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_Reno_Reno.data)" using 1:5 with lines ls 1 title "Reno", "" using 1:5:6 with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_Reno_Reno.data)" using 1:5 with lines ls 2 title "Reno", "" using 1:5:6 with yerrorbars ls 2 notitle


set term png
set grid
set output "./pic/experiment2_Vegas_Vegas_latency.png"
set title "Latency(Vegas/Vegas) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Latency(s)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_Vegas_Vegas.data)" using 1:5 with lines ls 1 title "Vegas", "" using 1:5:6 with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_Vegas_Vegas.data)" using 1:5 with lines ls 2 title "Vegas", "" using 1:5:6 with yerrorbars ls 2 notitle

# for packets drop rate
set term png
set grid
set output "./pic/experiment2_NewReno_Reno_pdr.png"
set title "PDR(NewReno/Reno) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Packets Drop Rate(%)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_NewReno_Reno.data)" using 1:7 with lines ls 1 title "NewReno", "" using 1:7:8 with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_NewReno_Reno.data)" using 1:7 with lines ls 2 title "NewReno", "" using 1:7:8 with yerrorbars ls 2 notitle

set term png
set grid
set output "./pic/experiment2_NewReno_Vegas_pdr.png"
set title "PDR(NewReno/Vegas) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Packets Drop Rate(%)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_NewReno_Vegas.data)" using 1:7 with lines ls 1 title "NewReno", "" using 1:7:8 with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_NewReno_Vegas.data)" using 1:7 with lines ls 2 title "Vegas", "" using 1:7:8 with yerrorbars ls 2 notitle

set term png
set grid
set output "./pic/experiment2_Reno_Reno_pdr.png"
set title "PDR(Reno/Reno) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Packets Drop Rate(%)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_Reno_Reno.data)" using 1:7 with lines ls 1 title "Reno", "" using 1:7:8 with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_Reno_Reno.data)" using 1:7 with lines ls 2 title "Reno", "" using 1:7:8 with yerrorbars ls 2 notitle

set term png
set grid
set output "./pic/experiment2_Vegas_Vegas_pdr.png"
set title "PDR(Vegas/Vegas) vs. CBR rate"
set xlabel "CBR rate(Mbps)"
set ylabel "Packets Drop Rate(%)"
set style line 1 lc rgb '#0060ad' lt 1 lw 1.5
set style line 2 lc rgb '#FA9D00' lt 1 lw 1.5
set key autotitle columnheader
plot "<(sed -n '1,20p' exp2_Vegas_Vegas.data)" using 1:7 with lines ls 1 title "Vegas", "" using 1:7:8 with yerrorbars ls 1 notitle \
   , "<(sed -n '21,39p' exp2_Vegas_Vegas.data)" using 1:7 with lines ls 2 title "Vegas", "" using 1:7:8 with yerrorbars ls 2 notitle
