Epic Events wants to develop a secure internal CRM system. The API allows sales representative to create and update their clients, contracts and events. A member of the support can update his events. Sales representative and members of the support have read access to all data.

You can find the documentation of this API by following this link : https://documenter.getpostman.com/view/22986696/2s83zdv6L8


User groups are managed by the management team in the django administration interface ("Sales" for sales representative and "Support" for support people)


## Clone of the repository

* git clone https://github.com/Herve-2476/OpenClassRoomsProject_12.git

* cd OpenClassRoomsProject_12


## Creation of the virtual environment (Python 3.10)
 
* python -m venv venv # or *python3 -m venv venv* 

* source venv/bin/activate *# to launch your environment under linux / Mac*

* venv\Scripts\activate.bat *# to launch your environment under windows*

* pip install -r requirements.txt # or *pip3 install -r requirements.txt*

## Creation of a local PostgreSQL database with the following parameters

* NAME = "mydb"
* USER = "myuser"
* PASSWORD = "mypass"
* HOST = "localhost"

## Running the program

* python manage.py runserver # or *python3 manage.py runserver* 

## Use of the program

* You can test the API with Postman, Django, curl... 

## Compliance with PEP 8 guidelines

* flake8 *# to create the HTML report*