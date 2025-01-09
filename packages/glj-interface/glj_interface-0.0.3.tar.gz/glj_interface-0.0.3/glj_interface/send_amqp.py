#!/usr/bin/env python
import pika

class amqpsender:
    def send_amqp_msg(fname):  

        credentials = pika.PlainCredentials('EndE','EndE')
        parameters = pika.ConnectionParameters('IP',
                                        5672,
                                        '/',
                                        credentials)

    
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
        print(" [x] Sent 'Hello World!'", fname)
        connection.close()