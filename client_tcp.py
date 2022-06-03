from asyncio import threads
import socket
import threading

import argparse
from time import sleep

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bKeepRunning = True

def Try2Connect(ip, port):
    print("Trying to connect to a server at {}:{}".format(args.ip, int(args.port)))
    
    client.settimeout(1)
    
    try:
        client.connect((ip, int(port)))
        return True
    except ConnectionRefusedError as e:
        print(e)
    
    return False


def SendInput():
    global bKeepRunning
    while bKeepRunning:
        try:
            text = input(">>> ")
            if text:
                client.send(text.encode())
                sleep(1)
            else:
                bKeepRunning = False
                break
        except Exception as e:
            print(e)    
    print("Leaving SendInput")
            

def ReadData():
    global bKeepRunning
    while bKeepRunning:
        try:
            data = client.recv(1024).decode()
            if data:
                if data == '\n':
                    bKeepRunning = False
                    break

                print("<<<" + data)
            else:
                return
        except TimeoutError:
            pass
        except Exception as e:
            print(e)
    print("Leaving ReadData")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="TCP Client", description="Creates a tcp client at a desired ip and port", epilog="To close a connection, just sent an empty message\n")
    parser.add_argument('ip', help="IP to connect")
    parser.add_argument('port', help="Port to connect")
    args = parser.parse_args()

    if Try2Connect(args.ip, args.port):
        
        threadlist = []
        threadlist.append(threading.Thread(target=SendInput))
        threadlist.append(threading.Thread(target=ReadData))

        for thread in threadlist:
            thread.start()
            
        for thread in threadlist:
            thread.join()
    else:
        print("Connection failed...")
    


    