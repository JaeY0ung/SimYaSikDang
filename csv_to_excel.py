import pandas as pd

def csv_to_excel(area):
    csvfile = f"./csv/{area}.csv"
    csvReader = pd.read_csv(csvfile)

    # 저장할 xlsx파일의 이름을 정함
    save_xlsx = pd.ExcelWriter(f"./excel/{area}.xlsx")
    csvReader.to_excel(save_xlsx, index = False)

    #xlsx 파일로 저장
    save_xlsx.save()

def csv_to_excel_2(area):
    csvfile = f"./csv/{area}_processed.csv"
    csvReader = pd.read_csv(csvfile)

    # 저장할 xlsx파일의 이름을 정함
    save_xlsx = pd.ExcelWriter(f"./excel/{area}_processed.xlsx")
    csvReader.to_excel(save_xlsx, index = False)

    #xlsx 파일로 저장
    save_xlsx.save()