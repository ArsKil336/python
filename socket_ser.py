import socket

server_ip = socket.gethostbyname(socket.gethostname())

# Создаем UDP сокет (SOCK_DGRAM)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем к порту на всех интерфейсах
my_ip = server_ip
server.bind(('0.0.0.0', 8080))
server.setblocking(False)
print(f"UDP сервер запущен!")
print(f"Ваш IP в сети: {my_ip}")
print("Ожидание сообщений...")
while True:
    # recvfrom возвращает кортеж: (данные, адрес_отправителя)
    try:
        data, addr = server.recvfrom(1024)
        print(f"[{addr}] получено: {data.decode()}")
        
        # Можно сразу отправить ответ обратно
        server.sendto("OK".encode('utf-8'), addr)
    except BlockingIOError:
        pass
    except InterruptedError:
        print('\nСервер остановлен')
        break
server.close()