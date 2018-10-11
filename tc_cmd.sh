#!/bin/bash

qlen=$1
delay=$2
loss=$3
rate=$4

function add_qdisc {
    dev=$1
    tc qdisc del dev $dev root
    echo qdisc removed

    tc qdisc add dev $dev root handle 1:0 htb default 1
    echo qdisc added

    tc class add dev $dev parent 1:0 classid 1:1 htb rate $rate ceil $rate
    echo classes created

    tc qdisc add dev $dev parent 1:1 handle 10: netem delay $delay limit $qlen loss $loss

    ifconfig $dev mtu 1064

    echo parameters added
}

add_qdisc s0-eth1
add_qdisc s0-eth2