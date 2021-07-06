#!/usr/bin/env python3
"""Play a sine signal."""
import argparse
import sys
import json
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
levi = 0
#tp_list =  np.arange(0.0,-30.0,-0.5)
tp_list =  np.arange(0.0,30.1,0.1)
tp_list = np.round(tp_list, 2)
print(tp_list)
np.set_printoptions(precision=1)
for tp in tp_list:

    #filename ='/Users/shota/Documents/klo_lab/matlab/phase/20201105/no'+str(tp)+'.mat'
    filename ='/Users/shota/Documents/klo_lab/matlab/phase/210604/LSGw_noref'+str(tp)+'.mat'
    if tp == 0.0:
        filename = '/Users/shota/Documents/klo_lab/matlab/phase/210428/LSGw-250.0.mat'
        phase_0 = sio.loadmat(filename)
        phase = phase_0['phix']
        A_sin = phase_0['sin_A']   
        phase_list.append(phase)

        A_list.append(A_sin)
    if tp ==30.0:
        filename ='/Users/shota/Documents/klo_lab/matlab/phase/210602/LSGw-30'+str(tp)+'.mat'
    phase_0 = sio.loadmat(filename)
    phase = phase_0['phix']
    phase_list.append(phase)
    A_list.append(np.ones(8))

        
with open('amp_list.json') as g:
    df = json.load(g)  
    
amp_L = df["amp"]  


def callback(outdata, frames, time, status):
   # if status:
    #    print(status, file=sys.stderr)
    global start_idx
    global phase_list
    global tp_num
    global f
    t = (start_idx + np.arange(frames)) / fs
    t = t.reshape(-1, 1)
    outdata[:,:] = 0
    outdata[:,0] = 1.95*np.reshape(amp_L[0] *A_list[tp_num][0]*np.sin(2 * np.pi * f * t-phase_list[tp_num][0]),outdata[:,0].shape)
    outdata[:,1] = 1.95*np.reshape(amp_L[1] *A_list[tp_num][1]*np.sin(2 * np.pi * f * t-phase_list[tp_num][1]),outdata[:,0].shape)
    outdata[:,2] = 1.95*np.reshape(amp_L[2] *A_list[tp_num][2]*np.sin(2 * np.pi * f * t-phase_list[tp_num][2]),outdata[:,0].shape)
    outdata[:,3] = 1.95*np.reshape(amp_L[3] *A_list[tp_num][3]*np.sin(2 * np.pi * f * t-phase_list[tp_num][3]),outdata[:,0].shape)
    outdata[:,14] = 1.95*np.reshape(amp_L[4] *A_list[tp_num][4]*np.sin(2 * np.pi * f * t-phase_list[tp_num][4]),outdata[:,0].shape)
    outdata[:,15] = 1.95*np.reshape(amp_L[5] *A_list[tp_num][5]*np.sin(2 * np.pi * f * t-phase_list[tp_num][5]),outdata[:,0].shape)
    outdata[:,16] = 1.95*np.reshape(amp_L[6] *A_list[tp_num][6]*np.sin(2 * np.pi * f * t-phase_list[tp_num][6]),outdata[:,0].shape)
    outdata[:,17] = 1.95*np.reshape(amp_L[7] *A_list[tp_num][7]*np.sin(2 * np.pi * f * t-phase_list[tp_num][7]),outdata[:,0].shape)
    start_idx += frames
    if levi == 1 and tp_num != len(tp_list)-1:
        tp_num += 1
    else:
        if tp_num != 0 and levi == 0:
            tp_num -= 1
       
with sd.OutputStream(device=4, channels=28, callback=callback,
                              samplerate=fs,blocksize=0):
    
    while True:
        
        key = input()
        if key == '':
            if levi == 0:
                levi = 1
                print('UP')
            else:
                levi = 0
                print('DOWN')