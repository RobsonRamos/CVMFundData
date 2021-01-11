import requests
from string import Template
from datetime import datetime
import asyncio
import aiohttp      
import aiofiles

class CVMFileDataClient:

    def startProcess(self, path, startYear, startMonth): 
            self.currentYear = startYear
            self.currentMonth = startMonth
            downloadDict = self.generateDownloadDict()
            asyncio.run(self.downloadAndSaveFiles(downloadDict, path))

    async def downloadAndSaveFiles(self, downloadDict, path): 
        semaphore = asyncio.BoundedSemaphore(12) # number of async jobs
        jobs = []
        for fileName in downloadDict:
            jobs.append(asyncio.ensure_future(self.downloadFile(path, fileName, downloadDict[fileName], semaphore)))        
        await asyncio.gather(*jobs) 

    def generateDownloadDict(self):   
        currentMonthStr = ''
        downloadDict = {}

        while datetime(self.currentYear, self.currentMonth, 1) < datetime(datetime.today().year, datetime.today().month, 1):
            if(self.currentMonth < 10):
                currentMonthStr = '0' + str(self.currentMonth)
            else:
                currentMonthStr = str(self.currentMonth)
            
            yearMonth = str(self.currentYear) + currentMonthStr
            
            t = Template('http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_${yearMonth}.csv')
            url = t.substitute(yearMonth=yearMonth) 
            downloadDict[yearMonth] = url #file name and URL
            self.currentMonth+=1
            if self.currentMonth > 12:
                self.currentMonth = 1
                self.currentYear+=1

        return downloadDict

    async def downloadFile(self, path, fileName, url, semaphore, retryIfError = True):
        async with semaphore:
            print('downloading: ' + fileName + '.csv')    
            
            try:     
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url) as resp:
                        response = await resp.read()
                        if resp.status == 200:
                            f = await aiofiles.open(path + fileName +'.csv', mode='wb')
                            await f.write(response)
                            await f.close() 
                            print(fileName + '.csv downloaded!')
                        else:
                            print(resp)   
            except Exception:
                print('Error downloading file: ' + fileName + '.csv')
                if retryIfError:
                    print('Trying to download again...')
                    await self.downloadFile(path, fileName, url, semaphore, False)
                else:
                    raise
