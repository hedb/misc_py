import json
import sys


with open('/Users/hed-bar-nissan/marriot_declan.txt') as f_in:
    data = json.load(f_in)
    # with open('/Users/hed-bar-nissan/marriot_declan_pretty.txt' ,'w', encoding='utf-8') as f_out:
        # json.dump(data, f_out, ensure_ascii=False, indent=4)
    print ('id', '\t', 'size', '\t', 'num samples', '\t', 'sample_size', '\t', 'final_url')
    for i,elem in enumerate(data):
        print (i,'\t', len(json.dumps(elem)), '\t', len(json.loads(elem['samples'])), '\t', len(json.dumps(elem['samples'])), '\t', elem['fingerprints']['$set'][0])

    # print(data[-1]['fingerprints']['$set'][0])
