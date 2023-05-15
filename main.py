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
h_glass=15
h_air=50
h_concrete=10
h_insulation=20
h_oak=10
height=2.4

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

G[9,9]=h_glass
