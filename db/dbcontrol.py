import sqlite3
from src.area import areas_dict_test, k_to_e

class DBcontroller:
    def __init__(self):
        self.db_loc = './db/simyasikdang.db'
        self.conn = None 
        self.cursor = None 

    def connect(self):
        self.conn = sqlite3.connect(self.db_loc, check_same_thread=False)
        self.cursor = self.conn.cursor()

    #? 정확히 언제씀..?
    def disconnect(self):
        self.conn.close()
        
    def csv_to_db(self):
        query = '.mode csv' 
        self.cursor.execute(query)
        for gu in areas_dict_test.keys():
            for area in areas_dict_test[gu]:
                #? 포맷팅 시 ' 써야 하는지.
                import_query = f'.import ../csv/{k_to_e[area]}_processed.csv {k_to_e[area]}'
                #? fetchall 해야 하는지