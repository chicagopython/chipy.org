web: gunicorn chipy_org.wsgi --pythonpath chipy_org --log-file -

worker: python chipy_org/manage.py rqworker high default low