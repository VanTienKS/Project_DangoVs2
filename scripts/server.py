import socket
import pickle
import pygame

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
        'pos': pygame.math.Vector2(1700, 1000),
        'status': 'down_idle',
        'frame_index': 1,
        'selected_tool': 'axe',
        'selected_seed': 'tomato',
        'sleep': False,
    },
    'player2': {
        'name': 'Tien Dat',
        'pos': pygame.math.Vector2(1500, 1900),
        'status': 'left_idle',
        'frame_index': 1,
        'selected_tool': 'hoe',
        'selected_seed': 'tomato',
        'sleep': False,
    },
    'start_color': [255, 255, 255],
}

currentPlayer = 0


def thread_client(conn, currentplayer):
    send_data = {
        'player1': server_data['player1' if currentplayer == 1 else 'player2'],
        'player2': server_data['player2' if currentplayer == 1 else 'player1'],
        'start_color': server_data['start_color']
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
                
            send_data = {
                'player2': server_data['player2' if currentplayer == 1 else 'player1'],
                'start_color': server_data['start_color']
            }
            print("Received: ", receive_data)
            print("Send: ", send_data)
            
            conn.send(pickle.dumps(send_data))
        except:
            break

    global currentPlayer
    currentPlayer = max(0, currentPlayer - 1)
    print(currentPlayer)


while True:
    conn, addr = socket_server.accept()
    print("Connect to: ", addr)
    currentPlayer = (currentPlayer + 1) % 2
    start_new_thread(thread_client, (conn, currentPlayer))
