import os

def main() :
    '''
    Ask for the number of servers and clients, and lauch algorep.py
    '''

    nb_clients = 2
    nb_servers = 2

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print("cd " + str(script_dir))

    command = "mpiexec -n " + str(nb_servers + nb_clients + 1) + " python3 algorep.py " + str(nb_servers) + " " + str(nb_clients)
    print(command)

    os.system(command)
    print()

    return 0

if __name__ == "__main__":
    main()
