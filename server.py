import socket
import threading
import random
import pickle
import time
from TTTManager import *
from Board import *

HOST = ''
PORT = 5555
server = socket.socket()
server.bind((HOST, PORT))
print("[RUNNING] Server is up and running")

HOST_LOGIN = ''
PORT_LOGIN = 5556
connection_to_login_server = socket.socket()
connection_to_login_server.bind((HOST, PORT_LOGIN))
print("[RUNNING] Login Server is up and running")

logged_in_ids = []

def send_board_to_players(board, player_1, player_2):
    current_board = board.get_board()
    player_1.send(current_board.encode())
    player_2.send(current_board.encode())

def send_game_state_to_players(board, player_1, player_2):
    game_state = board.check_board_state()
    player_1.send(game_state.encode())
    player_2.send(game_state.encode())

def run_game(player_1, player_2):
    board = Board()

    current_player = random.choice([player_1, player_2])
    opponent = player_1 if current_player is player_2 else player_2
    current_player.send("FIRST".encode())
    opponent.send("SECOND".encode())

    if board.check_board_state() == "NO_RESULT":
        while True:
            time.sleep(0.5)
            current_player.send("MOVE".encode())
            opponent.send("WAIT_MOVE".encode())
            send_board_to_players(board, player_1, player_2)

            data = current_player.recv(1024)
            tile, tile_type = pickle.loads(data)
        
            if board.check_tile(tile):
                board.set_tile(tile, tile_type)
            else:
                break #TODO: add error handling - disconnect client if false
            
            send_board_to_players(board, player_1, player_2)
            time.sleep(0.5)

            send_game_state_to_players(board, player_1, player_2)

            current_player, opponent = opponent, current_player
    else:
        player_1.send("GAME_OVER".encode())
        player_2.send("GAME_OVER".encode())
        player_1.close()
        player_2.close()


def main_game_server():
    active_players = []
    while True:
        server.listen()

        client_socket, client_address = server.accept()
        print(f"[CONNECTION] {client_address}")
        active_players.append(client_socket)

        player_random_id = client_socket.recv(1024).decode()
        if player_random_id not in logged_in_ids:
            client_socket.close()
        
        if len(active_players) > 1:
            game = threading.Thread(target=run_game, args=(active_players[0], active_players[1]))
            active_players = active_players[2:]

            game.start()

def login_server():
    connection_to_login_server.listen()
    client, address = connection_to_login_server.accept()
    while True:
        random_id = client.recv(1024).decode()
        logged_in_ids.append(random_id)

main_game_server_running = threading.Thread(target=main_game_server)
login_server_running = threading.Thread(target=login_server)

main_game_server_running.start()
login_server_running.start()


    