import csv

#Receives data as list of sublists, with a sublist representing a row
def csv_writer(data, path):
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

def csv_reader(myfilepath):
    file_rows = []
    cr = csv.reader(open(myfilepath,"rb"))
    for row in cr:
        file_rows.append(row)
    return file_rows
