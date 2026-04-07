import socket

HOST = '0.0.0.0'
PORT = 5000
BUFFER_SIZE = 1024
PING_MESSAGE = 'ping'.encode('utf-8')

# Создание UDP-сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязка к адресу и порту
server_socket.bind((HOST, PORT))

print(f"UDP сервер запущен на {HOST}:{PORT}")
print('Отправка всем пользователям ping...')
for i in range(256):
    server_socket.sendto(PING_MESSAGE, (f"192.168.1.{i}", 5000))
print('Всем пользователям было отправлено сообщение ping.')

while True:
    # Получение данных и адреса клиента
    data, address = server_socket.recvfrom(BUFFER_SIZE)
    print('Получено сообщение', data.decode('utf-8'), 'от', address)
    if data.decode('utf-8') == 'ping':
        message = "pong"
    
        # Отправка ответа клиенту
        server_socket.sendto(message.encode('utf-8'), address)
        print(f"Отправлено сообщение '{message}' клиенту {address}")