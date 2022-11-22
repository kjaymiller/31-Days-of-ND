from flask import (
        Flask,
        render_template,
        flash,
)
import json

from uuid import uuid4

from .messages import get_messages, get_message
from .queue import queue as q
from .form import AddMessage

try:
    q.queue.create_queue()
except:
    pass


app = Flask(__name__)
app.secret_key = str(uuid4())

@app.route('/')
def index():
    msg = get_messages(queue = q.queue)
    form = AddMessage()
    return render_template('index.html', msgs=msg, form=form)


@app.route('/send/<message_id>', methods=['POST'])
def tweet(message_id):
    get_message(id=message_id, queue=q.queue)
    q.send_next_message(
        message_transformer=lambda msg: {"text": json.loads(msg)['msg']},
        delete_after=True,
        )
    msgs = get_messages(queue=q.queue)
    form=AddMessage()
    return render_template('message.html', msgs=msgs, form=form)


@app.route('/message', methods=["POST"])
def add_message():
    form = AddMessage()

    if form.validate_on_submit():
        q.queue_message(json.dumps({
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
    q.queue.clear_messages()
    flash("Queue Cleared", "success")
    form = AddMessage()
    msgs = get_messages()
    return render_template('message.html', msgs=msgs, form=form)

if __name__ == '__main__':
    app.run() 