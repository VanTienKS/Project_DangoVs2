# Project Dango Version2

Client and server to play game **Project Dango Game**. It uses [pygame](https://www.pygame.org/news).

# Screenshots
![](screenshots/house.png)

## Install
Requires: Python >=3.6.
To install, open a command prompt and launch:
```bash
pip3 install pygame
```

## Use
To launch a server:
```bash
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.gethostbyname(socket.gethostname())
port = 12345
socket_server.bind((server, port))

```
To launch a client:
```bash
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.gethostbyname(socket.gethostname())
port = 12345
socket_client.connect((server, port))
```

- HOST: IP address
- PORT: port number
- NUM_PLAYERS: number of players 2

HOST and PORT must be the same as the server.

## Play



## Pathfinding algorithm

## About Us 
[Email: vantiennst@gmail.com](https://vantienks.github.io/vantienks.githup.io/)

Email: ductindang1009@gmail.com

Email: tienhai488@gmail.com

## License
