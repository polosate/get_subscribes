broker_url = 'pyamqp://guest@localhost//'
result_backend = 'amqp'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json', 'pickle']
timezone = 'Europe/Oslo'
enable_utc = True

# CELERY_RESULT_SERIALIZER = ['json', 'pickle'] #json pickle msgpack
# CELERY_TASK_SERIALIZER = ['json', 'pickle']
# CELERY_ACCEPT_CONTENT = ['json', 'pickle']
