#!/usr/bin/python  
import os
import numpy as np
import subprocess

from argparse import ArgumentParser

parse = ArgumentParser(description = "Number of data points")
parse.add_argument('--bwsegs', '-b',
	dest="num_bw",
	type = int,
	action = "store",
	help="Number of bandwidth slices",
	default = 7)

parse.add_argument('--qsegs', '-q',
	dest="num_q",
	type = int,
	action="store",
	help="Number of queue slices",
	default = 4)

parse.add_argument('--lsegs', '-l',
	dest="num_l",
	type = float,
	help = "Number of loss slices",
	action= "store",
	default=28)

args=parse.parse_args()

def simulate():
    bw_min = 10
    bw_max = 10000
    q_min = 5
    q_max = 30
    l_min = .003 
    l_max = 1.0
    delay = '60ms'
    open('output/data.txt', 'w').close()
    open('output/iperf-recv.txt', 'w').close() 
    open('output/ping-recv.txt', 'w').close()

    try:
        for i in range(bw_max, bw_min, -(bw_max-bw_min)/(args.num_bw)):
            for j in range(q_max, q_min, -(q_max-q_min)/(args.num_q)):
                # Ref: stackoverflow How do I generate log uniform distribution
                # TODO: Potentially fix?
                l = np.exp(np.random.uniform(l_min, l_max))
                b_str = str(float(i)/1000)
                q_str = str(j)
                l_str = str(l)

                print "Calling subprocess for BW=%s, Q=%s, L=%s, D=%s" % (b_str, q_str, l_str, delay)
                cmd = ['sudo', 'python', 'nodes.py', 
                    '-b', b_str, '-q', q_str, '-l', l_str, '-d', delay]
                subprocess.call(cmd)
                # Parse perf file.
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
                    if((len(perf_parsed) == 9) and ('Mbits' in perf_parsed[8])):
                        try:
                            perf_total+=float(perf_parsed[7])*1000000
                            perf_count+=1
                        except:
                            pass
                perf_av = 0
                if(perf_count!=0):
                    perf_av = float(perf_total)/perf_count
                perf_file.close()

                # Parse ping file.
                ping_file = open("output/ping-recv.txt")
                ping_total = 0.0
                ping_count = 0
                for ping_line in ping_file:
                    # TODO: Get ping average
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

                y_axis = (perf_av * ping_av)/1024

                print 'Average BW(B): %f, average RTT(s): %f' %(perf_av, ping_av)
                print 'Y_axis:   %s, X_axis: %s' % (str(y_axis), str(l))
                os.system('echo %f, %f >> output/data.txt' %(l,y_axis))

    except Exception as inst:
        print('Exiting program: %s' % type(inst))

if __name__ == '__main__':
    simulate()
