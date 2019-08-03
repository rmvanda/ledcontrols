from simple_websocket_server import WebSocketServer, WebSocket


class TableListener(WebSocket):

    clients = []

    def handle(self):
        for client in self.clients:
            if client != self:
                client.send_message(self.data)

    def lightSeats()
        pass

    def doAnimation(animation, **params):
        pass

    def on(color,style=None):
        pass

    def off(color, style=None): 
        pass


    def connected(self):
        #for client in self.clients:
        #    client.send_message("new client Connected");
        self.clients.append(self)

    def handle_close(self):
        self.clients.remove(self)
        #for client in self.clients:
            #client.send_message(self.address[0] + u" - disconnected")


server = WebSocketServer("", 8000, SimpleChat)
server.serve_forever()
