from flask_restful import Resource, Api, reqparse
from flask import jsonify, Response, request
import json 
import traceback
from datetime import datetime
import sys
sys.path.append('./data/')
sys.path.append('./domain/')
from  database import Database
from fundDailyDataQuery import FundDailyDataQuery

class FundDataService(Resource):

    def datetime_handler(self, x):
        if isinstance(x, datetime):
            return x.isoformat()
        raise TypeError("Unknown type") 

    def get(self):

        try:
            cnpj = request.args.get('cnpj')
            startDate = request.args.get('startDate')
            endDate = request.args.get('endDate')
            query = FundDailyDataQuery(cnpj)
            
            if startDate is not None:
                query.startDate = datetime.strptime(startDate, '%Y-%m-%d')

            if endDate is not None:
                query.endDate = datetime.strptime(endDate, '%Y-%m-%d')
            
            if cnpj is not None:
                database = Database()
                data = database.getData(query)  
                return Response(response=json.dumps(data, default=self.datetime_handler),
                            status=200,
                            mimetype='application/json')
            else:
                return Response(response="The field cnpj is required", status=400)
         
        except:
            traceback.print_exc()
            return Response(response="Internal server error", status=500)