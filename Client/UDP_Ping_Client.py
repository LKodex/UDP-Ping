import socket as socks
from time import time, ctime
from sys import argv
from math import inf

def main(serverAddress = ('localhost', 12000), pingQuantity = 10, bufferSize = 4096):
    socket = socks.socket(socks.AF_INET, socks.SOCK_DGRAM)
    socket.settimeout(2)
    packetSent = 0
    packetReceived = 0
    minimumRTT = inf
    maximumRTT = -inf
    accumulatedRTT = 0
    for seqNum in range(1, pingQuantity + 1):
        packetSent += 1
        try:
            sentTime = time()
            data = f'Ping {seqNum} {ctime(sentTime)}'
            socket.sendto(data.encode(), serverAddress)
            message, address = socket.recvfrom(bufferSize)
            receivedTime = time()
            packetReceived += 1
            RTT = receivedTime - sentTime
            accumulatedRTT += RTT
            maximumRTT = RTT if RTT > maximumRTT else maximumRTT
            minimumRTT = RTT if RTT < minimumRTT else minimumRTT
            socket.settimeout(2 * RTT + 1)
        except (TimeoutError, socks.timeout):
            print(f'Request {seqNum} timed out.')
    socket.close()
    packetLost = packetSent - packetReceived
    averageRTT = accumulatedRTT / packetReceived
    SECONDS_TO_MS = 1000
    print(f'Packets: Sent = {packetSent}, Received = {packetReceived}, Lost = {packetLost} ({int(packetLost / packetSent * 100)}% loss)')
    print(f'RTT: Minimum = {int(minimumRTT * SECONDS_TO_MS)}ms, Maximum = {int(maximumRTT * SECONDS_TO_MS)}ms, Average = {int(averageRTT * SECONDS_TO_MS)}ms')

if __name__ == '__main__':
    if len(argv) == 2:
        main(('localhost', int(argv[1])))
    elif len(argv) == 3:
        main((argv[1], int(argv[2])))
    else:
        main()
