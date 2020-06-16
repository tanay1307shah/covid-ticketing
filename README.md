# RESTAPI Demo

### Prerequisite: 
1. [Python 3.x](https://www.python.org/downloads/)
2. [Pip](https://pip.pypa.io/en/stable/installing/)

### How to run

1. Clone this project.
2. Run ```pip install requirements.txt```. Requirements file has all the necessary modules that needs to be installed on your machine to run the app.
3. Server folder has the backend api code. You can refer to ```products()``` method in ```/server/backend.py``` to see how ```localhost:5000/products``` url works.
4. This method checks the the type of request(GET, POST, DELETE) made with ```/products``` url and respond accordingly. Check comments in server code for more details.
5. To run the api server open a terminal/cmd and run command ```python backend.py```
6. Now go to ```http://localhost:5000``` to access the home page.
7. The homepage html code is in ```client/home.html``` has 3 buttons which lets Add, View or Delete content from the mlab test db. 
8. Play with the app to Add, Delete and Read products from mlab test DB. You don't have to do anything specific for the db setup.
9. You can input a non empty value for ```Product name``` and ```Product price``` input boxes. Click on ```Add``` it to the test mlab db.
10. Click on ```View all``` to check the recently added content into mlab db. Similarly clicking on ```Delete all``` delete all the contents.

### Note

To generate requirements.txt I have used ```pipreqs``` module. You can run
```
   1. pip install pipreqs
   2. pipreqs -r <absolute-path-to-project-backend-folder> 
```
In this project this file is already created and stored in ```/server``` folder.
