from Client import client

leClient=client("127.0.0.1",8080,"Balkany")
leClient.connection_server()
leClient.envoie_message()

