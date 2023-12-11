from mpi4py import MPI
import sys

class Server:
    def __init__(self, comm, nb_servers, nb_clients):
        self.comm = comm
        self.id = comm.Get_rank()
        self.nb_servers = nb_servers
        self.nb_clients = nb_clients
        self.log = []
        print(f"[SERVER] Initiated new server {self.id}")

    def replicate_value_across_servers(self):
        # Simulate replicating the value to other servers
        for server_id in range(self.nb_servers):
            if server_id != self.id:
                print(f"[SERVER] Server {self.id} sending \"{self.log}\" to server {server_id}.")
                self.comm.send(self.log, dest=server_id)

    def receive_value_from_server(self):
        # Simulate receiving a value from other servers
        for sender_id in range(0, self.nb_servers):
            if sender_id != self.id:
                value = self.comm.recv(source=sender_id)
                self.log = value
                print(f"[SERVER] Server {self.id} received \"{self.log}\" from server {sender_id}.")

    def receive_value_from_client(self):
        # Simulate receiving a value from a client
        value = self.comm.recv(source=MPI.ANY_SOURCE)
        self.log.append(value)
        print(f"[SERVER] Server {self.id} received \"{value}\" from client.")

    def check_logs(self):
        self.replicate_value_across_servers()
        for sender_id in range(0, self.nb_servers):
            if sender_id != self.id:
                value = self.comm.recv(source=sender_id)
                if (self.log != value):
                    print(f"[SERVER][ERROR] Server {self.id} has a different log ({self.log}) than server {sender_id} ({value}).")
                    return
        for i in range(1, self.nb_clients + 1):
            self.notify_client(i)

    def notify_client(self, client_UID):
        # Simulate notifying the client about successful replication
        print(f"[SERVER] Server {self.id} notifies Client {client_UID}: Replication successful.")

class Client:
    def __init__(self, comm):
        self.comm = comm
        self.UID = comm.Get_rank()
    
    def send_command(self, server_id, command):
        self.comm.send(command, dest=server_id)
        print(f"[CLIENT] New client {self.UID}")


def main():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if (len(sys.argv) != 3):
        print(f"[MAIN] Program expected 2 arguments : 'nb_servers' and 'nb_clients'.")
        return

    nb_servers = int(sys.argv[1])
    nb_clients = int(sys.argv[2])

    # Server
    if (rank < nb_servers):
        server = Server(comm, nb_servers, nb_clients)

        if (rank == 0): # Leader server
            for i in range(1, nb_clients + 1):
                server.receive_value_from_client()
            server.replicate_value_across_servers()
        else:
            server.receive_value_from_server()
        
        server.check_logs()

    # Client
    else:
        client = Client(comm)
        client.send_command(0, client.UID)



if __name__ == "__main__":
    main()