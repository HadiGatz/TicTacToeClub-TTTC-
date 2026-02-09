# TTTC - TicTacToeClub
---
TTTC brings the classic game of Tic-Tac-Toe to the online world, 
allowing players to enjoy multiplayer matches 
over the network. This project is built using Python.


## Installation & Set Up
---
In order to set up your own TicTacToe server, install the modules:
- Board.py
- TTTManager.py
- server.py
- login_server.py


In addition, you should pip install the following libraries:
- pickle
- json
- threading
- time
- hashlib
- socket
- sqlite3

Put all the modules in the same directory.
After installing, run server.py, then run login_server.py.
You now have your very own TicTacToe server.

## Architecture
The architecture behind the project consists of 2 servers - The main (game) server, and the Login server.


### Login Server
The Login server consists of 2 sockets - 1 socket that serves as the way to connect to the server, 
and the other socket for communication with the Main server.
It also connects to the users database, using Python's sqlite3 library. 
The server's general logic looks like this:


After every successful Login, the Login server sends the client and the main server a special ID, which the client will use when connecting to the main server. That way,
the main server can verify that the user indeed logged in earlier.

### Main Server
The main server consists of 2 sockets - 1 socket serving its clients (the players), and the other for direct communication with the Login server. 
Its general logic looks like this:


## Security

During the planning and execution of this project, security was my top priority. Because of that, some decisions were made by me,
that had sacrificed some efficiency for security. Examples include:
- Sending Login information with JSON instead of using pickle - While pickle is faster, I decided to use encrypted JSON instead.
- Hashing passwords before storing them - Storing passwords in the database in their original form would be a security risk.
- Performing checks both on the client and server side - The client can, potentially, change his code.


