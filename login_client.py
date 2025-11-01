import socket
import json

def get_user_login_info():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    return {"username": username, "password": password}

def send_user_login_info(client, info):
    data = json.dumps(info)  
    client.sendall(data.encode())  

def check_username(username):
    return len(username) >= 1 and len(username) <= 12

def handle_new_user(client):
    username = input("Enter your username: ")
    
    if check_username(username):
        password = input("Enter your password: ")
        send_user_login_info(client, {"username": username, "password": password})

        result = client.recv(1024).decode()
        if result == "SUCCESS":
            print("Success - You are logged in.")
        elif result == "USERNAME_EXISTS":
            print("Your user already exists. Please log in.")
            handle_existing_user(client)
        elif result == "REGISTER":
            print("You are registering as a new user.")
            client.send(password.encode())  
            result = client.recv(1024).decode()
            if result == "SUCCESS":
                print("Registration successful. You are now logged in.")

def handle_existing_user(client):
    user_info = get_user_login_info()
    send_user_login_info(client, user_info)
    result = client.recv(1024).decode()

    if result == "SUCCESS":
        print("Success - You are logged in.")
    elif result == "PASSWORD":
        print("ERROR: Wrong password.")
        retry_login(client, user_info["username"])
    elif result == "REGISTER":
        print("ERROR: No such username was found. Proceeding to register.")
        handle_new_user(client)

def retry_login(client, username):
    attempts = 3
    while attempts > 0:
        password = input(f"Enter your password ({attempts} attempts left): ")
        send_user_login_info(client, {"username": username, "password": password})

        result = client.recv(1024).decode()
        if result == "SUCCESS":
            print("Success - You are logged in.")
            return
        attempts -= 1
    print("Too many failed attempts. Disconnecting...")

def handle_login(client):
    client.connect(('192.168.68.104', 5557))
    new_or_not = input("Do you have a registered user? [Y/N] ").lower()

    if new_or_not == 'y':
        handle_existing_user(client)
    else:
        handle_new_user(client)
    
    

client = socket.socket()
handle_login(client)