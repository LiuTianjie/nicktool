import os.path

import pika
import yaml


class ImageTaskProducer:
    yamlPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../config.yaml")
    f = open(yamlPath, 'r', encoding='utf-8')
    rconfig = yaml.load(f.read(), Loader=yaml.FullLoader)["rabbitmq"]
    f.close()
    username = rconfig["username"]
    password = rconfig["password"]
    host = rconfig["host"]
    port = rconfig["port"]
    credentials = pika.PlainCredentials(username, password)
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials))
    channel = conn.channel()
    channel.queue_declare(queue="image_task", durable=True)
    channel.queue_bind(exchange="direct", queue="image_task", routing_key="image_task")
    channel.exchange_declare(exchange="direct", exchange_type="direct")

    @staticmethod
    def publish(message):
        ImageTaskProducer.channel.basic_publish(exchange="direct", routing_key="image_task", body=message)
