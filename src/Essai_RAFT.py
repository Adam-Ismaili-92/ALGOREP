from mpi4py import MPI
import sys
import time

class Server:
    def __init__(self, comm, nb_servers, nb_clients):
        self.comm = comm
        self.id = comm.Get_rank()
        self.nb_servers = nb_servers
        self.nb_clients = nb_clients
        self.log = []
        self.log.append(f"Server {self.id} started")
        self.state = 'follower'
        self.current_term = 0
        self.voted_for = None
        self.vote_count = 0
        # self.heartbeat_received = False
        print(f"[SERVER] Initiated new server {self.id}")

    def start_election(self):
        self.state = 'candidate'
        self.current_term += 1
        self.voted_for = self.id
        self.vote_count = 1  # Vote for self
        print("In election")

        # Envoyer des demandes de vote à tous les autres serveurs
        for server_id in range(self.nb_servers):
            if server_id != self.id:
                self.comm.send({'term': self.current_term, 'candidate_id': self.id}, dest=server_id)

        time.sleep(0.2)
        # Attendre les réponses
        for _ in range(self.nb_servers - 1):
            if self.comm.Iprobe(source=MPI.ANY_SOURCE):
                data = self.comm.recv(source=MPI.ANY_SOURCE)
                if isinstance(data, dict) and 'vote_granted' in data:
                    if data['vote_granted']:
                        self.vote_count += 1
        self.check_majority_votes()

    def handle_vote_request(self, data):
        candidate_term = data['term']
        candidate_id = data['candidate_id']


        if candidate_term >= self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
            self.current_term = candidate_term  # Mettre à jour le terme actuel
            self.voted_for = candidate_id       # Accorder le vote
            self.state = 'follower'             # Revenir à l'état de follower
            self.comm.send({'term': self.current_term, 'vote_granted': True}, dest=candidate_id)
            print(f"[SERVER] Server {self.id} voted for candidate {candidate_id} for term {self.current_term}")
        else:
            # Si le serveur ne vote pas pour le candidat.
            self.comm.send({'term': self.current_term, 'vote_granted': False}, dest=candidate_id)
            print(f"[SERVER] Server {self.id} denied vote for candidate {candidate_id} for term {self.current_term}")

    def check_majority_votes(self):
        if self.vote_count > self.nb_servers // 2:
            self.state = 'leader'
            self.log.append(f"[SERVER] Server {self.id} is now the leader for term {self.current_term}")
            print(f"[SERVER] Server {self.id} is now the leader for term {self.current_term}")

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

    def handle_message(self):
        if self.comm.Iprobe(source=MPI.ANY_SOURCE):
            data = self.comm.recv(source=MPI.ANY_SOURCE)
            if isinstance(data, dict) and 'term' in data and 'candidate_id' in data:
                self.handle_vote_request(data)
            self.log = data

    def run(self):
        self.start_election()
        while True:
            self.handle_message()


class Client:
    def __init__(self, comm):
        self.comm = comm
        self.UID = comm.Get_rank()
    
    def send_command(self, server_id, command):
        self.comm.send(command, dest=server_id)
        print(f"[CLIENT] New client {self.UID}")


def main():
    # Initialize
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if (len(sys.argv) != 3):
        print(f"[MAIN] Program expected 2 arguments : 'nb_servers' and 'nb_clients'.")
        return

    nb_servers = int(sys.argv[1])
    nb_clients = int(sys.argv[2])

    # Initialize
    if (rank < nb_servers):
        server = Server(comm, nb_servers, nb_clients)
    else:
        client = Client(comm)

    # Barrier synchronization
    comm.Barrier()

    # Start server or client process
    if (rank < nb_servers):
        server.run()
    else:
        client.send_command(0, client.UID)

if __name__ == "__main__":
    main()