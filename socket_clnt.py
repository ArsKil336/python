import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = socket.gethostbyname(socket.gethostname())

# Укажите IP сервера, который напечатал скрипт выше
SERVER_ADDR = (server_ip, 8080) 

message = "Привет по UDP!"
client.sendto(message.encode(), SERVER_ADDR)

# Ждем подтверждения от сервера (необязательно)
data, server = client.recvfrom(1024)
print(f"Ответ сервера: {data.decode()}")

client.close()