class FundDailyDataQuery:
     def __init__(self, cnpj, startDate = None, endDate = None):
        self.cnpj = cnpj
        self.startDate = startDate
        self.endDate = endDate