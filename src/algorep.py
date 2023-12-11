from mpi4py import MPI
import sys
import time

host_server_id = 1

class Server:
    def __init__(self, comm, nb_servers, nb_clients):
        self.comm = comm
        self.id = comm.Get_rank()
        self.nb_servers = nb_servers
        self.nb_clients = nb_clients
        self.log = []
        self.crash = False
        self.speed = 2 # FAST by default

    def replicate_value_across_servers(self):
        # Simulate replicating the value to other servers
        for server_id in range(1, self.nb_servers + 1):
            if server_id != self.id:
                print(f"[SERVER] Server {self.id} sending \"{self.log}\" to server {server_id}.")
                self.comm.send(self.log, dest=server_id)
                time.sleep((2 - self.speed) * 1)

    def receive_value_from_server(self):
        # Simulate receiving a value from other servers
        for sender_id in range(1, self.nb_servers + 1):
            if sender_id != self.id:
                value = self.comm.recv(source=sender_id)
                self.log = value
                print(f"[SERVER] Server {self.id} received \"{self.log}\" from server {sender_id}.")

    def receive_value_from_client(self, source):
        # Simulate receiving a value from a client
        value = self.comm.recv(source=source)
        self.log.append(value)
        print(f"[SERVER] Server {self.id} received \"{value}\" from client.")

    def check_logs(self):
        self.replicate_value_across_servers()
        for sender_id in range(1, self.nb_servers + 1):
            if sender_id != self.id:
                value = self.comm.recv(source=sender_id)
                if (self.log != value):
                    print(f"[SERVER][ERROR] Server {self.id} has a different log ({self.log}) than server {sender_id} ({value}).")
                    return
        for i in range(self.nb_servers + 1, self.nb_servers + 1 + self.nb_clients):
            self.notify_client(i)

    def notify_client(self, client_UID):
        # Simulate notifying the client about successful replication
        print(f"[SERVER] Server {self.id} notifies Client {client_UID}: Replication successful.")
    
    def receive_REPL(self):
        value = self.comm.recv(source=0).strip().split()

        if (value[0] == "SPEED"):
            if (value[1] == "LOW"):
                self.speed = 0
            elif (value[1] == "MEDIUM"):
                self.speed = 1
            elif (value[1] == "HIGH"):
                self.speed = 2
            self.comm.send(f"[SERVER] Server {self.id} is now {value[1]}.", dest=0)

        if (value[0] == "CRASH"):
            self.crash = True
            self.comm.send(f"[SERVER] Server {self.id} crashed.", dest=0)

        if (value[0] == "LOG"):
            self.comm.send(f"[SERVER] Server {self.id} LOG : \t{self.log}.", dest=0)

    def run(self):
        '''
        if (self.id == host_server_id):
            for i in range(self.nb_servers + 1, self.nb_servers + 1 + self.nb_clients):
                self.receive_value_from_client(i)
            self.replicate_value_across_servers()
        else:
            self.receive_value_from_server()
        # self.check_logs()
        '''

        while True:
            self.receive_REPL()
            '''
            if not self.crash:
                self.receive_value_from_client()
                self.replicate_value_across_servers()
            '''






class Client:
    def __init__(self, comm):
        self.comm = comm
        self.UID = comm.Get_rank()
        self.isStarted = False
    
    def send_command(self, server_id, command):
        if (self.isStarted):
            self.comm.send(command, dest=server_id)
    
    def receive_REPL(self):
        value = self.comm.recv(source=0).strip().split()

        if (value[0] == "START"):
            self.isStarted = True
            self.comm.send(f"[CLIENT] Client {self.UID} started.", dest=0)
    
    def run(self):
        self.send_command(host_server_id, self.UID)

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

def REPL(comm, nb_servers, nb_clients):
    while True:
        try:
            command = input("[REPL]: ").strip().split()
            if len(command) > 0:
                com = command[0].upper()
                if com == "CRASH":
                    if len(command) <= 1:
                        print("Please enter a server ID")
                    else:
                        server_id = string_to_positive_integer(command[1])
                        if server_id < 1 or server_id > nb_servers:
                            print("Please enter a valid server ID")
                        else:
                            comm.send("CRASH", dest=server_id)
                            print(comm.recv(source=server_id))
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
                            comm.send("SPEED LOW", dest=server_id)
                            print(comm.recv(source=server_id))
                        elif speed == "MEDIUM":
                            comm.send("SPEED MEDIUM", dest=server_id)
                            print(comm.recv(source=server_id))
                        elif speed == "HIGH":
                            comm.send("SPEED HIGH", dest=server_id)
                            print(comm.recv(source=server_id))
                        else:
                            print("Please enter a valid speed value")
                elif com == "START":
                    for process_id in range(nb_servers + 1, nb_servers + 1 + nb_clients):
                        comm.send("START", dest=process_id)
                        print(comm.recv(source=process_id))
                elif com == "LOG":
                    if len(command) < 2:
                        comm.send("LOG", dest=host_server_id)
                        print(comm.recv(source=host_server_id))
                    else:
                        server_id = string_to_positive_integer(command[1])
                        if server_id < 1 or server_id > nb_servers:
                            print("Please enter a valid server ID")
                        else:
                            comm.send("LOG", dest=server_id)
                            print(comm.recv(source=server_id))
            

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
        REPL(comm, nb_servers, nb_clients)

    elif rank <= nb_servers:
        server = Server(comm, nb_servers, nb_clients)
        server.run()
        '''
        # Initializing servers with clients UIDs
        if (rank == 0):
            for _ in range(1, nb_clients + 1):
                server.receive_value_from_client()
            server.replicate_value_across_servers()
        else:
            server.receive_value_from_server()
        server.check_logs()
        '''
            
    else: # Client
        client = Client(comm)
        client.run()

        # client.send_command(1, client.UID)



if __name__ == "__main__":
    main()