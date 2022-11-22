from azure.storage.queue import QueueClient
import json


def message_loader(message):
    """Loads a message from the queue"""
    return json.loads(message.content)


def get_messages(queue: QueueClient, count:int=10):
    """Creates a List of the last <COUNT> messages in the queue"""

    msgs = [{'id':msg['id'], "content":message_loader(msg)} for msg in queue.peek_messages(max_messages=count)]
    return msgs

def get_message(id, max_tries=20):

    message = queue.queue.peek_messages()[0]
    attempt = 0

    while message.id != id or attempt < max_tries:
        message = queue.queue.peek_messages()[0]

        if message.id == id:
            return message

        attempt += 1
        message = queue.queue.receive_message(visibility_timeout=1)
