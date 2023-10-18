import sys
import numpy as np


def approx_percentile(percentiles):
    sum = 0
    arr = []
    ret = []
    for percentile in percentiles:
        print(percentile)
        sum += percentile[0]
        chunk_size = percentile[0] / 10
        pc = percentile[1]
        backChunkLimit = sys.maxsize*-1
        for chunkLimit in pc:
            arr.append( (chunkLimit,backChunkLimit,chunk_size) )
            backChunkLimit =  chunkLimit
    arr.sort()
    print(arr)

    chunk_size = sum / 10

    ind = 0; current_chunk_size_to_fill = 0
    for i in range(1,10):
        current_chunk_size_to_fill += chunk_size
        while (True):
            current_chunk_size_to_fill -= arr[ind][2]
            if (current_chunk_size_to_fill > 0):
                ind += 1
                print ("passing " + str(arr[ind][2]) + " from " + str(arr[ind][1]) + " to " + str(arr[ind][0]) )
            else:
                step_ratio = (current_chunk_size_to_fill+ arr[ind][2])/arr[ind][2]
                step = (arr[ind][1]-arr[ind][0])
                newLimit = step_ratio*step  + arr[ind][1]
                ret.append( newLimit )
                print("setting " + str(newLimit) + " between " + str(arr[ind][1]) + " to " + str(arr[ind][0]))
                ind += 1
                break
    return ret

arr1 = np.random.normal(100, 10, 10000)
pc1 = np.percentile(arr1, (10,20,30,40,50,60,70,80,90))

arr2 = np.random.normal(105, 5, 1000)
pc2 = np.percentile(arr2, (10,20,30,40,50,60,70,80,90))

arr_total = np.concatenate((arr1,arr2))
pc_total = np.percentile(arr_total, (10,20,30,40,50,60,70,80,90))



pc_total_approx = approx_percentile( [(arr1.size,pc1),(arr2.size,pc2)] )

print ("Approx\n" + str(pc_total_approx) )
print("Exact\n" + str(pc_total) )


