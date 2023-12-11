import mpi4py.MPI
from mpi4py import MPI
import sys
import random
import time
import os

def client_process(uid, server_comm):
    # Processus client
    # Envoie la valeur/la commande au serveur
    server_comm.send(uid, dest=0)
    
def server_process(rank, size, server_comm):
    # Processus serveur
    logs = []

    for _ in range(size - 1):
        # Attend la réception des valeurs des clients
        uid = server_comm.recv(source=MPI.ANY_SOURCE)
        # Met en œuvre le consensus entre les serveurs si nécessaire
        # Réplique la valeur/commande dans le log
        logs.append(uid)
        # Notifie le client que la réplication est réussie
        server_comm.send("Réplication réussie", dest=rank)

    return logs

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 3:
        if rank == 0:
            print("Le système nécessite au moins 3 processus (1 serveur et 2 clients).")
    else:
        # Si c'est un serveur
        if rank == 0:
            server_comm = comm.Split(0)
            logs = server_process(rank, size, server_comm)
            print("Logs finaux du serveur {}: {}".format(rank, logs))
        # Si c'est un client
        else:
            server_comm = comm.Split(1)
            client_process(rank, server_comm)
            # Attend la notification du serveur
            server_comm.recv()

if __name__ == "__main__":
    main()