import unittest  
import os
from os import listdir
from os.path import isfile, join  
import csv
from etl.reader.fundFileReader import FundFileReader


class TestFundFileReader(unittest.TestCase): 

    def testCanParseFile(self):
        path = './tests/files/'
        file = '201801.csv'
        reader = FundFileReader()
        fundDict,  _ = reader.parseFile(path, file)
        self.assertTrue(list(fundDict)[0] == '00017024000153')
        self.assertTrue(list(fundDict)[1] == '00068305000135')

    def testCanParseDailyData(self):
        path = './tests/files/'
        file = '201801.csv'
        reader = FundFileReader()
        fundDict,  _ = reader.parseFile(path, file)
        self.assertTrue(len(fundDict['00017024000153'].dailyData) > 0)

    def testCanParsePortfolioValueInfo(self):
        path = './tests/files/'
        file = '201801.csv'
        reader = FundFileReader()
        fundDict,  _ = reader.parseFile(path, file)
        self.assertTrue(fundDict['00017024000153'].dailyData[0].portfolioValue == 1130197.89)

    def testInfosOfCurrentMonthMustBeGenerated(self):
        path = './tests/files/'
        file = '201801.csv'
        reader = FundFileReader()
        _,  infosOfCurrentMonth = reader.parseFile(path, file)
        self.assertTrue(len(infosOfCurrentMonth) > 0) 

    def testCalculateReturn(self):
        path = './tests/files/'
        file = '201801.csv'
        reader = FundFileReader()
        fundDict,  infosOfCurrentMonth = reader.parseFile(path, file)
        lastMonth = {}
        #print(len(infosOfCurrentMonth['00017024000153'])
        reader.calculateReturns(fundDict, lastMonth, infosOfCurrentMonth)
        self.assertTrue(fundDict['00017024000153'].dailyData[0].dailyReturn == None) 
        print(fundDict['00017024000153'].dailyData[1].dailyReturn == 0.00017322291172083837)
        

if __name__ == '__main__':
    unittest.main() 