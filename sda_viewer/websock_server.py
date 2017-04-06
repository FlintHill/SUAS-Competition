from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import random

clients = []
class SDAViewSocket(WebSocket):

    def handleMessage(self):
       for client in clients:
          if client == self:
             # change everything below this to JSON data of the drone's latitude, longitude, altitude, and bearing
             obstacle = False
             if bool(random.getrandbits(1)) == True:
              obstacle = "false"
             else:
              obstacle = "true"
             data = '{"obstacle_present":' + obstacle + ', "alt": ' + str(22 * random.random()) + ', "dir": ' + str(44 * random.random()) + ', "speed": ' + str(33 * random.random()) + ', "vert_speed": ' + str(55 * random.random()) + ', "lat": ' + str(38.8712152 + random.random()) + ', "long": ' + str(-77.319965 + random.random()) + "}"
             # keep this
             client.sendMessage(unicode(data)) # self.address[0] +

    def handleConnected(self):
       print(self.address, 'connected')
       for client in clients:
          client.sendMessage(self.address[0] + u' - connected')
       clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')

server = SimpleWebSocketServer('', 8000, SDAViewSocket)
server.serveforever()
