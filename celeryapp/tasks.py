from celeryapp.celery import celapp
from beeline_api.rest_api import get_subscriptions
from celery.exceptions import MaxRetriesExceededError


@celapp.task(bind=True, default_retry_delay=1, max_retries=30)
def check_subscriptions(self, ctn, subscription_id):
    subscriptions, _ = get_subscriptions(ctn)
    ids = [subscription['id'] for subscription in subscriptions]
    try:
        if subscription_id in ids:
            self.retry()
        return 'Subscription ' + subscription_id + ' removed.'
    except MaxRetriesExceededError:
        raise MaxRetriesExceededError('Subscription ' + subscription_id + ' not removed.')
