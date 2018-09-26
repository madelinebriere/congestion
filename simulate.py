#!/usr/bin/python  
import os
import numpy as np
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
    l_max = 30
    open('iperf-all.txt', 'w').close() #clear the file
    open('ping-all.txt', 'w').close()
    for i in range(bw_min, bw_max, (bw_max-bw_min)/(args.num_bw-1)):
        for j in range(q_min, q_max, (q_max-q_min)/(args.num_q-1)):
            # Ref: stackoverflow How do I generate log uniform distribution
            l = np.exp(np.random.uniform(l_min, l_max))
            os.system('sudo python nodes.py -b %f -q %f -l %f' %(i/1000, j, l))
            os.system('cat iperf-recv.txt >> iperf-all.txt')
            os.system('cat ping-recv.txt >> ping-all.txt')

if __name__ == '__main__':
    simulate()