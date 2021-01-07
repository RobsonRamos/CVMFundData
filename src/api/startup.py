from flask import Flask
from flask_restful import Resource, Api, reqparse 
from datetime import datetime 
import sys  
sys.path.append('./api/')
from fundDataService import FundDataService

class Startup: 

        def startAPI(self): 
                app = Flask(__name__)
                api = Api(app)
                api.add_resource(FundDataService, '/FundsDataService')  
                app.run(debug=False, port=5000, host='0.0.0.0')