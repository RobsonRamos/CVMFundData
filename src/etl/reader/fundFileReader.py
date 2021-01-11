import csv
import traceback
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join  
import sys
sys.path.append('./src/domain/')
sys.path.append('./src/data/')
from domain.fund import Fund
from domain.fundDailyData import FundDailyData
from data.database import Database

class FundFileReader:

    def parseFilesAndSave(self, path):

        files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('csv')]
        files.sort()
        fundDict = {} 
        lastDayInfosOfCurrentMonth = {}
        lastDayInfosOfLastMonth = {}
        db = Database()
        db.recreateDatabase()

        for file in files:
            try:
                
                fundDict,  lastDayInfosOfCurrentMonth = self.parseFile(path, file)                 
                self.calculateReturns(fundDict, lastDayInfosOfLastMonth, lastDayInfosOfCurrentMonth) 
                db.insertData(fundDict) 

            except (Exception):
                print('Error reading file:' + path + file) 
                traceback.print_exc() 
                raise   

    def parseFile(self, path, file):

        print('Reading file:' + path + file) 
        fundDict = {} 
        lastDayInfos = {}
        
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
                    lastDayInfos[fund.taxId] = dailyData 
                line_count += 1

        return (fundDict,  lastDayInfos)

    def calculateReturns(self, fundDict, lastInfosOfLastMonth, lastInfosOfCurrentMonth): 
        print('calculating returns')

        for key, fund in fundDict.items(): 
            if fund.taxId in lastInfosOfLastMonth:
                lastInfoLastMonth = lastInfosOfLastMonth[fund.taxId]
                fund.calculateDailyReturn(lastInfoLastMonth.quoteValue)
            else:
                fund.calculateDailyReturn()
                        
            lastInfosOfLastMonth[fund.taxId] = lastInfosOfCurrentMonth[fund.taxId] 

