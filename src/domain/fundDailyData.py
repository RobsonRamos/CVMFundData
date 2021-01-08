from datetime import datetime

class FundDailyData:
    def __init__(self, taxId = None, quoteDate = None, portfolioValue = None, quoteValue = None, fundNetWorth = None, investments = None, withdrawals = None, numberOfInvestors = None, dailyReturn = None):
        
        if taxId is not None:
            self.taxId = taxId.replace('.', '').replace('/','').replace('-','')
        if quoteDate is not None:
            self.quoteDate = datetime.strptime(quoteDate,  "%Y-%m-%d")
        if portfolioValue is not None:
            self.portfolioValue = float(portfolioValue)
        if quoteValue is not None:
            self.quoteValue = float(quoteValue)
        if fundNetWorth is not None:
            self.fundNetWorth = float(fundNetWorth)
        if investments is not None:
            self.investments = float(investments)
        if withdrawals is not None:
            self.withdrawals = float(withdrawals)
        if numberOfInvestors is not None:
            self.numberOfInvestors = float(numberOfInvestors)
        if dailyReturn is not None:
            self.dailyReturn = dailyReturn
        else:
            self.dailyReturn = None
    
    def to_json(self):
        return { 
            "cnpj": self.taxId,
            "quoteDate": self.quoteDate,
            "portfolioValue" : self.portfolioValue,
            "quoteValue" : self.quoteValue,
            "fundNetWorth" : (self.fundNetWorth),
            "investments" : (self.investments),
            "withdrawals" : (self.withdrawals),
            "numberOfInvestors" : (self.numberOfInvestors),
            "dailyReturn" : (self.dailyReturn)
        }