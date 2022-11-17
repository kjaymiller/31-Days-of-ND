from flask import (
        Flask,
        render_template,
        request,
)
import os
import json
from azure.storage.queue import QueueClient
from azqueuetweeter import storage, twitter


queue = QueueClient.from_connection_string(
        conn_str=os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
        queue_name=os.environ.get("AZURE_STORAGE_QUEUE_NAME")
)

try:
    queue.create_queue()
except:
    pass

def load_msg():
    return queue.receive_message().content
    

app = Flask(__name__)


@app.route('/')
def index():
    try:
        msg = load_msg()
    except:
        msg = "There is no message in the queue"
    return render_template('index.html', message=load_msg())

@app.route('/message', methods="POST")
def message():
    

if __name__ == '__main__':
    app.run() 