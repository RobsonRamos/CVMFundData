import sys
sys.path.append('./domain/')
sys.path.append('./etl/')
sys.path.append('./data/')
from etl.loader.cvmFileDataClient import CVMFileDataClient
from etl.reader.fundFileReader import FundFileReader
from data.database import Database
from datetime import datetime

class DataLoader:

    def loadData(self, startYear, startMonth):

        start = datetime.today() 
        path = './etl/dataFiles/'

        client = CVMFileDataClient()
        client.startProcess(path, startYear, startMonth) 
        
        end = datetime.today()   
        reader = FundFileReader()
        reader.parseFilesAndSave(path) 

        end = datetime.today()
        print('Total time')
        print((end - start))  
