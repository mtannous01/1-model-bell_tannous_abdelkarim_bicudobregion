import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import dm4bem

w_glass=0.02
w_cocncrete_ex=0.35
w_concrete_int=0.15
w_insulation=0.15
w_oak=0.04
lambda_air=0.025
lambda_concrete=1.4
lambda_insulation=0.035
lambda_oak=0.7
lambda_glass=1.05
h_glass=15
h_air=50
h_concrete=10
h_insulation=20
h_oak=10
height=2.4
density_concrete=2300
density_glass=2500
density_insulation=20
density_oak=750
cp_glass=840
cp_concrete=880
cp_insulation=1030
cp_oak=2380


Va = height*10.3*9.85                   # m³, volume of air
ACH = 1                     # air changes per hour
Va_dot = ACH / 3600 * Va    # m³/s, air infiltration
# ventilation & advection
Gv = 1.204 * 1000 * Va_dot

# P-controler gain
Kp = 1e4            # almost perfect controller Kp -> ∞
#Kp = 1e-3           # no controller Kp -> 0
#Kp = 0


A = np.zeros([26, 17])       # n° of branches X n° of nodes
A[0, 0], A[0,10] = -1,1                 # branch 0: <- node 0
A[1, 1] = -1    # branch 1: node 0 -> node 1
A[2, 1], A[2, 2] = -1, 1    # branch 2: node 1 -> node 2
A[3, 2], A[3, 3] = -1, 1    # branch 3: node 2 -> node 3
A[4, 4] = 1    # branch 4: node 3 -> node 4
A[5, 4], A[5, 5] = -1, 1    # branch 5: node 4 -> node 5
A[6, 4], A[6, 6] = -1, 1    # branch 6: node 4 -> node 6
A[7, 5], A[7, 6] = -1, 1    # branch 7: node 5 -> node 6
A[8, 7],A[8,3] = -1,1                 # branch 8: -> node 7
A[9, 8], A[9, 3] = -1, 1    # branch 9: node 5 -> node 7
A[10, 8] = 1                # branch 10: -> node 6
A[11, 3] = 1
A[12,3]=1# branch 11: -> node 6
A[13,3], A[13,10]=-1,1
A[14,3],A[14,9]=-1,1
A[15,9], A[15,10]=-1,1
A[16,10]=1
A[17,11]=1
A[18,10],A[18,11]=1,-1
A[19,12]=1
A[20,12]=-1
A[20,13]=1
A[21,13]=-1
A[21,14]=1
A[22,14],A[22,15]=-1,1
A[23,15],A[23,10]=-1,1
A[24,16], A[25,16],A[25,0]=1,-1,1

#Divide by 2 everywhere
#we have divided the app to two rooms: left room facing sun: upper wall-window+left wall=4.95+2.9+11=18.85
#bottom wall of the left room not facing sun: 10.47
#right room upper wall facing sun: 1.55+7.6-4.95=4.2
# right room buildings no sun: 11+5.53=16.53
G=np.zeros([26,26])
G[0,0]=2*lambda_concrete*height*16.53/w_cocncrete_ex+h_concrete*height*16.53
G[1,1]=lambda_concrete*height*10.47/w_cocncrete_ex+h_concrete*height*10.47
G[2,2]=lambda_concrete*height*10.47/w_cocncrete_ex+lambda_insulation*height*10.47/w_insulation
G[3,3]=lambda_insulation*height*10.47/w_insulation+h_insulation*height*10.47
G[4,4]=h_concrete*height*18.85
G[5,5]=lambda_concrete*height*18.85/w_cocncrete_ex
G[6,6]=lambda_concrete*height*18.85/w_cocncrete_ex+lambda_insulation*height*18.85/w_insulation
G[7,7]=lambda_concrete*height*18.85/w_cocncrete_ex
G[8,8]=h_insulation*height*18.85
G[9,9]=h_glass*height*2.5
G[10,10]=lambda_glass*height*2.5
G[11,11]=Gv
G[12,12]=Kp #perfect controller
G[13,13]=lambda_oak*height*1
G[14,14]=lambda_concrete*height*10.3/w_concrete_int+h_concrete*height*10.3
G[15,15]=lambda_concrete*height*10.3/w_concrete_int+h_concrete*height*10.3
G[16,16]=Kp
G[17,17]=lambda_glass*height*1.45
G[18,18]=h_glass*height*1.45
G[19,19]=h_concrete*height*5.65
G[20,20]=lambda_concrete*height*5.65/w_cocncrete_ex
G[21,21]=lambda_concrete*height*5.65/w_cocncrete_ex+lambda_insulation*height*5.65/w_insulation
G[22,22]=lambda_concrete*height*5.65/w_cocncrete_ex
G[23,23]=h_insulation*height*5.65
G[24,24]=lambda_concrete*height*16.53/w_cocncrete_ex+h_concrete*height*16.53
G[25,25]=lambda_concrete*height*16.53/w_cocncrete_ex+lambda_insulation*height*16.53/w_insulation

#Capacties
#Matrix C
C=np.zeros(17,17)
C[1,1]=cp_concrete*density_concrete*height*w_cocncrete_ex*10.47
C[2,2]=cp_insulation*density_insulation*height*w_insulation*10.47
C[5,5]=cp_concrete*density_concrete*height*w_cocncrete_ex*18.85
C[6,6]=cp_insulation*density_insulation*height*w_insulation*18.85
C[8,8]=cp_glass*density_glass*height*w_glass*2.5
C[9,9]=cp_oak*density_oak*height*w_oak
C[8,8]=cp_glass*density_glass*height*w_glass*1.45
C[13,13]=cp_concrete*density_concrete*height*w_cocncrete_ex*5.65
C[14,14]=cp_insulation*density_insulation*height*w_insulation*5.65
C[16,16]=cp_concrete*density_concrete*height*w_cocncrete_ex*16.53
C[0,0]=cp_insulation*density_insulation*height*w_insulation*16.53
