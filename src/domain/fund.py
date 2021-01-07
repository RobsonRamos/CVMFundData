from domain.fundDailyData import FundDailyData
from typing import List
import json

class Fund:
    def __init__(self, taxId):
        self.taxId = taxId.replace('.', '').replace('/','').replace('-','')
        self.dailyData = []
    
    def addDailyInfo(self, data : FundDailyData):
        self.dailyData.append(data)

    def calculateDailyReturn(self, lastQuote = None):
        sorted(self.dailyData, key=lambda r: r.quoteDate)

        for i, v in enumerate(self.dailyData):
            if i == 0 and lastQuote != None and lastQuote > 0:
                v.dailyReturn = (v.quoteValue / lastQuote) - 1
            elif(i > 0 and i < len(self.dailyData)):                
                lastQuote = self.dailyData[i - 1].quoteValue                 
                if lastQuote != 0:
                    v.dailyReturn = (v.quoteValue / lastQuote) - 1

    
    def to_json(self): 
        json = {
            "_id" : self.taxId,
            "cnpj" : self.taxId,
            "dailyData" : []  
        }
        for data in self.dailyData:
            json['dailyData'].append(data.to_json())

        return json