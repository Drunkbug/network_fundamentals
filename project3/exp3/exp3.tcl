# new  simulator
# argument1: variant
# arugment2: queuing
# arugment3: tcp start time
# argument4: tcp stop time
# argument5: cbr start time
# argument6: cbr stop time
# argument7: program end time
# examples to run this program
# ns exp3.tcl Reno DropTail 1 5 3 4 6
# ns exp3.tcl Sack Red 1 30 10 20 31
set ns [new Simulator]
# define cbr flow rate and TCP variant
set cbrflow 5
set variant [lindex $argv 0]
set queuing [lindex $argv 1]
set tcp_starttime [lindex $argv 2]
set tcp_stoptime [lindex $argv 3]
set cbr_starttime [lindex $argv 4]
set cbr_stoptime [lindex $argv 5]
set program_end_time [lindex $argv 6]

# output trace file
set tf [open exp3_${variant}_${queuing}_${tcp_starttime}_${tcp_stoptime}.tr w]
puts "exp3_${variant}_${queuing}_${tcp_starttime}_${tcp_stoptime}.tr"
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
# duplex-link node node bandwidth(Mbps) latency(ms) drop_algorithm/RED
if {$queuing == "DropTail"} {
    $ns duplex-link $n1 $n2 10Mb 10ms DropTail
    $ns duplex-link $n2 $n3 10Mb 10ms DropTail
    $ns duplex-link $n3 $n4 10Mb 10ms DropTail
    $ns duplex-link $n3 $n6 10Mb 10ms DropTail
    $ns duplex-link $n5 $n2 10Mb 10ms DropTail
} elseif {$variant == "RED"} {
    $ns duplex-link $n1 $n2 10Mb 10ms RED
    $ns duplex-link $n2 $n3 10Mb 10ms RED
    $ns duplex-link $n3 $n4 10Mb 10ms RED
    $ns duplex-link $n3 $n6 10Mb 10ms RED
    $ns duplex-link $n5 $n2 10Mb 10ms RED
}

# setup TCP connection
if {$variant == "Reno"} {
    set n1tcp [new Agent/TCP/Reno]
    set n4sink [new Agent/TCPSink]
} elseif {$variant == "SACK"} {
    set n1tcp [new Agent/TCP/Sack1]
    set n4sink [new Agent/TCPSink/Sack1]
}

$ns attach-agent $n1 $n1tcp
# set sink from n1 to n4
$ns attach-agent $n4 $n4sink
$ns connect $n1tcp $n4sink
$n1tcp set fid_ 1
$n1tcp set window_ 10000

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

if {$cbrflow == 10} {
    $n2cbr set rate_ 9.9Mb
} else {
    $n2cbr set rate_ ${cbrflow}Mb
}

$n2cbr set type_ CBR
$n2cbr set packe_size_ 1000
$n2cbr set random_ false

# set n3 to null
set n3null [new Agent/Null]
$ns attach-agent $n3 $n3null

# set sink from n2 to n3
$ns connect $n2udp $n3null
$n2udp set fid_ 3

#Schedule events for CBR and FTP
$ns at $tcp_starttime "$n1ftp start"
$ns at $cbr_starttime "$n2cbr start"
$ns at $cbr_stoptime "$n2cbr stop"
$ns at $tcp_stoptime "$n1ftp stop"
$ns at $program_end_time "finish"

$ns run
