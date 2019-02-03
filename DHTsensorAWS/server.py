#Created by- Preshit Harlikar
#Date - 12/08/2018

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import paho.mqtt.client as paho
import asyncio
import aiocoap.resource as resource
import aiocoap

#broker for MQTT
broker="iot.eclipse.org"

# callback function for MQTT
def on_message(client, userdata, message):
#    print("received message =",str(message.payload.decode("utf-8")))
#    print(type(message))
#    client.subscribe("server/profile")
#    time.sleep(10)
    client.publish("server/profile",str(message.payload.decode("utf-8")))  # publish the same message received from client on different topic 

    client.disconnect() #disconnect
    client.loop_stop() #stop loop

# Handler for websocket
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('New WebSocket Connection Opened')


    def on_message(self, message):
        
#        print('Message Received:  %s' % message)
        
        self.write_message(message)     # send the received mesaage back to the client
        
#        print('Message Sent Back: %s' %message)
 
    def on_close(self):
        print('WebSocket Connection Closed')
        tornado.ioloop.IOLoop.instance().stop()     #stop loop

 
    def check_origin(self, origin):
        return True

#Tornado application 
application = tornado.web.Application([
    (r'/ws', WSHandler)
])

# Handler for CoAP
class BlockResource (resource.Resource):
    def __init__(self):
        super().__init__()
        self.set_content(b"This is the resource's default content")
    
    def set_content(self, content):
        self.content = content
##        while len(self.content) <= 64:
##            self.content = self.content + b"0123456789\n"

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)    #message received from client 
        

    async def render_put(self, request):
##        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)               
        return aiocoap.Message(payload=self.content)    #send the message back to the client


 
if __name__ == "__main__":
    client= paho.Client("client-002")   #create client object for MQTT
    ######Bind function to callback
    client.on_message=on_message
    #####
    print("connecting to broker ",broker)
    client.connect(broker)              #connect
    print("subscribing ")
    client.subscribe("client/profile")  #subscribe
    client.loop_forever()               #start loop to process received messages    
    
    http_server = tornado.httpserver.HTTPServer(application)    #create instance for tornado application
    http_server.listen(8888)                                    #start websocket server
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()                    #start loop
    
    # Resource tree creation
    root = resource.Site()
    root.add_resource(('.well-known', 'core'),
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('other', 'block'), BlockResource())      
    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()                      #start loop


