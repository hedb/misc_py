
import numpy as np
import random
import matplotlib.pyplot as plt
import math

d = {}

for i in range(0, 10):
    for j in range(0, 10):
        for k in range(0, 10):
            if i*j*k not in d:
                d[i*j*k] = []
            d[i * j * k].append([i,j,k])

candidates = []
candidates.append(d[135])
candidates.append(d[45])
candidates.append(d[64])
candidates.append(d[280])
candidates.append(d[70])


for N1 in candidates[0]:
    for N2 in candidates[1]:
        for N3 in candidates[2]:
            for N4 in candidates[3]:
                for N5 in candidates[4]:
                    if \
                        N1[0] * N2[0] * N3[0] * N4[0] * N5[0] == 3000 \
                                and N1[1]  * N2[1] * N3[1] * N4[1] * N5[1] == 3969 \
                                and N1[2] * N2[2] * N3[2] * N4[2] * N5[2] == 640 :
                        print (N1, N2, N3, N4, N5)
