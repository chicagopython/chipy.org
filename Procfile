web: gunicorn chipy_org.wsgi --pythonpath chipy_org --log-file -

worker: python manage.py rqworker high default low