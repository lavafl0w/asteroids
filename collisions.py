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
    closest_y = max(rect.top, min(circle.position.y, rect.bottom))
    
    # Get the distance from the centre of the circle to the closest points
    circle_coords_dist = pygame.math.Vector2.distance_to(circle.position, (closest_x, closest_y))
    
    # If the distance is within the size of the radius
    if circle_coords_dist <= circle.radius:
        return True
    return False

def player_circle_collision(player: list[pygame.Vector2], circle: CircleShape, debug: dict | None) -> bool:
    '''
    Checks whether a circular object overlaps any edge of the player triangle.

    Triangle edges:
    - nose -> back_left
    - nose -> back_right
    - back_left -> back_right
    '''
    edges = [[player[0], player[1]], [player[0], player[2]], [player[1], player[2]]]

    # P in the collision-math notes: the centre of the circular object.
    circle_centre = circle.position

    for edge in edges:
        edge_a = edge[0]  # A
        edge_b = edge[1]  # B
        edge_direction = edge_b - edge_a  # d

        # Project the circle centre onto the infinite line through A -> B.
        # This gives the raw "how far along the edge?" value t.
        t = (circle_centre - edge_a).dot(edge_direction) / edge_direction.dot(edge_direction)

        # Clamp t so the closest point stays on the finite segment, not the
        # infinite line.
        t = (max(0, min(t, 1)))

        # Q(t): the closest point on this edge to the circle centre.
        point_on_edge = edge_a + edge_direction * t
        circle_coords_dist = pygame.math.Vector2.distance_to(circle.position, point_on_edge)
        
        if circle_coords_dist <= circle.radius:
            return True
    return False

    
