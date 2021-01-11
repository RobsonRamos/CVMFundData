![Github Default Action](https://github.com/RobsonRamos/CVMFundData/workflows/Tests/badge.svg?branch=master)

# CVM Data Funds

CVM Data Funds is a project to help you get historical funda data from the CVM (Brazilian SEC entity).


## How to execute the code


```python
   $ docker-compose build
   $ docker-compose up
```

## How to execute the tests 

```python
   $ cd src/
   $ coverage run   -m unittest discover  -s ./tests && coverage

```

## Using the API

When the ETL process finishs an API is exposed in the address ``localhost:5000/FundsDataService``

To use the API its necessary to execute a GET request (using the address above) containing the following parameters:
- cnpj: Mandatory parameter 
- startDate: Optional parameter (YYYY-MM-DD)
- endDate: Optional parameter (YYYY-MM-DD)

### Sample request
http://localhost:5000/FundsDataService?cnpj=00017024000153&startDate=2017-02-02&endDate=2019-02-10

###  

The API returns an object **result** containing the following informations:


 Field  | Description
 ------ |   ---------------
 cnpj  | Unique identifier of a fund
 quoteDate  | date of record 
 portfolioValue   | Total value of portfolio (NAV in BRL)
 quoteValue   | Quote value
 fundNetWorth  | Fund net worth (BRL)
 investments  | Total investments of the day (BRL)
 withdrawals  | Total withdrawals of the day (BRL)
 numberOfInvestors  | Number of investors 
 dailyReturn  | (quote(t) / quote(t-1)) -1 

