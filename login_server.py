import sqlite3
import hashlib
import socket
import json
import random
import threading

HOST = ''
PORT = 5557
server = socket.socket()
server.bind((HOST, PORT))

connection_to_game_server = socket.socket()
connection_to_game_server.connect(('192.168.68.104', 5556))

con = sqlite3.connect("userdata.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users
            (username text PRIMARY KEY, password text)''')

def generate_random_number():
    return random.randint(1, 10000000000000)

def send_random_id_to_server_and_client(client, game_server, id):
    client.send((str(id)).encode())
    game_server.send((str(id)).encode())

def check_username(username):
    return len(username) >= 1 and len(username) <= 12

def add_user(cur, con, username, password):
    hashed_password = hash_password(password)
    cur.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, hashed_password))
    con.commit()

def hash_password(password):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode())
    return sha256_hash.hexdigest()

def check_if_username_in_database(cur, con, username):
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cur.fetchone() is not None

def check_for_users_password(cur, username, password):
    hashed_password = hash_password(password)
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    actual_password = cur.fetchone()
    return actual_password and actual_password[0] == hashed_password

def retrieve_user_data_from_json(user_data_json):
    username = user_data_json["username"]
    password = user_data_json["password"]
    return (username, password)

def handle_login(client):
    con = sqlite3.connect("userdata.db")
    cur = con.cursor()

    logged_in = False
    while not logged_in:
        data = b''  

        while True:
            packet = client.recv(1024)
            if not packet:
                return  
            
            data += packet  

            try:
                json_data = json.loads(data.decode())
                break
            except json.JSONDecodeError:
                continue

        username, password = retrieve_user_data_from_json(json_data)

        if check_if_username_in_database(cur, con, username):
            if check_for_users_password(cur, username, password):
                client.send("SUCCESS".encode())
                send_random_id_to_server_and_client(client, connection_to_game_server, generate_random_number())
                logged_in = True
            else:
                client.send("PASSWORD".encode())
        else:
            client.send("REGISTER".encode())
            if check_username(username):
                add_user(cur, con, username, password)  
                client.send("SUCCESS".encode())  
                random_id = generate_random_number()
                send_random_id_to_server_and_client(client, connection_to_game_server, random_id)
                logged_in = True

def login_server():
    while True:
        server.listen()
        client, address = server.accept()

        login_process = threading.Thread(target=handle_login, args=(client,))
        login_process.start()

login_server()