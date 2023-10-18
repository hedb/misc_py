import sys
import numpy as np

def approx_percentile(percentiles, requested_percentiles):
    perc_len = len(percentiles[0][1])

    spreader = {};  arr = [] ; total_cases = 0

    step_size_arr = []; previous_point = 0
    requested_percentiles.append(100)

    for point in requested_percentiles:
        step_size_arr.append( (point-previous_point) / 100 )
        previous_point = point
    step_size_arr.append(0)

    for percentileCont in percentiles:
        if (len(percentileCont[1]) != perc_len): raise ValueError('All percentiles must be of the same size')
        percentile = percentileCont[1]
        num_of_cases = percentileCont[0]
        total_cases += num_of_cases

        starting_limit = percentile[0] - (percentile[1] - percentile[0])
        finishing_limit = percentile[perc_len-1] + (percentile[perc_len-1] - percentile[perc_len-2])
        percentile = np.concatenate( ([starting_limit],percentile,[finishing_limit] , [sys.maxsize] ) )

        previous_growth_rate = 0
        for i in range(0,len(percentile)-1):
            l = percentile[i]
            if (l in spreader):
                l = np.nextafter(l,l+1)
            spreader[l] = True
            growth_rate = (num_of_cases*step_size_arr[i]) / (percentile[i+1] - percentile[i] ) # cases per distance unit

            arr.append( (l,growth_rate,previous_growth_rate) )
            previous_growth_rate = growth_rate
    arr.sort()
    #print(arr)

    current_growth_rate = 0;ind = 0; current_chunk_size_to_fill = total_cases * step_size_arr[0]
    ret = []

    for i in range(0,len(arr)):
        current_growth_rate += arr[i][1] - arr[i][2]
        current_chunk_size_to_fill -= current_growth_rate * ( arr[i+1][0] - arr[i][0] )
        if (current_chunk_size_to_fill <= 0):
            ret.append( arr[i+1][0] + current_chunk_size_to_fill / current_growth_rate )
            current_chunk_size_to_fill += total_cases*step_size_arr[len(ret)]
        if (len(ret) == perc_len) :
            break
        else:
            continue

    return ret


#arr1 =

def calc_misplaced_items(unified_arr,pc_exact,pc_approx):
    if (len(pc_exact) != len(pc_approx)): raise ValueError('All percentiles must be of the same size')
    pc_exact = np.append(pc_exact,sys.maxsize); pc_approx = np.append(pc_approx,sys.maxsize)
    pc_last_ind = len(pc_exact) - 1
    exact_part = approx_part = -1
    exact_current_limit = approx_current_limit = -1 * sys.maxsize
    match_label_before = (exact_part == approx_part)
    mismatch_count = 0
    ret = []

    for case in unified_arr:
        if (case > exact_current_limit):
            exact_part += 1
            exact_current_limit = pc_exact[exact_part]
            if (exact_part > 0):
                ret.append(mismatch_count)
                mismatch_count = 0

        if (case > approx_current_limit):
            approx_part += 1
            approx_current_limit = pc_approx[approx_part]

        if (exact_part == pc_last_ind and approx_part == pc_last_ind) :
            ret.append(mismatch_count)
            break

        if (exact_part != approx_part):
            mismatch_count += 1
        match_label_before = (exact_part == approx_part)

    return ret


def compare_exact_and_approx(arrays,requested_percentiles,verbose = False):

    unified_arr = np.concatenate( arrays )
    pc_exact = np.percentile(unified_arr , requested_percentiles)
    if (verbose): print("Exact\n" + str(pc_exact) )

    approx_input = []
    for arr in arrays:
        approx_input.append(  (len(arr),np.percentile( arr,  requested_percentiles ))  )


    if (verbose): print("Approx\nInput:\n" + str(approx_input) )
    pc_approx = approx_percentile( approx_input ,requested_percentiles)
    if (verbose): print ("Result\n" + str(pc_approx) )

    misplaced_items = calc_misplaced_items(unified_arr,pc_exact,pc_approx)
    if (verbose): print("Distance = " + str(misplaced_items))
    if (verbose): print ("----------------------------------")
    return misplaced_items


np.random.seed(123456)

if (True) :
    assert (
        compare_exact_and_approx([[1,2,3,4,5,6,7,8,9,10],[1,2,3,4,5,6,7,8,9,10]],[10,90])
        ==
        [0, 0, 0]
    )

    assert (
        compare_exact_and_approx([[1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15,16,17,18,19,20]],[10,90])
        ==
        [0, 0, 0]
    )

    assert (
        compare_exact_and_approx([np.random.normal(100, 10, 10000),np.random.normal(100, 10, 10000)],[10,90],False)
        ==
        [0, 0, 0]
    )


    assert (
        compare_exact_and_approx([np.random.normal(100, 10, 10000),np.random.normal(105, 8, 10000)],[10,90],False)
        ==
        [0, 0, 0]
    )

    assert (
        compare_exact_and_approx([np.random.normal(100, 10, 10000),np.random.normal(105, 8, 10000) , np.random.normal(110, 4, 1000) ],[10,50,90],False)
        ==
        [0, 0, 0, 0]
    )

    assert (
        compare_exact_and_approx([np.random.normal(100, 10, 10000),np.random.normal(105, 8, 10000) , np.random.normal(110, 4, 1000) ],[10,20,30,40,50,60,70,80,90,95],False)
        ==
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )

if (True) :
    tmp = True
    #compare_exact_and_approx([[1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15,16,17,18,19,20]],[33,66],True)





if (True): # Test calc_misplaced_items
    dist = calc_misplaced_items(
            [1,2,3,4,5,6,7,8,9]# unified_arr,
            ,[5.5]# pc_exact
            ,[4.5]# pc_approx
            )
    assert ( dist == [1,0])

    dist = calc_misplaced_items(
            [1,2,3,4,5,6,7,8,9]# unified_arr,
            ,[4.5]# pc_exact
            ,[5.5]# pc_approx
            )
    assert ( dist == [0,1])
    #Two parts.
    # All the cases in the first part of the exact are in the first part of the approx
    # 5 is in the second part of the exact and is not in the second part of the approx


    dist = calc_misplaced_items(
            [1,2,3,4,5,6,7,8,9]# unified_arr,
            ,[5 ,7]# pc_exact
            ,[5,8]# pc_approx
            )
    assert ( dist == [0,0,1])


    dist = calc_misplaced_items(
            [1,2,3,4,5,6,7,8,9]# unified_arr,
            ,[4,7]# pc_exact
            ,[5,8]# pc_approx
            )
    assert ( dist == [0,1,1])


    dist = calc_misplaced_items(
            [1,2,3,4,5,6,7,8,9]# unified_arr,
            ,[5,7]# pc_exact
            ,[4,8]# pc_approx
            )
    assert ( dist == [1,0,1])


