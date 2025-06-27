# Import necessary libraries
import sys
import socket
import threading


def main():
    # If the user doesn't provide 2 arguments
    if len(sys.argv) != 3:
        print("Usage: python3 server.py <server_ip> <server_port>") # Print the correct format
        sys.exit(1) # Exit the program
        
    def receiver(socket):
        while True:
            try:
                data = socket.recv(1024) # Receive data from the server(can only read 1024 bytes at once)
                if not data: # If data is empty meaning the server closed the connection or sent nothing
                    break # Exit the while loop
                print("Recieved from server: ", str(data.decode()))
            except: # If any exception occurs like network error or server abruptly disconnects, the except block catches
                break # and breaks out of loop stopping the function
        
    # Storing the user input 
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    # Creating a socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connecting to the server
    clientSocket.connect((host ,port))

    # Creates and starts a new thread to run receiver(clientsocket) in the background, 
    # so the main thread can still handle user input and sending messages while receiver() handles
    # incoming messages without blocking
    threading.Thread(target=receiver, args=(clientSocket,)).start() # 
    
    # User must user JOIN to enter chat
    print("Please enter JOIN followed by name: ") # Prompting the user to join
    newUser = input() # Stores the user input

    # Sends the newUser string over the network to the server using the socket converted to bytes by encode().
    clientSocket.send(newUser.encode()) 
    
    # Begin chat loop
    while True:
        userCommand = input() # Takes input
        clientSocket.send(userCommand.encode()) # Sends the typed message to the server in encoded byte format
        if userCommand == "QUIT": # If the user exactly typ
            break # exit the while loop 
        
    # Close the socket connection, fully disconnecting from the server
    clientSocket.close()
    
if __name__ == "__main__":
    main()
    
    
    
        
