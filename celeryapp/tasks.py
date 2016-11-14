from celeryapp.celery import app
from beeline_api.rest_api import get_subscriptions
from celery.exceptions import MaxRetriesExceededError

@app.task(bind=True, default_retry_delay=1, max_retries=200)
def check_subscriptions(self, beeline_token, ctn, subscription_id):
    subscriptions, _ = get_subscriptions(beeline_token, ctn)
    print(subscription_id)
    ids = [subscription['id'] for subscription in subscriptions]
    print(ids)
    try:
        if  subscription_id not in ids:
            return 'Subscription ' + subscription_id + ' removed!!!'
        else:
            self.retry()
    except MaxRetriesExceededError:
        return 'Subscription ' + subscription_id +' not removed!!!'
