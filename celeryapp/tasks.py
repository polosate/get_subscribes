from celeryapp.celery import celapp
from beeline_api.rest_api import get_subscriptions
from celery.exceptions import MaxRetriesExceededError


@celapp.task(bind=True, default_retry_delay=1, max_retries=60)
def check_subscriptions(self, db, ctn, subscription_id, uesr_id):
    task = Tasks.query.filter_by(task_id=self.request.id)
    if not task:
        task = Task(task_id=self.request.id, subscription_id=subscription_id, user_id=user_id, status=self.request.state)
        db.session.add(task)
        db.session.commit()
    else:
        task.status = self.request.state

    subscriptions, _ = get_subscriptions(ctn)
    ids = [subscription['id'] for subscription in subscriptions]
    try:
        if  subscription_id not in ids:
            db.session.delete(task)
            db.session.commit()
            return 'Subscription ' + subscription_id + ' removed!!!'
        else:
            self.retry()
    except MaxRetriesExceededError:
        task.status = self.request.state
        db.session.commit()
        raise MaxRetriesExceededError('Subscription ' + subscription_id +' not removed!!!')
