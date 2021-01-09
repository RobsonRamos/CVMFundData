import csv
import traceback
from os import listdir
from datetime import datetime
from os.path import isfile, join  
import sys
sys.path.append('./domain/')
sys.path.append('./data/')
from domain.fund import Fund
from domain.fundDailyData import FundDailyData
from data.database import Database
import os

class FundFileReader:

    def parseFilesAndSave(self, path):

        files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('csv')]
        files.sort()
        fundDict = {} 
        lastInfosOfCurrentMonth = {}
        lastInfosOfLastMonth = {}
        db = Database()
        db.recreateDatabase()

        for file in files:
            try:
                print('Reading file:' + path + file) 

                with open(path + file) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    line_count = 0

                    for row in csv_reader:
                        if line_count > 0:
                            fund = Fund(row[0])

                            if(fund.taxId in fundDict):
                                fund = fundDict[fund.taxId]
                            else:
                                fundDict[fund.taxId] = fund

                            dailyData = FundDailyData(
                                row[0], row[1], row[2], row[3], row[4],
                                row[5], row[6], row[7])
                            
                            fund.addDailyInfo(dailyData)  
                            lastInfosOfCurrentMonth[fund.taxId] = dailyData

                        line_count += 1
                    
                    print('calculating returns')

                    for key, fund in fundDict.items(): 
                        if fund.taxId in lastInfosOfLastMonth:
                            lastInfoLastMonth = lastInfosOfLastMonth[fund.taxId]
                            fund.calculateDailyReturn(lastInfoLastMonth.quoteValue)
                        else:
                            fund.calculateDailyReturn()
                        
                        lastInfosOfLastMonth[fund.taxId] = lastInfosOfCurrentMonth[fund.taxId]  

                    db.insertData(fundDict)
                    lastInfosOfCurrentMonth.clear()
                    fundDict.clear()  

            except (Exception) as error:
                print('Error reading file:' + path + file) 
                traceback.print_exc() 
                raise
                
        return fundDict

