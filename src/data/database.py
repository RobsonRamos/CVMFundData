import traceback
import datetime 
from pymongo.errors import BulkWriteError
import sys
sys.path.append('./domain/')
from domain.fundDailyData import FundDailyData
from domain.fundDailyDataQuery import FundDailyDataQuery
from pymongo import MongoClient, UpdateOne

class Database:

    def createClient(self):
        return MongoClient(host='localhost', port=27017)

    def recreateDatabase(self):                   
        client = self.createClient()
        client.drop_database('CVMFundData') 
        db = client['CVMFundData']
        collection = db['FundsDailyData']
        collection.create_index([ ("cnpj", -1) ])

    def createConnection(self):                   
        client = self.createClient()
        db = client['CVMFundData']
        return db 
     
    def getData(self, query: FundDailyDataQuery):
        try:
            db = self.createConnection()
            specification = {
                "cnpj" : query.cnpj 
            }
            if query.startDate is not None or query.endDate is not None:
                specification['quoteDate'] = { }
                if query.startDate is not None:
                    specification['quoteDate']['$gte'] = query.startDate
                if query.endDate is not None:
                    specification['quoteDate']['$lt'] = query.endDate
 
            result = db.FundsDailyData.find(specification, {'_id': False})
            result = { 'data': list(data for data in result)}
            print(result)
            return result
        
        except BulkWriteError as bwe:
            print(bwe.details)

        except (Exception) as error:
            traceback.print_exc()
            print("Error while getting data from the database", error)
    
    def insertData(self, fundsDict):
        
        print('saving data') 

        try:
            db = self.createConnection() 
            collection = db['FundsDailyData'] 
            bulk = collection.initialize_unordered_bulk_op()

            for key, fund in fundsDict.items():  
                for data in fund.dailyData:
                    json = data.to_json()
                    bulk.insert(json)

            bulk.execute()
        except Exception as error:
            traceback.print_exc()
            print("Error while inserting data to the database", error) 