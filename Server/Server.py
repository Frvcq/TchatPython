import socket,select

class server:

 def __init__(self, host, port):
    self.host = host  
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    self.listeClient = []

 def start(self):
    RECV_BUFFER = 4096       
    #on lie le port et l'ip
    self.socket.bind((self.host,self.port))
    #la file dattente
    self.socket.listen(50)
    #on sajoute en tant que socket afin de parlementer aux autres
    self.listeClient.append(self.socket)
    print("Serveur demarré")
    #jai pas trouver comme faire de la prog evenementielle, on boucle alors a linfini
    while 1:
        # On recupere la liste de nos sockets
        read_sockets,write_sockets,error_sockets = select.select(self.listeClient,[],[])

        for sock in read_sockets:
            #Nnouvelle connexion
            if sock == self.socket:
                # en cas de nouvelle connection recu sur le serveur
                sockfd, addr = self.socket.accept()
                self.listeClient.append(sockfd)
                print ("Client (%s, %s) connected" % addr)
                self.broadcast_message(sockfd, "[%s:%s] entered room\n" % addr)
            else:
                # donnees recu du client
                try:
                    #en cas de coupure tcp de windaube
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        self.broadcast_message(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                
                except:
                    self.broadcast_message(sock, "Client (%s, %s) is offline" % addr)
                    print ("Client (%s, %s) is offline" % addr)
                    sock.close()
                    self.listeClient.remove(sock)
                    continue

 def broadcast_message(self, sock, message):
    for socket in self.listeClient:            
        if socket != self.socket and socket != sock :
            try :
                socket.send(message)
            except :
                # socket casse , on lexplose
                socket.close()
                self.listeClient.remove(socket)

 def stop(self):
    print("interruption du serveur, fermeture")
    self.socket.close

 def getPort(self):
    return self.port

 def getHost(self):
    return self.host