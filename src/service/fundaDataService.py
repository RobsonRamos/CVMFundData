import sys
sys.path.append('../domain/')
sys.path.append('../data/')
from fundDailyDataQuery import FundDailyDataQuery
from database import Database

class FundDataService:
    def getFundData(self, query: FundDailyDataQuery):
        database = Database()
        return database.getData(query)

        
        
        