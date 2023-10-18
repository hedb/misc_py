import json
import os
from collections import Counter

input_dir = "C:/Users/hedbn/Downloads/Anodot Metric"
output_file = "C:/Users/hedbn/Downloads/Anodot Metric/output.tsv"

all_metrics = []

normal_metrics = 0; odd_metrics = 0

for filename in os.listdir(input_dir):
    if filename.startswith("wix_metrics"):
        input_file = os.path.join(input_dir, filename)
        with open(input_file, encoding="utf8") as data_file:
            print("processing : " + input_file)
            data = json.loads(data_file.read())
            for item in data['hits']['hits']:
                key = str(item['fields']['name'])

                # workarounds:
                key = key.replace(".rpc.rpc","_rpc_rpc")
                key = key.replace("bi-hadoop-master0a.42.wixprod.net.","bi-hadoop-master0a_42_wixprod_net_")
                key = key.replace("bi-wce-hadoop-master0a.42.wixprod.net.","bi-wce-hadoop-master0a_42_wixprod_net_")

                l1 = key.split(".")
                l = list(filter(lambda x: x.find('=') == -1 or x.find('root') >= 0 or x.find('src') == 0 or x.find('evid') == 0  , l1))

                num_of_odd_metric = len(l) - sum(1 for x in l if  (x.find('root') >= 0 or x.find('src') == 0 or x.find('evid') == 0  ) )

                if (num_of_odd_metric <= 1) :
                    normal_metrics +=1
                else :
                    odd_metrics+=1

                # # if (num_of_odd_metric > 1):
                # if (key.find('^root=wix-bi') != -1):
                #     print(key)
                #     print(l1)
                #     print(l)
                #     if (odd_metrics >=10):
                #         exit()

                all_metrics.append(str(l))
        continue
    else:
        continue


print("normal_metrics = {}, odd_metrics={}".format(normal_metrics,odd_metrics))

with open(output_file ,'w') as file:
    for item in Counter(all_metrics).items():
        file.write(item[0] + "\t" + str(item[1]) + '\n')


