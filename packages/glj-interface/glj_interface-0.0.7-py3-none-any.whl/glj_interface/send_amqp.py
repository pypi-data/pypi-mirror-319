#!/usr/bin/env python
import pika
import json

class amqpsender: 
    def gen_send(payload):  
        data=json.loads(payload)    
        credentials = pika.PlainCredentials(data["user"],data["pw"])
        parameters = pika.ConnectionParameters(data["ip_addr"],
                                        5672,
                                        '/',
                                        credentials)

    
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='hello')
        i=1

        while True:
            ans= input("Send msg? :")
            message= json.loads(body.decode('utf-8'))

            if ans == "":
                channel.basic_publish(exchange='', routing_key='hello', body=message)
                print(" [x] Sent Msg from EndE #",i, fname)
                i+=1
            else:
                break
        connection.close()

   


    