from circleshape import CircleShape
import pygame
import logger
'''
So this needs to be called when: (all shapes are class Rect)

bullet > asteroid (circle/circle)
player > asteroid (triangle/circle)
player > pickup (triangle/rect)
explosion > asteroid (circle/circle)
'''

# Collision logic
def circle_circle_collision(me: CircleShape, other: CircleShape) -> bool:
    # Calculate distance between center of each CircleShape object
    center_distances = pygame.math.Vector2.distance_to(me.position, other.position)
    
    # When distance between center points is the same or less than both radius's put together --- return true
    if center_distances <= (me.radius + other.radius):
        return True
        
    return False

# Currently going to use this for player/bomb until I work out player being a triangle
def circle_rect_collision(circle: CircleShape, rect:pygame.Rect) -> bool: 
    # This takes the center position of the circle, and finds the closest point within the bounds of the Rect
    # If circle x is left of Rect - use that.. right of Rect - use that, somewhere in the middle, circle x
    closest_x = max(rect.left, min(circle.position.x, rect.right))
    closest_y = max(rect.bottom, min(circle.position.y, rect.top))
    
    # Get the distance from the centre of the circle to the closest points
    circle_coords_dist = pygame.math.Vector2.distance_to(circle.position, (closest_x, closest_y))
    
    # If the distance is within the size of the radius
    if circle_coords_dist <= circle.radius:
        return True
    return False

def player_circle_collision(player: list[pygame.Vector2], circle: CircleShape) -> bool:
    '''
    Nose > Back Left
    Nose > Back Right
    Back Left > Back Right
    check closest x, y with circle on each edge
    Nose = (1,1)
    BL = (2,0)
    BR = (0,0)
    
    edges = [[(0,0), (1,1)], [(1,1), (2,0)], [(0,0), (2,0)]]
    
    '''
    
    edges = [[player[1], player[0]], [player[0], player[2]], [player[1], player[2]]]
    
    for edge in edges:
        closest_x = max(edge[0][0], min(circle.position.x, edge[1][0]))
        closest_y = max(edge[0][1], min(circle.position.y, edge[1][1]))
        circle_coords_dist = pygame.math.Vector2.distance_to(circle.position, (closest_x, closest_y))
        
        if circle_coords_dist <= circle.radius:
            return True
    return False