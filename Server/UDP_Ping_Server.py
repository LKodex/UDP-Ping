import socket as socks
from random import randint

def main(
        packetLoss    = 30,
        serverAddress = ('localhost', 12000),
        bufferSize    = 4096
        ):
    try:
        socket = socks.socket(socks.AF_INET, socks.SOCK_DGRAM)
        socket.bind(serverAddress)
        print(f'Server listening at {serverAddress[0]}:{serverAddress[1]}')
        print(f'Simulated packet loss: {packetLoss}%')
        print(f'Buffer size: {bufferSize} bytes')
        while True:
            message, address = socket.recvfrom(bufferSize)
            if randint(1, 100) <= packetLoss: continue
            socket.sendto(message, address)
    except KeyboardInterrupt:
        print('Stopping the server')
    finally:
        print('Closing the socket')
        socket.close()

if __name__ == '__main__':
    main()