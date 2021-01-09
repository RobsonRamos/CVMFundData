[![Tests Status] (https://github.com/RobsonRamos/CVMFundData/Workflows/action/badge.svg)]

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
   $ python3 ...

```

## Using the API

When the ETL process finishs an API is exposed through the address ``localhost:5000/FundsDataService``

To use the API its necessary to inform the following parameters:
- cnpj: Mandatory parameter 
- startDate: Optional parameter (YYYY-MM-DD)
- endDate: Optional parameter (YYYY-MM-DD)

For example:
http://localhost:5000/FundsDataService?cnpj=00017024000153&startDate=2017-02-02&endDate=2019-02-10
