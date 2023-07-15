import pandas as pd
import csv

def csv_to_excel(csvfile, xlsxfile):
    csvReader = pd.read_csv(csvfile)
    save_xlsx = pd.ExcelWriter(xlsxfile)
    csvReader.to_excel(save_xlsx, index = False)
    save_xlsx.save()

def load_csv(csvfile):
    data = []
    with open(csvfile, newline="") as file:
        csvReader = csv.DictReader(file)
        for row in csvReader:
            data.append(row)
    return data
