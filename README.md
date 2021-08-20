# grad-proj-api
this repo is for our graduation project API\
graduation project is a movies recommendation android app\
you can view android app repo from [here](https://github.com/eslamalaaeddin/GraduationProject)\
### Run the server locally
1- you need to install [MySQL](https://www.mysql.com/) and [Neo4J](https://neo4j.com/) databases\
2- edit utils/config.py with your databases configurations\
3- install pipenv in your computer
```
pip install pipenv
```
4- open cmd in project folder and create new virtual environment (this step is required each timr you want to start the server)
```
pipenv shell
```
5- install dependencies
```
pipenv install
```
6- start the server
```
python app.py
```
the first time you start the server will take sometime to insert the initial data to databases
