import unittest  
import os
from os import listdir
from os.path import isfile, join  
import csv
from etl.loader.cvmFileDataClient import CVMFileDataClient

class TestCVMFileDataClient(unittest.TestCase): 

    def testCanDownloadSomeFile(self):
        path = './tests/dataFiles/'
        client = CVMFileDataClient() 
        client.startProcess(path, 2020, 12)
        files = list([f for f in listdir(path) if isfile(join(path, f)) and f.endswith('csv')])        
        self.assertTrue(len(files) > 0)
        os.remove('./tests/dataFiles/202012.csv')

    def testDictMustContainsTheStartDateInTheFirstPosition(self):
        client = CVMFileDataClient()
        client.currentYear = 2020
        client.currentMonth = 12
        dict =  client.generateDownloadDict()
        self.assertTrue(list(dict)[0] == '202012')
    

    def testDictMustContainsTheURLToDownloadTheFile(self):
        client = CVMFileDataClient()
        client.currentYear = 2020
        client.currentMonth = 12
        dict =  client.generateDownloadDict()
        self.assertTrue(dict['202012'] == 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_202012.csv')
        

if __name__ == '__main__':
    unittest.main() 