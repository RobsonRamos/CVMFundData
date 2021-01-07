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

    def dropDatabase(self):                   
        client = self.createClient()
        client.drop_database('CVMFundData') 

    def createConnection(self):                   
        client = self.createClient()
        db = client['CVMFundData']
        return db 
     
    def getData(self, query: FundDailyDataQuery):
        try:
            db = self.createConnection()
            specification = [ 
                { '$match' : { 'cnpj' : query.cnpj }}
            ]
            if query.startDate is not None or query.endDate is not None:
                specification.append({ '$unwind' : '$dailyData'}) 

                if query.startDate is not None:
                    specification.append({ '$match' : {'dailyData.quoteDate': { '$gte' : query.startDate }}})                
                if query.endDate is not None:
                    specification.append({ '$match' : {'dailyData.quoteDate': { '$lt' : query.endDate }}})

                specification.append({ '$group' : { '_id' : '$_id', 'dailyData' : { '$push' : '$dailyData'}}})

            result = db.FundsDailyData.aggregate(specification)
            result = list({'data': data[item] for item in data if item == 'dailyData'} for data in result )
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
            funds = [] 
            
            bulk = collection.initialize_unordered_bulk_op()

            for key, fund in fundsDict.items(): 
                
                fundJSON = fund.to_json() 

                bulk.find({ '_id': fund.taxId }).upsert().update_one({
                    '$set':  { 'cnpj': fundJSON["cnpj"] }, 
                    '$push': { 'dailyData':  { '$each' : fundJSON['dailyData'] } }
                })

            bulk.execute()
        except Exception as error:
            traceback.print_exc()
            print("Error while inserting data to the database", error) 