import logging
from datetime import datetime

import azure.functions as func
from azqueuetweeter import storage, twitter, QueueTweeter

sa = storage.Auth(
        connection_string=os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
        queue_name=os.environ.get("AZURE_STORAGE_QUEUE_NAME")
)

ta = twitter.Auth(
    consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
)

queue = QueueTweeter(storage_auth=sa, twitter_auth=ta)

try:
    queue.queue.create_queue()
except:
    pass

def tweet_is_ready():
    if queue.queue.peek_messages():
        message = json.loads(queue.queue.peek_messages()[0].content)

        if datetime.now() >= datetime.fromisoformat(message['date']):
            return True


def send_tweet():
    queue.send_next_message(
        message_transformer=lambda x: {"text": json.loads(x)['msg']},
        delete_after=True,
        )
    msgs = get_messages()
    form=AddMessage()
    return render_template('message.html', msgs=msgs, form=form)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if tweet_is_ready():
        send_tweet()

    response = {
        "status": "200",
        "message": f"Tweet sent {msg}"
    }

    return func.HttpResponse(json.dumps(response), mimetype="application/json")
