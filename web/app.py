from datetime import datetime
from flask import (
        Flask,
        render_template,
        flash,
)
from flask_wtf import FlaskForm
from wtforms import (
        TextAreaField,
        DateTimeLocalField,
)

import os
import json

from azure.storage.queue import QueueClient
from azqueuetweeter import storage, twitter, QueueTweeter
from uuid import uuid4

from .messages import get_messages, get_message


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


class AddMessage(FlaskForm):
    msg = TextAreaField(
            "Message",
            render_kw={"style": "width:100%"},
    )
    date = DateTimeLocalField(
            "Send At",
            default=datetime.now(),
            format='%Y-%m-%dT%H:%M',
    )
    

app = Flask(__name__)
app.secret_key = str(uuid4())

@app.route('/')
def index():
    msg = get_messages()
    form = AddMessage()
    return render_template('index.html', msgs=msg, form=form)


@app.route('/send/<message_id>', methods=['POST'])
def tweet(message_id):
    get_message(message_id)
    queue.send_next_message(
        message_transformer=lambda msg: {"text": json.loads(msg)['msg']},
        delete_after=True,
        )
    msgs = get_messages()
    form=AddMessage()
    return render_template('message.html', msgs=msgs, form=form)


@app.route('/message', methods=["POST"])
def add_message():
    form = AddMessage()

    if form.validate_on_submit():
        queue.queue_message(json.dumps({
                "msg": form.msg.data,
                "date": form.date.data.isoformat()
                })
        )
        flash("Message Queued", "success")
    else:
        for error in form.errors:
            flash(error, "error")

    msgs = get_messages()
    return render_template('message.html', msgs=msgs, form=form)

@app.route('/clear', methods=["POST"])
def clear():
    queue.queue.clear_messages()
    flash("Queue Cleared", "success")
    form = AddMessage()
    msgs = get_messages()
    return render_template('message.html', msgs=msgs, form=form)

if __name__ == '__main__':
    app.run() 