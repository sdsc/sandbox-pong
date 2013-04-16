import math
#from PIL import Image
def rect_from_image(path):
    img = Image.open(path)
    width, height = img.size
    print width,height
    rect = Rect( 0, 0, width, height)
    return rect

class Paddle(object):
    def __init__(self, velocity, image_path, bounds_y, *groups):
        #self.image = image
        #self.rect = rect_from_image(image_path)
        self.rect = Rect( 0, 0, 30, 100)
        self.direction = 0
        self.velocity = velocity
        self.bounds_y = bounds_y
        # Like original pong, we break this up into 8 segments from the edge angle (acute_angle) to pi/2 at the center
        # Changing acute_angle lets us change the extreme edge angle of the paddle.
        acute_angle = .125
        # Build the angles from acute_angle to the first 0.5 center value then append the values going from the
        # second center 0.5 value by using the values we just calculated reversed.
        angles = [acute_angle + (0.5-acute_angle)/3.0 * n for n in xrange(4)]
        angles += map(lambda x: 1 + x * -1, reversed(angles))
        # Final table is the output vector (x,y) of each angle
        self.bounce_table = [(math.cos(n*math.pi-math.pi/2.0), math.sin(n*math.pi-math.pi/2.0)) for n in angles]
        
    def update(self):
        self.rect.y = max(self.bounds_y[0], min(self.bounds_y[1]-self.rect.height, \
            self.rect.y + self.direction * self.velocity))

    def calculate_bounce(self, delta):
        return self.bounce_table[int(round(delta * (len(self.bounce_table)-1)))]
    
class Line(object):
    def __init__(self, rect, *groups):
        self.rect = rect

class Ball(object):
    def __init__(self, velocity, image_path, *groups):
        self.velocity = velocity
        #self.rect = rect_from_image(image_path)
        self.rect = Rect( 0, 0, 96, 96 )
        self.position_vec = [0., 0.]
        self.velocity_vec = [0., 0.]
        
    def update(self):
        self.position_vec[0] += self.velocity_vec[0]
        self.position_vec[1] += self.velocity_vec[1]
        self.rect.x = self.position_vec[0]
        self.rect.y = self.position_vec[1]
    
    def set_position_x(self, value):
        self.position_vec[0] = value
        self.rect.left = value
    position_x = property(lambda self: self.position_vec[0], set_position_x)
        
    def set_position_y(self, value):
        self.position_vec[1] = value
        self.rect.top = value
    position_y = property(lambda self: self.position_vec[1], set_position_y)


    # left in as is, no attempt was made for scoring yet, other projects
# class Score(object):
#     def __init__(self, image_list, *groups):
#         #Sprite.__init__(self, *groups)
#         self.image_list = image_list
#         self.image = None
#         #self.rect = pygame.Rect(0,0,0,0)
#         self.score = 0
    
#     def get_score(self):
#         return self.score_value
        
#     def set_score(self, value):
#         self.score_value = value
#         digit_spacing = 8
#         digit_width = self.image_list[0].get_width()
#         digit_height = self.image_list[0].get_height()
#         values = map(int, reversed(str(self.score_value)))
#         surface_width = len(values) * digit_width + (len(values)-1) * digit_spacing
#         if not self.image or self.image.get_width() < surface_width:
#             #self.image = pygame.Surface((surface_width, digit_height))
#             self.image.fill((0,0,0))
#             self.rect.width = self.image.get_width()
#             self.rect.height = self.image.get_height()
#         offset = self.image.get_width()-digit_width
#         for i in values:
#             self.image.blit(self.image_list[i], (offset, 0))
#             offset = offset - (digit_width + digit_spacing)

