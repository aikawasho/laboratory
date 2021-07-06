#!/usr/bin/env python3
"""Play a sine signal."""
import argparse
import sys

import numpy as np
import sounddevice as sd
import scipy.io as sio
import json

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
A = 2.3
pi = np.pi
phase_list = []
A_list = []
tp_num = 0
#tp_list =  np.arange(-0.0,-30.0,-0.5)
tp_list =  np.arange(-21,0.1,0.1)
#tp_list2 =  np.arange(-14.0,10.0,0.1)

#tp_list = np.concatenate([tp_list1,tp_list2])
tp_list = np.round(tp_list, 2)
tp_list = np.append(tp_list,100)
np.set_printoptions(precision=1)
print(tp_list)
#for i,t in enumerate(tp_list):
 #   if t >= -13 and t <= -12.5:
  #      t = -12.5
   # tp_list[i] = t
    
#for i,t in enumerate(tp_list):
 #   if t >= -15 and t < -14:
  #      t = -14
   # tp_list[i] = t
    
for tp in tp_list:


        if tp == 100:

            A_list.append(np.ones(8))
            phase_list.append(np.zeros(8))
            

                          
        else:   
            filename ='/Users/shota/Documents/klo_lab/matlab/phase/210618/LSGBw-25'+str(tp)+'.mat'
            phase_0 = sio.loadmat(filename)
            phase = phase_0['phix']
            phase_list.append(phase)
           # A_sin = phase_0['sin_A']   
            #A_list.append(A_sin)
            A_list.append(np.ones(8))

#tp_list = np.append(tp_list,0.0)
        
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
    outdata[:,0] = A*np.reshape(amp_L[0] *A_list[tp_num][0]*np.sin(2 * np.pi * f * t-phase_list[tp_num][0]),outdata[:,0].shape)
    outdata[:,1] = A*np.reshape(amp_L[1] *A_list[tp_num][1]*np.sin(2 * np.pi * f * t-phase_list[tp_num][1]),outdata[:,0].shape)
    outdata[:,2] = A*np.reshape(amp_L[2] *A_list[tp_num][2]*np.sin(2 * np.pi * f * t-phase_list[tp_num][2]),outdata[:,0].shape)
    outdata[:,3] = A*np.reshape(amp_L[3] *A_list[tp_num][3]*np.sin(2 * np.pi * f * t-phase_list[tp_num][3]),outdata[:,0].shape)
    outdata[:,14] = A*np.reshape(amp_L[4] *A_list[tp_num][4]*np.sin(2 * np.pi * f * t-phase_list[tp_num][4]),outdata[:,0].shape)
    outdata[:,15] = A*np.reshape(amp_L[5] *A_list[tp_num][5]*np.sin(2 * np.pi * f * t-phase_list[tp_num][5]),outdata[:,0].shape)
    outdata[:,16] = A*np.reshape(amp_L[6] *A_list[tp_num][6]*np.sin(2 * np.pi * f * t-phase_list[tp_num][6]+np.pi),outdata[:,0].shape)
    outdata[:,17] = A*np.reshape(amp_L[7] *A_list[tp_num][7]*np.sin(2 * np.pi * f * t-phase_list[tp_num][7]+np.pi),outdata[:,0].shape)
    
   # outdata[:,0] = A*np.reshape(amp_L[0] *1.5*np.sin(A_list[tp_num][0])*np.sin(2 * np.pi * f * t-phase_list[tp_num][0]),outdata[:,0].shape)
  #  outdata[:,1] = A*np.reshape(amp_L[1] *1.5*np.sin(A_list[tp_num][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][1]),outdata[:,0].shape)
  #  outdata[:,2] = A*np.reshape(amp_L[2] *1.5*np.sin(A_list[tp_num][2])*np.sin(2 * np.pi * f * t-phase_list[tp_num][2]),outdata[:,0].shape)
  #  outdata[:,3] = A*np.reshape(amp_L[3] *1.5*np.sin(A_list[tp_num][3])*np.sin(2 * np.pi * f * t-phase_list[tp_num][3]),outdata[:,0].shape)
  #  outdata[:,14] = A*np.reshape(amp_L[4] *1.5*np.sin(A_list[tp_num][4])*np.sin(2 * np.pi * f * t-phase_list[tp_num][4]),outdata[:,0].shape)
  #  outdata[:,15] = A*np.reshape(amp_L[5] *1.5*np.sin(A_list[tp_num][5])*np.sin(2 * np.pi * f * t-phase_list[tp_num][5]),outdata[:,0].shape)
  #  outdata[:,16] = A*np.reshape(amp_L[6] *1.5*np.sin(A_list[tp_num][6])*np.sin(2 * np.pi * f * t-phase_list[tp_num][6]),outdata[:,0].shape)
  #  outdata[:,17] = A*np.reshape(amp_L[7] *1.5*np.sin(A_list[tp_num][7])*np.sin(2 * np.pi * f * t-phase_list[tp_num][7]),outdata[:,0].shape)
    start_idx += frames
       
with sd.OutputStream(device=4, channels=28, callback=callback,
                              samplerate=fs,blocksize = 0):
    
    while True:
        print(tp_list[tp_num])
        
        key = input()
        if key == '':
            if tp_num == len(tp_list)-1:
                tp_num = len(tp_list)-1

            else:
                tp_num += 1