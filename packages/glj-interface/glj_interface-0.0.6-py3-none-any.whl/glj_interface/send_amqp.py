#!/usr/bin/env python
import pika

class amqpsender:
     def glj_connect(username,password, ip_addr):
        user=username
        pw=password
        IP=ip_addr

        credentials = pika.PlainCredentials(user,pw)
        parameters = pika.ConnectionParameters(IP,
                                        5672,
                                        '/',
                                        credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()


    
    def gen_send(fname):  

        #credentials = pika.PlainCredentials('EndE','EndE')
        #parameters = pika.ConnectionParameters(IP,
                                        #5672,
                                        #'/',
                                        #credentials)

    
        #connection = pika.BlockingConnection(parameters)
        #channel = connection.channel()

        channel.queue_declare(queue='hello')
        i=1
        while True:
            ans= input("Send msg? :")
            message= "msg from End E " + str(i) +" " +str(fname)

            if ans == "":
                channel.basic_publish(exchange='', routing_key='hello', body=message)
                print(" [x] Sent Msg from EndE #",i, fname)
                i+=1
            else:
                break
        connection.close()

   


    def pose_req(json):  

        credentials = pika.PlainCredentials('EndE','EndE')
        parameters = pika.ConnectionParameters(IP,
                                        5672,
                                        '/',
                                        credentials)

    
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='hello')
        i=1
        while True:
            ans= input("Send msg? :")
            message= "msg from End E " + str(i) +" " +str(fname)

            if ans == "":
                channel.basic_publish(exchange='', routing_key='hello', body=message)
                print(" [x] Sent Msg from EndE #",i, fname)
                i+=1
            else:
                break
        connection.close()   