# /
#   data/
#       providers/
#           hermes_socket.py
#           hermes_encryption.py
#           hermes_notify.py
#           hermes_clipboard.py
#       confg/
#           hermes.json
#   main.py

# {
#     "app":{
#         "name":"Hermes",
#         "codename":"monika.hermes",
#         "version":"0.0.1",
#         "description":"Hermes is a simple, fast, and secure communication platform for the desktop devices.",
#         "author":"Ismael P. Santana",
#         "license":"none",
#         "icon":"resources/icon.ico"
#     },
#     "providers":{
#         "socket":{
#             "sender":{
#                 "host":"192.168.0.1",
#                 "port":161201
#             },
#             "receiver":{
#                 "port":161202
#             }
#         },
#         "notification":{
#             "type":"toast",
#             "timeout":4
#         },
#         "encryption":{
#             "key":"1234567890123456"
#         }
#     }
# }

import json
import os
import keyboard

config_hermes_path = os.getcwd() + "/data/config/hermes.json"

with open(config_hermes_path, "r") as my_file:
    hermes = json.load(my_file)
    app_name = hermes['app']['name']
    # app_icon = hermes['app']['icon']
    app_icon = ''
    providers_socket_receiver_port = hermes['providers']['socket']['receiver']['port']
    providers_socket_sender_host = hermes['providers']['socket']['sender']['host']
    providers_socket_sender_port = hermes['providers']['socket']['sender']['port']
    providers_notification_type = hermes['providers']['notification']['type']
    providers_notification_timeout = hermes['providers']['notification']['timeout']
    providers_encryption_key = hermes['providers']['encryption']['key']
    my_file.close()

import data.providers.hermes_socket as hermes_socket
import data.providers.hermes_notify as hermes_notify
import data.providers.hermes_clipboard as hermes_clipboard
import data.providers.hermes_encryption as hermes_encryption

import threading
from time import sleep

my_ip = hermes_socket.get_hostname()
my_port = providers_socket_receiver_port
my_key = providers_encryption_key
our_ip = providers_socket_sender_host
our_port = providers_socket_sender_port

if providers_notification_type == 'toast':
    my_notify_toast = True

print('my_ip: ' + my_ip)
print('my_port: ' + str(my_port))
print('our_port: ' + str(our_port))
print('our_ip: ' + our_ip)

def getter_thread():
    while True:
        try:
            my_socket = hermes_socket.Server(my_ip, my_port)
            my_socket.accept()
            print('Servidor: Recibiendo...')
            my_message = my_socket.receive()
            if my_message != '':
                my_message = hermes_encryption.decrypt(my_message, my_key)
                if my_message != hermes_clipboard.get():
                    hermes_clipboard.set(my_message)
                    hermes_clipboard.set(my_message)
            my_socket.close()
        except:
            my_socket.close()

def setter_thread():
    while True:
        try:
            # Check ctrl + c
            if keyboard.is_pressed('ctrl+c'):
                my_socket = hermes_socket.Client(our_ip, our_port)
                print('Cliente: Enviando...')
                my_message = hermes_encryption.encrypt(hermes_clipboard.get(), my_key)
                my_socket.send(my_message)
                my_socket.close()
        except:
            my_socket.close()

my_threads = []

def main():
    try:
        # sleep(5)
        my_thread_getter = threading.Thread(target=getter_thread)
        my_thread_setter = threading.Thread(target=setter_thread)
        my_thread_getter.start()
        my_thread_setter.start()
        my_threads.append(my_thread_getter)
        my_threads.append(my_thread_setter)
        hermes_notify.notify(
            my_title=app_name,
            my_message='Todo listo para comenzar.',
            my_app_name=app_name,
            my_timeout=providers_notification_timeout,
            my_icon=app_icon,
            my_toast=my_notify_toast
        )
    except:
        for my_thread in my_threads:
            my_thread.join()

try:
    main()
except:
    hermes_notify.notify(
        my_title=app_name,
        my_message='Error inesperado.',
        my_app_name=app_name,
        my_timeout=providers_notification_timeout,
        my_icon=app_icon,
        my_toast=my_notify_toast
    )