# Import the libraries
import sys # Used to get command-line arguments
import socket # Provides low-level networking interface 
import threading # To handle multiple clients simultaneoulsy

# A dictionary mapping client usernames to client sockets, so the server knows
# who's connected and where to send messages
userDatabase = dict()

# Thread function: handles one client's connection in a seperate thread
def threaded(clientSocket):
    username = None # Username initialized to track the client's name after they send a JOIN
    # Loop to receive client messages
    while True:
        try:
            # data received from client
            data = clientSocket.recv(1024)
            if not data: # If nothing comes,
                print('Disconnecting') # Print disconnecting
                break # and break from the loop
            
            # using startwith() to check if user inputed JOIN
            data = data.decode().strip() # decode() convert bytes to string and strip() removes leading and trailing whitespace from a string
            if data.startswith("JOIN "): # Check if user input begins with a "JOIN"
                # storing the user inputted name
                name = data.split()[1] # Gets the second element from a list of substrings by splitting the data string at whitespace
                if len(userDatabase) > 10:
                    # Reject new user if current users are over 10
                    clientSocket.send("Too Many Users".encode())
                # Store new user in database if there is space in the chat
                elif len(userDatabase) <= 10:
                    userDatabase[name] = clientSocket # add the client socket to the dictionary(mapped to the username)
                    username = name
                    print(f"{username} has joined the chat") 
                    
            # Removes user from the userDatabase
            elif data == "QUIT": # If user wants to quit
                if username in userDatabase: # if username is in the userDatabase dictionary 
                    del userDatabase[username] # delete that user from the userDatabase dictionary
                    print(f"{username} is quitting the server")

            # Sends the list of connected users back to the requester
            elif data == "LIST":
                if username is not None: 
                    displayList = ", ".join(userDatabase.keys())
                    clientSocket.send(displayList.encode())
                    
            elif data.startswith("BCST "):
                if username is not None:
                    # message contains all the items of the string after the command
                    broadcastMsg = data[5:]
                    clientSocket.send(f"{username} is sending a broadcast".encode())
                    bcstFunc(username, broadcastMsg)
                    
            elif data.startswith("MESG"):
                userInput = data.split()
                
                # storing the name of recepcient 
                recpName = userInput[1]
                # storing the message of the user
                message = " ".join(userInput[2:])
                
                # ensuring that user has enough arguments in command call
                if len(userInput) < 3:
                    print("Usage: MESG <User> <Message>")
                    
                if recpName in userDatabase:
                    try:
                        userDatabase[recpName].send(f"{username}: {message} ".encode())
                    except:
                        clientSocket.send("Error".encode())
        
        except:
            break
    # connection closed
    clientSocket.close()
    
def bcstFunc(username, message):
    for name, userSocket in userDatabase.items():
        if name != username:
            userSocket.send(f"{username}: {message}".encode())


def main():
    # Correct usage shown in case of arguments mismatch
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <server_port>")
        sys.exit(1) # Exit the program
        
    port = int(sys.argv[1]) # Stores the port number

    # TCP server socket creation + binding
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a TCP socket
    serverSocket.bind(("0.0.0.0", port)) # Binds the TCP socket to all interfaces on the specified port
    
    serverSocket.listen(5) # Prepares to accept up to 5 pending connections
    print("Socket is Listening")
    
    
    # a forever loop until client wants to exit
    while True:
        # establish connection with client and gets a new socket and the client address
        clientSocket, addr = serverSocket.accept()
        print('Connected to :', {addr})
        # Start a new thread for each client so multiple user can chat simulataneously and return client identifier
        t1 = threading.Thread(target = threaded, args=(clientSocket,))
        t1.start()
    serverSocket.close() # close the circuit

if __name__ == "__main__":
    main()
