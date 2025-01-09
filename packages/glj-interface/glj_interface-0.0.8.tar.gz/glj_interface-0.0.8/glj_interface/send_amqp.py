#!/usr/bin/env python
import pika
import json

class amqpsender: 
    def gen_send(payload):  
        credentials = pika.PlainCredentials(payload["user"],payload["pw"])
        parameters = pika.ConnectionParameters(payload["ip_addr"],
                                        5672,
                                        '/',
                                        credentials)

    
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='hello')
        i=1

        while True:
            ans= input("Send msg? :")
            message=json.dumps(payload)

            if ans == "":
                channel.basic_publish(exchange='', routing_key='hello', body=message)
                print(" [x] Sent Msg from EndE #",i, fname)
                i+=1
            else:
                break
        connection.close()

   


    