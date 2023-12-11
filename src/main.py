import os

def main() :
    '''
    
    Ask for the number of servers and clients, and lauch algorep.py
    
    '''
    
    nb_clients = input("Number of clients : ")
    nb_servers = input("Number of servers : ")
    
    command = "mpiexec -n 4 python algorep.py " + str(nb_servers) + " " + str(nb_clients)
    
    os.system(command)
    
    return 0

if __name__ == "__main__":
    main()