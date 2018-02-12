#!/usr/bin/python
import csv
with open('people.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        with open('insert.sql','ab') as writer:
            writer.write ('INSERT INTO Persons VALUES (' + row[0] + ',"' + row[1] + '","' + row[2] + '","' + row[3] + '","' + row[4] + '");\n')
        print ('INSERT INTO Persons VALUES (' + row[0] + ',"' + row[1] + '","' + row[2] + '","' + row[3] + '","' + row[4] + '")')

