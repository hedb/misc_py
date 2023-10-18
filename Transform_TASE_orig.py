import csv

i = 0
input_header_rows = [1,2,3]
data_indexes = []
day_of_the_week = 5 # initial
output_header = ["day_of_the_week"]
output_rows = []


output_file = open('./TA125.output.csv', 'w', newline='')
writer = csv.writer(output_file)


output_file1 = open('./TA125.output_percentage.csv', 'w', newline='')
writer1 = csv.writer(output_file1)

with open('./TA125.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if i<=2:
            input_header_rows[i] = row
            if i==2:
                #print (str(header_rows[2])[:100])
                cell_ind = -1
                for cell in input_header_rows[0]:
                    cell_ind +=1
                    if (input_header_rows[0][cell_ind] != '') and (input_header_rows[2][cell_ind] != '#N/A Requesting Data...') :
                        output_header.append(input_header_rows[0][cell_ind])
                        data_indexes.append(cell_ind+1)
        if i>=2:
            if row[data_indexes[0]] != '#N/A':
                output_row = [day_of_the_week]
                if (day_of_the_week == 5) : day_of_the_week = 1
                else : day_of_the_week+= 1

                for ind in data_indexes:
                    output_row.append(row[ind])
                output_rows.append(output_row)

        i += 1

writer.writerow(output_header)
for row in output_rows:
    writer.writerow(row)


def isNumber(a):
    ret = True
    try:
        float(a)
    except:
        ret = False
    return ret

writer1.writerow(output_header)
isFirst = True
for row in output_rows:
    if isFirst :
        isFirst = False
    else:
        perc_row = [row[0]]
        i = 0
        for val in row:
            if i > 0:
                perc_val = 'NA' if not ( isNumber(row[i]) and isNumber(prev_row[i]) ) else (float(row[i]) - float(prev_row[i])) / float(prev_row[i])
                perc_row.append(perc_val)
            i += 1
        writer1.writerow(perc_row)

    prev_row = row
