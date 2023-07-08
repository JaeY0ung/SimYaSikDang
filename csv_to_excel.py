import pandas as pd
import numpy as np

def csv_to_excel(area):
    csvfile = f"./csv/{area}술집.csv"
    csvReader = pd.read_csv(csvfile)

    # 저장할 xlsx파일의 이름을 정함
    save_xlsx = pd.ExcelWriter(f"./excel/{area}.xlsx")
    csvReader.to_excel(save_xlsx, index = False)

    #xlsx 파일로 저장
    save_xlsx.save()

csv_to_excel("홍대")