class Rect( object ):
    # 
    def __init__( self, x, y, width, height ):        
        self.width, self.height = width, height
        self._x, self._y =  x, y 
        self._left = self._x
        self._right = self._x + self.width
        self._top = self._y
        self._bottom = self._y + self.height
        self._center = ( self._x+self.width/2, self._y+self.height/2 )
        self._centerx = self._center[0]
        self._centery = self._center[1]
        self._topleft = ( self._left, self._top )
        self._bottomleft = ( self._left, self._bottom )
        self._topright = ( self._right, self._top )
        self._bottomright = ( self._right, self._bottom )

    @property
    def x( self ):
        return self._x

    @x.setter
    def x( self, value ):
        self._x = value
        #update things based on x value
        self._left = self._x
        self._right = self._x + self.width
        self._topleft = ( self._left, self._top )
        self._bottomleft = ( self._left, self._bottom )
        self._topright = ( self._right, self._top )
        self._bottomright = ( self._right, self._bottom )
        self._centerx = self._x + self.width/2 

    @property
    def y( self ):
        return self._y
    @y.setter
    def y( self, value ):
        self._y = value
        self._top = self._y
        self._bottom = self._y + self.height
        self._topleft = ( self._left, self._top )
        self._bottomleft = ( self._left, self._bottom )
        self._topright = ( self._right, self._top )
        self._bottomright = ( self._right, self._bottom )
        self._centery = self._y + self.height/2
    @property
    def top( self ):
        return self._top
    @top.setter
    def top( self, value ):
        self.y = value #Changing the y coordinate will update everything

    @property
    def bottom(self):
        return self._bottom
    @bottom.setter
    def bottom( self, value ):
        self.y = value - self.height #will set the y coordinate correctly.

    @property
    def right( self ):
        return self._right
    @right.setter
    def right( self, value ):
        self.x = value - self.width #it's just the x coordinate + width so set reverse

    @property
    def left( self ):
        return self._left
    @left.setter
    def left( self, value ):
        self.x = value #it's just the x coordinate 

    @property
    def topleft( self ):
        return self._topleft
    @topleft.setter
    def topleft( self, coordinate_tuple ):
        self.x = coordinate_tuple[0] #setting left is the same as setting x
        self.y = coordinate_tuple[1] #setting top is same as setting y

    @property
    def center( self ):
        return ( self.centerx, self.centery )
    @center.setter
    def center ( self, value ):
        self.centerx = value[0]
        self.centery = value[1]

    @property
    def centerx( self ):
        return self._centerx
    @centerx.setter
    def centerx( self, value ):
        #self._centerx = value
        self.x = value-self.width/2

    @property
    def centery( self ):
        return self._centery
    @centery.setter
    def centery( self, value ):
        #self._centery = value
        self.y = value - self.height/2

    def colliderect( self, other_rect ):
        # simple colision detection for 2d rects. Won't check non opposing edges, i.e.
        # self.left won't collide with rect.left
        # outside_left = self.left < other_rect.right and self.bottom <= other_rect.top 

        # outside_right = ( self.right < other_rect.left and self.left > other_rect.right )\
        #      and( self.bottom <= other_rect.top and self.top >= other_rect.bottom )

        # outside_top = ( self.top < other_rect.bottom and self.bottom > other_rect.top )\
        #      and( self.left <= other_rect.right and self.right >= other_rect.left )

        # outside_bottom = ( self.bottom < other_rect.top and self.top > other_rect.bottom )\
        #      and( self.left <= other_rect.right and self.right >= other_rect.left )
        outside_left = ( self.left < other_rect.right and self.right > other_rect.left )\
                     and( self.bottom <= other_rect.top and self.top >= other_rect.bottom )

        outside_right = ( self.right < other_rect.left and self.left > other_rect.right )\
             and( self.bottom <= other_rect.top and self.top >= other_rect.bottom )

        outside_top = ( self.top < other_rect.bottom and self.bottom > other_rect.top )\
             and( self.left <= other_rect.right and self.right >= other_rect.left )

        outside_bottom = ( self.bottom < other_rect.top and self.top > other_rect.bottom )\
             and( self.left <= other_rect.right and self.right >= other_rect.left )

        return outside_right or outside_left or outside_top or outside_bottom
        
