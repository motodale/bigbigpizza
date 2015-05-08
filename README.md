# bigbigpizza
software engineering app for class

clone this and navigate to the directory.


To run this app, install python flask. This is required and it will require python to
be installed. From a terminal run:
```
pip install flask
```

Navigate to this project directory and type "python" in your terminal.
This will open a python shell, from there type following one line at a time:
```
from pizza import init_db
init_db()
```
this will create the database for sqlite

next cd into project and then type: 
```
./manage.py runserver
```

then in a browser go to
```
http://localhost:5000
```
