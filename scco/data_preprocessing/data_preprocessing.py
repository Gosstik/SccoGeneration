import json
import os
import pandas as pd
import pika
import sys

import config
from pipeline import PreprocessingPipeline
from rabbit_rpc import FilterRpcClient


class Preprocessor:
    def __init__(self):
        print(" [*] Initializing Preprocessor", flush=True)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.RABBIT_ADDRESS))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=config.IN_QUEUE, durable=True)
        self.channel.queue_declare(queue=config.OUT_QUEUE, durable=True)

        self.filter_rpc_client = FilterRpcClient(self.connection, self.channel)

        self.new_queries_csv_info = {'path': None}

        self.channel.basic_consume(queue=config.IN_QUEUE,
                                   on_message_callback=self.on_message_received)

    def start(self):
        print(" [*] Waiting for messages. To exit press CTRL+C", flush=True)
        self.channel.start_consuming()

    def on_message_received(self, ch, method, properties, body):
        print(f" [x] Received {body}", flush=True)

        try:
            json_in = json.loads(body.decode())

            data = pd.read_csv(json_in['parsed_csv'])
            data.columns = ['channel_id', 'client_id', 'message', 'message_date']
            customer_id = json_in['customer_id']
        except Exception as e:
            print(" [x] Caught the following exception when parsing input:")
            print(e)
            print(" [x] Sending ack, continue listening", flush=True)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        pipeline = PreprocessingPipeline(customer_id=customer_id)
        data = pipeline(data)
        if data.empty:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        print(f" [x] Sending {len(data)} messages")
        with open('/data/new_queries/out.txt', 'w') as f:
            for index, row in data.iterrows():
                json_str = json.dumps({col: str(row[col]) for col in data.columns})
                # self.send_message(ch, json_str)
                print(json_str, file=f)
        print(" [x] Done", flush=True)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def send_message(slef, channel, body):
        channel.basic_publish(exchange=config.ML_GENERATION_EXCHANGE,
                              routing_key=config.ML_GENERATION_ROUTING_KEY,
                              body=body,
                              properties=pika.BasicProperties(
                                  delivery_mode=pika.DeliveryMode.Persistent
                              ))


try:
    Preprocessor().start()
except KeyboardInterrupt:
    print("Interrupted")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
