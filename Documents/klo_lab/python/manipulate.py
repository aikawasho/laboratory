#!/usr/bin/env python3
"""Play a sine signal."""
import argparse
import sys

import numpy as np
import sounddevice as sd
import scipy.io as sio

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'frequency', nargs='?', metavar='FREQUENCY', type=float, default=500,
    help='frequency in Hz (default: %(default)s)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-a', '--amplitude', type=float, default=0.2,
    help='amplitude (default: %(default)s)')
args = parser.parse_args(remaining)

start_idx = 0
f = 40000
fs = 192000

pi = np.pi
phase_list = []
A_list = []
tp_num = 0
tp_list =  np.arange(-15,2.5,2.5)
##逆順##
#tp_list =  np.arange(0,-17.5,-2.5)
for tp in tp_list:
    sig = []
    ######位相のみ読み込むとき#######
    filename ='/Users/shota/Documents/klo_lab/matlab/phase/20201013/w_-15'+str(int(tp))+'.mat'
    phase_0 = sio.loadmat(filename)
    phase = phase_0['phix']
    phase_list.append(phase)
    A_list.append(np.ones(8))
    ######振幅, 位相を読み込む#######
    #filename ='/Users/shota/Documents/klo_lab/matlab/phase/20201013/LS_w_-15'+str(int(tp))+'.mat'
    #phase_0 = sio.loadmat(filename)
    #phase = phase_0['phix']
    #A_sin = phase_0['A_sin']   
    #phase_list.append(phase)
    #A_list.append(A_sin)
    

def callback(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    global start_idx
    global phase_list
    global tp_num
    global f
    t = (start_idx + np.arange(frames)) / fs
    t = t.reshape(-1, 1)
    outdata[:,:] = 0
    outdata[:,0] = np.reshape(0.20 *A_list[tp_num][0]*np.sin(2 * np.pi * f * t+phase_list[tp_num][0]),outdata[:,0].shape)
    outdata[:,1] = np.reshape(0.40 *A_list[tp_num][1]*np.sin(2 * np.pi * f * t+phase_list[tp_num][1]),outdata[:,0].shape)
    outdata[:,2] = np.reshape(0.97 *A_list[tp_num][2]*np.sin(2 * np.pi * f * t+phase_list[tp_num][2]),outdata[:,0].shape)
    outdata[:,3] = np.reshape(1.28 *A_list[tp_num][3]*np.sin(2 * np.pi * f * t+phase_list[tp_num][3]),outdata[:,0].shape)
    outdata[:,14] = np.reshape(0.71 *A_list[tp_num][4]*np.sin(2 * np.pi * f * t+phase_list[tp_num][4]),outdata[:,0].shape)
    outdata[:,15] = np.reshape(0.84 *A_list[tp_num][5]*np.sin(2 * np.pi * f * t+phase_list[tp_num][5]),outdata[:,0].shape)
    outdata[:,16] = np.reshape(1.8 *A_list[tp_num][6]*np.sin(2 * np.pi * f * t+phase_list[tp_num][6]),outdata[:,0].shape)
    outdata[:,17] = np.reshape(2.20 *A_list[tp_num][7]*np.sin(2 * np.pi * f * t+phase_list[tp_num][7]),outdata[:,0].shape)
    start_idx += frames
       
with sd.OutputStream(device=4, channels=28, callback=callback,
                              samplerate=fs,blocksize = 0):
    
    while True:
        print(tp_list[tp_num])
        key = input()
        if key == '':
            if tp_num == len(tp_list)-1:
                tp_num = 0
            else:
                tp_num += 1