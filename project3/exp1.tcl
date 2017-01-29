# new simulator
set ns [new Simulator]
# define cbr flow rate and TCP variant
set cbrflow [lindex $argv 0]
set variant [lindex $argv 1]
# output trace file
set tf [open exp1_${variant}_${cbrflow}.tr w]
$ns trace-all $tf

# finish 
proc finish {} {
  exit 0
}

# initialize node n1-n6
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

# link the nodes with 10Mbps speed
# duplex-link node node bandwith(Mbps) latency(ms) drop_algorithm
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail


# setup TCP connection
if {$variant == "Tahoe"} {
  set n1tcp [new Agent/TCP]
} elseif {$variant == "Reno"} {
  set n1tcp [new Agent/TCP/Reno]
} elseif {$variant == "NewReno"} {
  set n1tcp [new Agent/TCP/Newreno]
} elseif {$variant == "Vegas"} {
  set n1tcp [new Agent/TCP/Vegas]
}

$ns attach-agent $n1 $n1tcp
# set sink from n1 to n4
set n4sink [new Agent/TCPSink]
$ns attach-agent $n4 $n4sink
$ns connect $n1tcp $n4sink

# set a ftp over TCP connection
set n1ftp [new Application/FTP]
$n1ftp attach-agent $n1tcp
$n1ftp set type_ FTP

# setup UDP connection
set n2udp [new Agent/UDP]
$ns attach-agent $n2 $n2udp
# setup cbr over n2udp
set n2cbr [new Application/Traffic/CBR]
$n2cbr attach-agent $n2udp
$n2cbr set type_ CBR
$n2cbr set packet_size_ 1000
$n2cbr set rate_ 1mb
$n2cbr set random_ false

# set n3 to null
set n3null [new Agent/Null]
$ns attach-agent $n3 $n3null

# set sink from n2 to n3
$ns connect $n2udp $n3null


# Schedule events for CBR and FTP
$ns at 0.1 "$n2cbr start"
$ns at 1.0 "$n1ftp start"
$ns at 4.0 "$n1ftp stop"
$ns at 4.5 "$n2cbr stop"
$ns at 5.0 "finish"

puts "CBR packet size = [$n2cbr set packet_size_]"
puts "TCP window size = [$n1tcp set window_]"
puts "input0=$cbrflow"
puts "input1=$variant"

$ns run


