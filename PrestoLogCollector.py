import json




def Semi_JSON_parse(rec,str):
    ind = 0
    token = ''
    waiting_for_token_end = False
    while (ind < len(str)):
        c = str[ind]
        if (c == '[' and str[ind+1]!="]"):
            ind += Semi_JSON_parse(rec, str[ind+1:])
            waiting_for_token_end = True
        elif (c == ']' and str[ind-1]!="[" ):
            ind+=1
            break
        elif (c == ','):
            if (not waiting_for_token_end) :
                rec.append(token.strip())
                token = ""
            else :
                waiting_for_token_end = False
        else:
            token += c
        ind += 1
    rec.append(token.strip())
    return ind




if __name__ == "__main__":
    input_file = "C:/Users/hedbn/Desktop/Presto slow log/presto_slow_or_failed_queries_test.log"
    output_file = "C:/Users/hedbn/Desktop/Presto slow log/presto_slow_or_failed_queries.output.tsv"

    record_list = []
    rec =[]


    with open(input_file, "r") as infile:
        for line in infile:
            rec = line.split("\t")
            lastToken = rec.pop()
            splitInd = lastToken.find("[")
            rec.append(lastToken[:splitInd])
            # rec.append(lastToken[splitInd:])

            Semi_JSON_parse(rec,lastToken[splitInd:])

            record_list.append(rec)




    outfile = open(output_file, "w")
    for rec in record_list:
        for cell in rec:
            outfile.write(cell)
            outfile.write("\t")
        outfile.write("\n")

    outfile.flush()
    outfile.close()

