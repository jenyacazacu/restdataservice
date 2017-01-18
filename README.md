# Python REST API Data Service
This project is a Restful API built with Django, Django Rest Framework, pandas, celery and redis. The intended use is for aggregating on a column/key from an uploaded file. 

The endpoints and their functionality:

- <strong>/api/datafile</strong>: Accepts a file upload (.json)
- <strong>/api/aggregate</strong>: given a  fileid and column name from the uploaded file, it will try to aggregate that column, will only return a result if that column is numeric

<strong>Requires</strong>: PostgreSQL, Redis ( you can find installation instructions online)<br>

<strong>Steps to run this locally</strong>:

1. go to root directory of the repo
2. install a virtulenv and activate it

  virtualenv your_env <br> 
  source your_env/bin/activate
  
3. pip install requirements.txt
4. modify the settings.py file database user with the user that you created in PostgreSQL
5. run with ./manage.py runserver
6. You are done!

<strong>Tests</strong> are included and can be run with: ./manage.py test

<strong>API Docs</strong> are powered by <a href="http://drfdocs.com/" target="_blank">DRF Docs</a> and can be accessed locally if you go to <a href="http://localhost:8000/api/docs/" target="_blank">http://localhost:8000/api/docs/</a>
