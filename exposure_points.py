import json
import sys

i = 1
with open('exposure_points.json', "r") as infile:
    for line in infile:
        try:
            j = json.loads(line)
            #print(str(i) + ' : ' + str(j))
            print(str(i) + ' : ' + str(len(j["eventGroups"][0]["events"])))
        except:
            print ("Error: at " + str(i) +  str(sys.exc_info()[0]))
            print(line)
            #raise
        i += 1
