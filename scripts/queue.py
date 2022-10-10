import json
import pika

d = {}
with open("add") as f:
    d = {k: v for line in f for (k, v) in [line.strip().split(None, 1)]}


def send(j, k):
    credentials = pika.PlainCredentials('micro', 'micro')
    parameters = pika.ConnectionParameters('10.51.89.44',
                                           5672,
                                           '/',
                                           credentials)
    body = json.dumps({
        "donor": {
            "accountId": j
        },
        "acceptors": [
            {
                "accountId": k
            }
        ],
        "deletedMembers": [
            {
                "accountId": k
            }
        ],
        "blockRequired": False
    })

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)

    channel.basic_publish(exchange='', routing_key='hello', properties=pika.BasicProperties(
        headers={'event': 'ALLIN',
                 'entity': 'GROUP_DISCOUNT',
                 'operation': 'CHANGE'}
    ), body=body)
    print(" [x] Sent 'Hello RabbitMQ!'")
    connection.close()


for i in d:
    send(i, d[i])
