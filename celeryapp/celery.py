from celery import Celery

# app = Celery('tasks')
celapp = Celery('celeryapp',
              include=['celeryapp.tasks'])
celapp.config_from_object('celeryapp.celeryconfig')
celapp.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    celapp.start()
