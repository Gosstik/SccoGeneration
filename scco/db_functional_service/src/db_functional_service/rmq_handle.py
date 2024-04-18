from typing import Callable

import pika
from pika.adapters.blocking_connection import (
    BlockingConnection,
    BlockingChannel,
)
from pika.channel import Channel

import util.parse_env as pe
from util.json_handle import dict_get_or_panic

# Getting environment variables.

if not pe.is_on_host():
    # RMQ_NET_ALIAS = "scco_rmq_rabbitmq"
    RMQ_NET_ALIAS = pe.get("RMQ_NET_ALIAS")
    DB_FUNCTIONAL_SERVICE_NET_ALIAS = pe.get("DB_FUNCTIONAL_SERVICE_NET_ALIAS")
    DB_FUNCTIONAL_SERVICE_EXCHANGE = pe.get("DB_FUNCTIONAL_SERVICE_EXCHANGE")
    DB_FUNCTIONAL_SERVICE_QUEUE = pe.get("DB_FUNCTIONAL_SERVICE_QUEUE")
    DB_FUNCTIONAL_SERVICE_ROUTING_KEY = pe.get("DB_FUNCTIONAL_SERVICE_ROUTING_KEY")


class Reply:
    def __init__(self, srv_req_data: dict):
        if "reply" not in srv_req_data:
            self.reply_not_required = True
            return
        else:
            self.reply_not_required = False

        reply = srv_req_data["reply"]
        self.exchange = dict_get_or_panic(reply, "exchange", srv_req_data)
        self.routing_key = dict_get_or_panic(reply, "routing_key", srv_req_data)


class RmqHandle:
    conn: BlockingConnection = None
    chan: BlockingChannel = None
    callback: Callable = None

    @classmethod
    def _create_channel(cls):
        # RMQ_NET_ALIAS = "localhost" # working with port passing
        # RMQ_NET_ALIAS = "rabbitmq"
        # RMQ_NET_ALIAS = "rabbitmq_alias"
        print("BEFORE pika.BlockingConnection")
        cls.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=RMQ_NET_ALIAS)
        )
        print("AFTER pika.BlockingConnection")
        cls.chan = cls.conn.channel()
        print("HERE")

    @classmethod
    def _declare_exchange(cls):
        cls.chan.exchange_declare(
            exchange=DB_FUNCTIONAL_SERVICE_EXCHANGE,
            exchange_type='topic',
        )

    @classmethod
    def _declare_publish_queue(cls):
        pass

    @classmethod
    def _declare_consumer_queue(cls):
        # generated_offers queue.
        cls.chan.queue_declare(
            queue=DB_FUNCTIONAL_SERVICE_QUEUE
        )
        cls.chan.queue_bind(
            exchange=DB_FUNCTIONAL_SERVICE_EXCHANGE,
            queue=DB_FUNCTIONAL_SERVICE_QUEUE,
            routing_key=DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
        )
        cls.chan.basic_consume(
            queue=DB_FUNCTIONAL_SERVICE_QUEUE,
            on_message_callback=cls.callback,
        )

    @classmethod
    def setup_rmq(cls, callback):
        cls.callback = callback

        print("0")
        cls._create_channel()
        print("1")
        cls._declare_exchange()
        print("2")
        cls._declare_consumer_queue()
        print("3")

    @classmethod
    def start_consume(cls):
        cls.chan.start_consuming()  # Infinite loop.

    @classmethod
    def basic_publish(cls, answer: str, reply: Reply):
        if reply.reply_not_required:
            return

        body = answer.encode("utf-8")
        cls.chan.basic_publish(
            exchange=reply.exchange,
            routing_key=reply.routing_key,
            body=body,
        )
