import unittest   
import csv 
from domain.fund import Fund
from domain.fundDailyData import FundDailyData

class TestFund(unittest.TestCase): 

    def testFundMustCNPJWithoutSpecialCharacters(self):
        fund = Fund('00.068.305/0001-35')
        self.assertEqual(fund.taxId, '00068305000135')
        
    def testCanCreateJSON(self):
        fund = Fund('00.068.305/0001-35')
        json = fund.to_json()
        self.assertEqual(json['cnpj'], '00068305000135')

    def testCanCalculateReturn(self):
        fund = Fund('00.068.305/0001-35')
        data1 = FundDailyData(taxId=fund.taxId, quoteDate= '2020-01-02', quoteValue= 1)
        data2 = FundDailyData(taxId=fund.taxId, quoteDate= '2020-01-01', quoteValue= 2)
        fund.addDailyInfo(data1)
        fund.addDailyInfo(data2)
        fund.calculateDailyReturn()
        self.assertTrue(fund.dailyData[1].dailyReturn == 1)

    def testCanCalculateNegativeReturns(self):
        fund = Fund('00.068.305/0001-35')
        data1 = FundDailyData(taxId=fund.taxId, quoteDate= '2020-01-02', quoteValue= 2)
        data2 = FundDailyData(taxId=fund.taxId, quoteDate= '2020-01-01', quoteValue= 1)
        fund.addDailyInfo(data1)
        fund.addDailyInfo(data2)
        fund.calculateDailyReturn()
        self.assertTrue(fund.dailyData[1].dailyReturn == -0.5)

    def testCanCalculateReturnWithPreviousQuote(self):
        fund = Fund('00.068.305/0001-35')
        data1 = FundDailyData(taxId=fund.taxId, quoteDate= '2020-01-02', quoteValue= 9)
        data2 = FundDailyData(taxId=fund.taxId, quoteDate= '2020-01-01', quoteValue= 2)
        fund.addDailyInfo(data1)
        fund.addDailyInfo(data2)
        fund.calculateDailyReturn(3)
        self.assertTrue(fund.dailyData[0].dailyReturn == 2)
        
if __name__ == '__main__':
    unittest.main() 