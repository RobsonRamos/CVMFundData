import traceback
from etl.dataLoader  import DataLoader
from api.startup import Startup

class App:
    try:
        loader = DataLoader()
        loader.loadData(startYear = 2017, startMonth = 1)

        startup = Startup()
        startup.startAPI()  
    except:
        traceback.print_exc()
        print("Looks like something went wrong :( ")
