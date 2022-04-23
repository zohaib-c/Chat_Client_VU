import socket
import time
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostPort = ("143.47.184.219", 5378)
sock.connect(hostPort)


def incomingMessages():
    while True:
        try:
            reply = sock.recv(2).decode("utf-8")
            while not reply.endswith("\n"):
                reply += sock.recv(2).decode("utf-8")

            splice = 0
            for i in range(0, len(reply)):
                if reply[i] == " ":
                    splice = i + 1
                    break
            reply = reply[splice:]
            print(reply)
        except OSError as msg:
            print(msg)


username = str(input("Enter username: "))
handshakeSuccess = False
while not handshakeSuccess:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostPort = ("143.47.184.219", 5378)
    sock.connect(hostPort)

    firstMessage = ("HELLO-FROM " + username + "\n").encode("utf-8")
    try:
        sock.sendall(firstMessage)
    except OSError as msg:
        print(msg)

    try:
        handshake = sock.recv(4096).decode("utf-8")
        if not handshake:
            print("Socket is Closed")
        else:
            if handshake[:5] == "HELLO":
                print(handshake)
                handshakeSuccess = True
            else:
                print(handshake)
                username = str(input("Enter UNIQUE username: "))
    except OSError as msg:
        print(msg)

t = Thread(target=incomingMessages)
t.daemon = True
t.start()

print("The users online right now are:")
try:
    sock.sendall("WHO\n".encode("utf-8"))
except OSError as msg:
    print(msg)

time.sleep(0.03)
while True:
    userInput = str(input("Type '!who' to get a list of all available users, '!quit' to quit the chatroom, or "
                          "'@username message' to send a message to a user that is online\n"))

    if userInput == "!quit":
        break

    else:
        if userInput == "!who":
            print("The users online right now are:")
            try:
                sock.sendall("WHO\n".encode("utf-8"))
            except OSError as msg:
                print(msg)

        if userInput[0] == "@":
            sendUser = ""
            spaceIndex = 0
            for i in range(1, len(userInput)):
                if userInput[i] == " ":
                    spaceIndex = i
                    break
                else:
                    sendUser = sendUser + userInput[i]

            messageInput = userInput[spaceIndex:]

            while True:
                if messageInput != "!end":
                    message = "SEND " + sendUser + " " + messageInput + "\n"
                    try:
                        sock.sendall(message.encode("utf-8"))
                    except OSError as msg:
                        print(msg)

                    time.sleep(0.05)
                    messageInput = str(input("Enter reply or !end to end conversation: "))
                else:
                    break
    time.sleep(0.03)
