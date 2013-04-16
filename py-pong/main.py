import pypong, socket, struct, threading
from pypong.player import BasicAIPlayer, Player
import RPi.GPIO as GPIO
player_left = None # set the players as global so the control thread has access
player_right = None # simplest way to do it
def run():
    global player_left, player_right
    configuration = {
        'screen_size': (5800,2430),
        'paddle_image': 'assets/paddle.png',
        'paddle_left_position': 84.,
        'paddle_right_position': 5716.,
        'paddle_velocity': 120.,
        'paddle_bounds': (1, 2420),  
        'line_image': 'assets/dividing-line.png',
        'ball_image': 'assets/ball.png',
        'ball_velocity': 80.,
        'ball_velocity_bounce_multiplier': 1.105,
        'ball_velocity_max': 130.,
    }
    #make a socket, and connect to a already running server socket
    # read some file with the ip addresses and put them in the variables ip addersses
    # hard coded for now but read from a file will be added
    clisocket = [ None, None, None, None, None, None ]
    ip_addresses = ( '10.10.0.10', '10.10.0.11', '10.10.0.12', '10.10.0.13','10.10.0.14', '10.10.0.15' )
    for x in range(0,len( clisocket )):
        clisocket[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clisocket[x].connect((ip_addresses[x], 20000))

    # Prepare game
    player_left = Player(None, 'up', 'down')
    player_right = Player(None, 'up', 'down')
    
    #player_left = BasicAIPlayer()
    #player_right = BasicAIPlayer()
    game = pypong.Game(player_left, player_right, configuration)
    controls = RPIGPIO()
    controls.start()
    # Main game loop
    while game.running:
        game.update()
        posvect = struct.pack('iiii', game.ball.position_vec[0], game.ball.position_vec[1], \
            game.paddle_left.rect.y, game.paddle_right.rect.y )
        # loop over clients and send the coordinates
        for x in range( 0,len( clisocket ) ):
            clisocket[x].sendall( posvect ) 
        # wait for them to send stuff back to avoid a race condition.
        for x in range( 0,len( clisocket ) ):
            clisocket[x].recv( 16 )

class RPIGPIO( threading.Thread ):
    def run( self ):
        global player_left, player_right
        GPIO.setwarnings( False )
        GPIO.setmode( GPIO.BOARD )
        up1 = 7
        down1 = 11
        up2 = 13
        down2 = 15
        GPIO.setup( up1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        GPIO.setup( down1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        GPIO.setup( up2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        GPIO.setup( down2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

        while True:
            if GPIO.input( up1 ):
                player_left.input_state = 'up'
            elif GPIO.input( down1 ):
                player_left.input_state = 'down'
            else:
                player_left.input_state = None

            if GPIO.input( up2 ):
                player_right.input_state = 'up'
            elif GPIO.input( down2 ):
                player_right.input_state = 'down'
            else:
                player_right.input_state = None
        
if __name__ == '__main__': run()
