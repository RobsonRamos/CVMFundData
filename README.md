# CVM Data Funds

CVM Data Funds is a project to help you get historical funda data from the CVM (Brazilian SEC entity).


## How to

run
-------

.. code-block:: bash

   $ docker-compose build
   $ docker-compose up


execute the tests
-------

.. code-block:: bash

   $ cd src/
   $ python3 ...


## Using the API

When the ETL process finishs an API is exposed through the address ``localhost:5000/FundsDataService``

To use the API its necessary to inform the following parameters:
- cnpj: Mandatory parameter 
- startDate: Optional parameter (YYYY-MM-DD)
- endDate: Optional parameter (YYYY-MM-DD)

For example:
http://localhost:5000/FundsDataService?cnpj=00017024000153&startDate=2017-02-02&endDate=2019-02-10