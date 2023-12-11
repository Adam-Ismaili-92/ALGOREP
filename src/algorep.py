from mpi4py import MPI
import sys
import time

host_server_id = 1

REPL, REPL_RESPONSE, FOR_SERVER, FOR_CLIENT, DELTA, UPDATE = 0, 1, 2, 3, 4, 5

class Server:
    def __init__(self, comm, nb_servers, nb_clients):
        self.comm = comm
        self.id = comm.Get_rank()
        self.nb_servers = nb_servers
        self.nb_clients = nb_clients
        self.log = []
        self.crash = False
        self.speed = 2 # FAST by default
        self.file = ""
        self.delta = 0

    def replicate_value_across_servers(self):
        # Simulate replicating the value to other servers
        for server_id in range(1, self.nb_servers + 1):
            if server_id != self.id:
                print(f"[SERVER] Server {self.id} sending \"{self.log}\" to server {server_id}.")
                self.comm.send(self.log, dest=server_id, tag=FOR_SERVER)
                time.sleep((2 - self.speed) * 1)

    def receive_value_from_server(self):
        # Simulate receiving a value from other servers
        for sender_id in range(1, self.nb_servers + 1):
            if sender_id != self.id:
                value = self.comm.recv(source=sender_id, tag=FOR_SERVER)
                self.log = value
                print(f"[SERVER] Server {self.id} received \"{self.log}\" from server {sender_id}.")

    def receive_value_from_client(self, source):
        # Simulate receiving a value from a client
        value = self.comm.recv(source=source, tag=FOR_SERVER)
        self.log.append(value)
        print(f"[SERVER] Server {self.id} received \"{value}\" from client.")

    def check_logs(self):
        self.replicate_value_across_servers()
        for sender_id in range(1, self.nb_servers + 1):
            if sender_id != self.id:
                value = self.comm.recv(source=sender_id, tag=FOR_SERVER)
                if (self.log != value):
                    print(f"[SERVER][ERROR] Server {self.id} has a different log ({self.log}) than server {sender_id} ({value}).")
                    return
        for i in range(self.nb_servers + 1, self.nb_servers + 1 + self.nb_clients):
            self.notify_client(i)

    def notify_client(self, client_UID):
        # Simulate notifying the client about successful replication
        print(f"[SERVER] Server {self.id} notifies Client {client_UID}: Replication successful.")

    def update_delta(self):
        for sender_id in range(1, self.nb_servers + 1):
            if sender_id != self.id:
                self.comm.send(self.delta, dest=sender_id, tag=DELTA)

    def update_file(self):
        file_path = "my_file.txt"
        with open(file_path, "w") as file:
            file.write(self.file)
        for sender_id in range(1, self.nb_servers + 1):
            if sender_id != self.id:
                self.comm.send(self.file, dest=sender_id, tag=UPDATE)
    
    def receive_REPL(self):
        value = self.comm.recv(source=0, tag=REPL).strip().split()
        
        if (value[0] == "MOVE"):
            self.delta += int(value[1])
            if (self.delta < 0):
                self.delta = 0
            self.update_delta()
            self.comm.send(f"Here is the edited delta {self.delta}", dest=0, tag= REPL_RESPONSE)
        if (value[0] == "INSERT"):
            text = ""
            for i in range(1,len(value)):
                text = text + value[i] + " "
            self.file = self.file[:self.delta] + text + self.file[self.delta:]
            self.update_file()
            self.comm.send(f"Here is the edited file {self.file}", dest=0, tag= REPL_RESPONSE)
        if (value[0] == "DELETE"):
            self.file = self.file[:self.delta] + self.file[self.delta + int(value[1]):]
            self.update_file()
            self.comm.send(f"Here is the edited file {self.file}", dest=0, tag= REPL_RESPONSE)


        if (value[0] == "SPEED"):
            print("hello")
            if (value[1] == "LOW"):
                self.speed = 0
            elif (value[1] == "MEDIUM"):
                self.speed = 1
            elif (value[1] == "HIGH"):
                self.speed = 2
            self.comm.send(f"[SERVER] Server {self.id} is now {value[1]}.", dest=0, tag=REPL_RESPONSE)

        if (value[0] == "CRASH"):
            self.crash = True
            self.comm.send(f"[SERVER] Server {self.id} crashed.", dest=0, tag=REPL_RESPONSE)

        if (value[0] == "LOG"):
            self.comm.send(f"[SERVER] Server {self.id} LOG : \t{self.log}.", dest=0, tag=REPL_RESPONSE)

    def handle_message(self):
        value = self.comm.recv(source=0, tag=DELTA)
        if (isistance(value, int)):
            self.delta = value
        value = self.comm.recv(source=0, tag=UPDATE).strip()
        if (isistance(value, str)):
            self.file = value
        

    def run(self):
        # Initializing servers with clients UIDs
        if (self.id == host_server_id):
            for i in range(self.nb_servers + 1, self.nb_servers + 1 + self.nb_clients):
                self.receive_value_from_client(i)
            self.replicate_value_across_servers()
        else:
            self.receive_value_from_server()

        while True:
            self.receive_REPL()

            '''
            if not self.crash:
                if (self.id == host_server_id):
                    for i in range(self.nb_servers + 1, self.nb_servers + 1 + self.nb_clients):
                        self.receive_value_from_client(i)
                    self.replicate_value_across_servers()
                else:
                    self.receive_value_from_server()
            '''
            






