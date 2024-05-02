import socket
import pickle
import pygame
from random import randint

from _thread import start_new_thread
from pytmx.util_pygame import load_pygame


socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.gethostbyname(socket.gethostname())
port = 12345

try:
    socket_server.bind((server, port))
except socket.error as e:
    print(e)

socket_server.listen(2)
print("Server waiting for connection")

server_data = {
    'player1': {
        'name': 'Van Tien',
        'pos': pygame.math.Vector2(600, 300),
        'status': 'down_idle',
        'frame_index': 1,
        'selected_tool': 'axe',
        'selected_seed': 'tomato',
        'sleep': False,
        'item_inventory': {
            'wood': 10,
            'apple': 4,
            'corn': 8,
            'tomato': 20,
        },
        'seed_inventory': {
            'corn': 35,
            'tomato': 35,
        },
        'money': 100,
        'has_use_seed': False,
    },
    'player2': {
        'name': 'Tien Dat',
        'pos': pygame.math.Vector2(1500, 1900),
        'status': 'left_idle',
        'frame_index': 1,
        'selected_tool': 'hoe',
        'selected_seed': 'tomato',
        'sleep': False,
        'item_inventory': {
            'wood': 77,
            'apple': 7,
            'corn': 10,
            'tomato': 4,
        },
        'seed_inventory': {
            'corn': 15,
            'tomato': 25,
        },
        'money': 200,
        'has_use_seed': False,
    },
    
    'start_color': [255, 255, 255],
    'chat': ['eee', 'ewe', 'wwew'],
    'rain': randint(0,20) > 10,
}

currentPlayer = 0

def thread_client(conn, currentplayer):
    send_data = {
        'player1': server_data['player1' if currentplayer == 1 else 'player2'],
        'player2': server_data['player2' if currentplayer == 1 else 'player1'],
        'start_color': server_data['start_color'],
        'chat': server_data['chat'],
        'rain': server_data['rain'],
    }
    conn.send(pickle.dumps(send_data))

    while True:
        try:
            receive_data = pickle.loads(conn.recv(4096))
            if not receive_data:
                print('Disconnected')
                break
            else:
                server_data['player1' if currentplayer == 1 else 'player2'] = receive_data['player1']
                server_data['start_color'] = receive_data['start_color']
                if len(receive_data['chat']) > 0:
                    server_data['chat'] = receive_data['chat']
                if receive_data['rain'] is not None:
                    server_data['rain'] = receive_data['rain']
                
            send_data = {
                'player2': server_data['player2' if currentplayer == 1 else 'player1'],
                'start_color': server_data['start_color'],
                'chat': server_data['chat'],
                'rain': server_data['rain'],
                
            }
            print("Received: ", receive_data['player1']['name'], receive_data['player1']['has_use_seed'])
            print("Send: ", send_data['player2']['name'], send_data['player2']['has_use_seed'])
            
            conn.send(pickle.dumps(send_data))
        except:
            break

    global currentPlayer
    currentPlayer = max(0, currentPlayer - 1)
    print(currentPlayer)


while True:
    # block code
    conn, addr = socket_server.accept()
    print("Connect to: ", addr)
    currentPlayer = (currentPlayer + 1) % 2
    start_new_thread(thread_client, (conn, currentPlayer))

# currentPlayer = 'player2'

# def thread_client(conn, currentplayer):
#     send_data = {
#         'player1': server_data['player1' if currentplayer == 'player1' else 'player2'],
#         'player2': server_data['player2' if currentplayer == 'player1' else 'player1'],
#         'start_color': server_data['start_color']
#     }
#     conn.send(pickle.dumps(send_data))

#     while True:
#         try:
#             receive_data = pickle.loads(conn.recv(4096))
#             if not receive_data:
#                 print('Disconnected')
#                 break
#             else:
#                 server_data['player1' if currentplayer == 'player1' else 'player2'] = receive_data['player1']
#                 server_data['start_color'] = receive_data['start_color']
                
#             send_data = {
#                 'player2': server_data['player2' if currentplayer == 'player1' else 'player1'],
#                 'start_color': server_data['start_color']
#             }
#             print("Received: ", receive_data)
#             print("Send: ", send_data)
            
#             conn.send(pickle.dumps(send_data))
#         except:
#             break

#     # global currentPlayer
#     # currentPlayer = max(0, currentPlayer - 1)
#     # print(currentPlayer)


# while True:
#     conn, addr = socket_server.accept()
#     print("Connect to: ", addr)
#     currentPlayer = 'player1' if currentPlayer == 'player2' else 'player2'
#     start_new_thread(thread_client, (conn, currentPlayer))
