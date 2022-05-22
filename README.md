# Fleo
###### It is an emulation of Tata Steel Sale Status management system.

## Technology Stack:
### Backend
* #### Django(Python3)

### Database
* #### SQLite
  ###### It is used(which comes bundled with Django). This is only used for development purpose and a more powerful datatbase should be used in production.

## How to Use?
* Create a python3 virtual environment, navigate to project directory on terminal and install dependencies(listed in requirements.txt file) using the command
`pip install requirements.txt` <br>
RUN `python manage.py makemigrations` and `python manage.py migrate` <br>to create tables in database. <br>
To run server, use command `python manage.py runserver`

* Open a browser and navigate to <b>localhost:8000</b> for FlameServer1 or <b>localhost:8000/flam2</b> for FlameServer2.

* http://localhost:8000/category/  `Categories Api (ViewSets)` <br>
  http://localhost:8000/category/<int:pk>/level/<int:level>/  `To Retrieve the category details along with the n-th level child` <br>
  http://localhost:8000/get-parents/<int:pk>/  `to Get the related parents for a category` <br>
  http://localhost:8000/delete-category-without-child/<int:pk>/  `For deleting category without deleting the child` <br>
