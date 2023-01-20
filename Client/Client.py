import socket,time,select,sys

class client:

    def __init__(self,host,port,pseudo):
        self.host=host
        self.port=port
        self.pseudo=pseudo
        self.socket_liste=[]
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)

    def connection_server(self):
        try:
            self.socket.connect((self.host,self.port))
            print ('Connnecte au serveur !')
            
        except:
            print("connexion impossible")
            exit
 
    def envoie_message(self):
        x=1
        
        while x == 1:
            self.socket_liste = [sys.stdin, self.socket]

            # On recupere les socket (que la socket server de memeorie)
            read_sockets, write_sockets, error_sockets = select.select(self.socket_liste,[],[])

            for sock in read_sockets:
                #en cas de message recu du server, si cest nous on print les infos
                if sock == self.socket:
                    data = sock.recv(4096)
                    #si il n y a rien que du vide , theoriquement deco du tchat
                    if not data :
                        print ('\nDeconnecte du serveur de tchat')
                        sys.exit()
                    else :
                        #on affiche les donnes envoyé par la socket server
                        sys.stdout.write(data)

                #user entered a message
                else :
                    msg=sys.stdin.readline()
                    self.socket.send(msg)
                    print(self.pseudo,": ",msg)
                    