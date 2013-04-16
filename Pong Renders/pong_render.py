import pygame
import sys
import SocketServer, struct

screen = None #setting them as global for now, may be better solution
ball = None
ballrect = None
paddle_left = None #these should be in array, just trying to make it work for now
paddle_left_rect = None
paddle_right = None
paddle_right_rect = None
boundsx = [None, None] #left, right
boundsy = [None, None] #top, bottom
black = 0,0,0

class broadcastServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class requestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        global screen, ball, ballrect, paddle_left_rect, paddle_right_rect, bounds,\
            edge_node, paddle_index
        posvec=self.request.recv(16)
        while posvec !='':
            pos = struct.unpack( 'iiii',posvec )
            ballrect.x = pos[0] - boundsx[0] # offset the bounds
            ballrect.y = pos[1] - boundsy[0] 
            screen.fill( black )
            if ( pos[0] > boundsx[0] and pos[1] < boundsx[1] ):
                screen.blit( ball, ballrect )
            if edge_node:
                if ( pos[paddle_index] > boundsy[0] and pos[paddle_index] < boundsy[1]  ):
                    paddle_rect.y = pos[paddle_index] - boundsy[0]
                    screen.blit( paddle, paddle_rect )
            pygame.display.flip()
            self.request.send( 'Got it' )
            try:
                posvec=self.request.recv( 16 )
            except:
                print( 'client disconnect' )
        #         pygame.quit()
        #         sys.exit()
        # pygame.quit()
        # sys.exit()

def read_pong_settings():
    # put in seperate function since it's special. Could have been done easier
    global  boundx, boundsy, right_edge_node, left_edge_node, ip_address
    settings = open( 'settings.txt', 'r' )
    line = settings.readline()
    boundsx[0] = int( settings.readline().strip() ) 
    line = settings.readline()
    boundsx[1] = int( settings.readline().strip() )
    line = settings.readline()
    boundsy[0] = int( settings.readline().strip() ) 
    line = settings.readline()
    boundsy[1] = int( settings.readline().strip() )
    line = settings.readline()
    right_edge_node = settings.readline().strip() 
    line = settings.readline()
    left_edge_node = settings.readline().strip() 
    line = settings.readline()
    ip_address = settings.readline().strip()
    settings.close()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( (1920,1200) )
    ball = pygame.image.load( 'assets/ball.png' )
    ballrect = ball.get_rect()
    read_pong_settings()
    pygame.mouse.set_visible(False)
    if ( right_edge_node == 'True' ):
        paddle = pygame.image.load( 'assets/paddle.png' )
        paddle_rect = paddle.get_rect()
        paddle_rect.x = 1836 - paddle_rect.width
        edge_node = True #will signal to update paddle as well
        paddle_index = 3
    elif( left_edge_node == 'True' ):
        paddle = pygame.image.load( 'assets/paddle.png' )
        paddle_rect = paddle.get_rect()
        paddle_rect.x = 84
        edge_node = True #will signal to update paddle as well
        paddle_index = 2
    else:
        edge_node = False
    server=broadcastServer( ( ip_address, 20000 ), requestHandler )
    server.serve_forever()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    
    
        
        
