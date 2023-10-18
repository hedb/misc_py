
import csv

with open("C:/Users/hedbn/Downloads/p054_poker.txt") as csvfile:
        reader = csv.reader(csvfile,delimiter=' ')
        file = []
        for row in reader:
            file.append(row)

        print(file)
