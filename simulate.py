#!/usr/bin/python  
import os
import numpy as np
import subprocess
import math

from argparse import ArgumentParser

parse = ArgumentParser(description = "Number of data points")
parse.add_argument('--bwsegs', '-b',
	dest="num_bw",
	type = int,
	action = "store",
	help="Number of bandwidth slices",
	default = 3)

parse.add_argument('--qsegs', '-q',
	dest="num_q",
	type = int,
	action="store",
	help="Number of queue slices",
	default = 6)

parse.add_argument('--lsegs', '-l',
	dest="num_l",
	type = float,
	help = "Number of loss slices",
	action= "store",
	default=28)

args=parse.parse_args()

def parse_perf_file():
    perf_file = open("output/iperf-recv.txt")
    perf_count = 0.0
    perf_total = 0
    for perf_line in perf_file:
        perf_parsed = perf_line.split()
        if((len(perf_parsed) == 9) and ('Kbits' in perf_parsed[8])):
            try:
                perf_total+=float(perf_parsed[7])*1000
                perf_count+=1
            except:
                pass
        elif((len(perf_parsed) == 9) and ('Mbits' in perf_parsed[8])):
            try:
                perf_total+=float(perf_parsed[7])*1000000
                perf_count+=1
            except:
                   pass
        elif((len(perf_parsed) == 9) and ('bits' in perf_parsed[8])):
            try:
                perf_total+=float(perf_parsed[7])
                perf_count+=1
            except:
                   pass
    perf_av = 0
    if(perf_count!=0):
        perf_av = float(perf_total)/perf_count
    perf_file.close()
    return perf_av

def parse_ping_file():
    # Parse ping file.
    ping_file = open("output/ping-recv.txt")
    ping_total = 0.0
    ping_count = 0
    for ping_line in ping_file:
        ping_parsed = ping_line.split()
        if((len(ping_parsed) == 8) and
            ('time=' in ping_parsed[6])):
            try:
                time_parse=ping_parsed[6].split("=")
                ping_time = float(time_parse[1])/1000
                ping_total+=ping_time
                ping_count+=1
            except:
                pass
    ping_av = 0
    if(ping_count!=0):
        ping_av = float(ping_total)/ping_count
    ping_file.close()
    return ping_av

def run_net(l, b, q, d):
    print "---------------------------------"
    print "Calling subprocess for BW=%s, Q=%s, L=%s, D=%s" % (b, q, l, d)
    cmd = ['sudo', 'python', 'nodes.py', 
        '-b', b, '-q', q, '-l', l, '-d', d]
    subprocess.call(cmd)
    # Parse perf file.
    perf_av = parse_perf_file()
    # Parse ping file.
    ping_av = parse_ping_file()
    # TODO: Get MSS right.
    toret = (perf_av * ping_av)/(1024*8)
    print " "
    return toret


def simulate():
    # Adjust variables.
    # TODO: Need just 28 data points. More accurate.
    bw_min = 10
    bw_max = 10000
    q_min = 5
    q_max = 30
    l_min = math.log(0.01, math.e)
    l_max = math.log(5, math.e)
    delay = '15ms' # | -- 15 -- | -- 15 -- | --> 60ms
    open('output/data.txt', 'w').close()
    open('output/iperf-recv.txt', 'w').close() 
    open('output/ping-recv.txt', 'w').close()

    try:
        for l in np.logspace(l_min, l_max, args.num_l, base=math.e):
            l_str = str(l)
            y_total=0
            y_count=0
            # Average over range of bandwidths.
            for i in range(bw_max, bw_min-1, -(bw_max-bw_min)/(args.num_bw-1)):
                b_str = str(float(i)/1000)
                # Average over range of queue sizes.
                for j in range(q_max, q_min-1, -(q_max-q_min)/(args.num_q-1)):
                    q_str = str(j)
                    y_total+=run_net(l_str, b_str, q_str, delay)
                    y_count+=1
            y_axis = y_total/y_count

            print 'Averaged Iteration ... X_axis:   %f, Y_axis: %f' % (l, y_axis)
            os.system('echo %f, %f >> output/data.txt' %(l,y_axis))

    except Exception as inst:
        print('Exiting program: %s' % type(inst))

if __name__ == '__main__':
    simulate()
