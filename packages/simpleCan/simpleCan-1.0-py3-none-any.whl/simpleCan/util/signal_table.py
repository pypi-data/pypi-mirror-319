import logging

import pandas, openpyxl
from simpleCan.util import dataStructure as ds

class Signal_table_messageList:

    def __init__(self):
        self.messageList = []
        self.excel_table_path = ''

    def setExcelPath(self, path):
        self.excel_table_path = path
        logging.info(self.excel_table_path)
        self.read_Excel_into_messageList()

    def read_Excel_into_messageList(self):
        self.clearMessageList()
        try:
            data_frame = pandas.read_excel(self.excel_table_path)
            for i in range(len(data_frame)):
                message = ds.CanMessage(id = int(data_frame['id'][i], 16), data = [int(x, 16) for x in str(data_frame['data'][i]).split(',')],
                                        period = float(data_frame['periodic'][i]))
                self.messageList.append(message)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def clearMessageList(self):
        self.messageList = []
    def get_messageList(self):
        return self.messageList

    def printMessageList(self):
        for i in range(len(self.messageList)):
            print(self.messageList[i].id)
            print(self.messageList[i].data)
            print(self.messageList[i].period)