class Client:
    def __init__(self, comm):
        self.comm = comm
        self.UID = comm.Get_rank()
        self.isStarted = False
    
    def send_command(self, server_id, command, bypass=False):
        if (bypass or self.isStarted):
            self.comm.send(command, dest=server_id, tag=FOR_SERVER)
    
    def receive_REPL(self):
        value = self.comm.recv(source=0, tag=REPL).strip().split()

        if (value[0] == "START"):
            self.isStarted = True
            self.comm.send(f"[CLIENT] Client {self.UID} started.", dest=0, tag=REPL_RESPONSE)
    
    def run(self):
        self.send_command(host_server_id, self.UID, bypass=True)

        while True:
            self.receive_REPL()
                




def string_to_positive_integer(s):
    try:
        num = int(s)
        if num >= 0:
            return num
        else:
            return -1
    except ValueError:
        return -1

def REPL_function(comm, nb_servers, nb_clients):
    while True:
        try:
            command = input("[REPL]: ").strip().split()
            if len(command) > 0:
                com = command[0].upper()
                if com == "MOVE":
                    if len(command) <= 1:
                        print("Need cursus movement")
                    else:
                        comm.send(f"MOVE {command[1]}", dest = host_server_id, tag = REPL)
                        print(comm.recv(source=host_server_id, tag=REPL_RESPONSE))
                elif com == "INSERT":
                    if len(command) <= 1:
                        print("Need text to insert")
                    else:
                        text = ""
                        for i in range(1,len(command)):
                            text = text + command[i] + " "
                        comm.send(f"INSERT {text}", dest = host_server_id, tag = REPL)
                        print(comm.recv(source=host_server_id, tag=REPL_RESPONSE))
                elif com == "DELETE":
                    if len(command) <= 1:
                        print("Need number of characters to delete")
                    else:
                        comm.send(f"DELETE {command[1]}", dest = host_server_id, tag = REPL)
                        print(comm.recv(source=host_server_id, tag=REPL_RESPONSE))
                elif com == "CRASH":
                    if len(command) <= 1:
                        print("Please enter a server ID")
                    else:
                        server_id = string_to_positive_integer(command[1])
                        if server_id < 1 or server_id > nb_servers:
                            print("Please enter a valid server ID")
                        else:
                            comm.send("CRASH", dest=server_id, tag=REPL)
                            print(comm.recv(source=server_id, tag=REPL_RESPONSE))
                elif com == "SPEED":
                    if len(command) <= 2:
                        print("Please enter a speed value and a server ID")
                    else:
                        speed = command[1].upper()
                        server_id = string_to_positive_integer(command[2])
                        if server_id < 1 or server_id > nb_servers:
                            print("Please enter a valid server ID")
                            continue
                        if speed == "LOW":
                            comm.send("SPEED LOW", dest=server_id, tag=REPL)
                            print(comm.recv(source=server_id, tag=REPL_RESPONSE))
                        elif speed == "MEDIUM":
                            comm.send("SPEED MEDIUM", dest=server_id, tag=REPL)
                            print(comm.recv(source=server_id, tag=REPL_RESPONSE))
                        elif speed == "HIGH":
                            comm.send("SPEED HIGH", dest=server_id, tag=REPL)
                            print(comm.recv(source=server_id, tag=REPL_RESPONSE))
                        else:
                            print("Please enter a valid speed value")
                elif com == "START":
                    for process_id in range(nb_servers + 1, nb_servers + 1 + nb_clients):
                        comm.send("START", dest=process_id, tag=REPL)
                        print(comm.recv(source=process_id, tag=REPL_RESPONSE))
                elif com == "LOG":
                    if len(command) < 2:
                        comm.send("LOG", dest=host_server_id, tag=REPL)
                        print(comm.recv(source=host_server_id, tag=REPL_RESPONSE))
                    else:
                        server_id = string_to_positive_integer(command[1])
                        if server_id < 1 or server_id > nb_servers:
                            print("Please enter a valid server ID")
                        else:
                            comm.send("LOG", dest=server_id, tag=REPL)
                            print(comm.recv(source=server_id, tag=REPL_RESPONSE))
            

        except EOFError:
            break
            


def main():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if (len(sys.argv) != 3):
        print(f"[MAIN] Program expected 2 arguments : 'nb_servers' and 'nb_clients'.")
        return

    nb_servers = int(sys.argv[1])
    nb_clients = int(sys.argv[2])

    # Create Server instance for each process
    if rank == 0:
        REPL_function(comm, nb_servers, nb_clients)

    elif rank > 0 and rank <= nb_servers:
        server = Server(comm, nb_servers, nb_clients)
        server.run()
            
    elif rank > nb_servers: # Client
        client = Client(comm)
        client.run()



if __name__ == "__main__":
    main()