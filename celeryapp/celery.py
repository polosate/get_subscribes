from celery import Celery

# app = Celery('tasks')
app = Celery('celeryapp',
              include=['celeryapp.tasks'])
app.config_from_object('celeryapp.celeryconfig')
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
