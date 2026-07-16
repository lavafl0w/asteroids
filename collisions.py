from typing import cast
from circleshape import CircleShape, TriangleShape
import pygame

# COLLISION LOGIC #

# Master Collision Check / Router
def collides(shape_1: CircleShape, shape_2: CircleShape) -> bool:
    '''
    This is the collision check dispatcher to keep things simple.
    For now, pass arguments in one of the supported orders:
    triangle -> circle, triangle -> rect, circle -> circle, or circle -> rect.
    '''
    match shape_1.hitbox_kind, shape_2.hitbox_kind:
        case "circle", "circle":
            return circle_overlaps_circle(
                cast(CircleShape, shape_1.get_hitbox()),
                cast(CircleShape, shape_2.get_hitbox()),
            )
        case "circle", "rect":
            return circle_overlaps_rect(
                cast(CircleShape, shape_1.get_hitbox()),
                cast(pygame.Rect, shape_2.get_hitbox()),
            )
        case "triangle", "circle":
            return triangle_overlaps_circle(
                cast(TriangleShape, shape_1.get_hitbox()),
                cast(CircleShape, shape_2.get_hitbox()),
            )
        case "triangle", "rect":
            return triangle_overlaps_rect(
                cast(TriangleShape, shape_1.get_hitbox()),
                cast(pygame.Rect, shape_2.get_hitbox()),
            )
        case _:
            raise NotImplementedError(f"Collision case not found for object_1: {shape_1.__class__.__name__} and object_2: {shape_2.__class__.__name__}")
    
# Bomb Explosion / Asteroid -- Circle / Circle
def circle_overlaps_circle(circle_1: CircleShape, circle_2: CircleShape) -> bool:
    # Calculate distance between center of each CircleShape object
    center_distances = pygame.math.Vector2.distance_to(circle_1.position, circle_2.position)
    
    # When distance between center points is the same or less than both radius's put together --- return true
    if center_distances <= (circle_1.radius + circle_2.radius):
        return True
        
    return False

# Not used currently
def circle_overlaps_rect(circle: CircleShape, rect:pygame.Rect) -> bool: 
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

# Player / Asteroid -- Triangle / Circle
def triangle_overlaps_circle(triangle: TriangleShape, circle: CircleShape) -> bool:
    '''
    Checks whether a circular object overlaps any edge of the player triangle.

    Triangle edges:
    - nose -> back_left
    - nose -> back_right
    - back_left -> back_right
    '''
    edges = [[triangle[0], triangle[1]], [triangle[0], triangle[2]], [triangle[1], triangle[2]]]
    
    # P in the collision-math notes: the centre of the circular object.
    circle_centre = circle.position

    # Check if centre is within triangle // Handles entire circle being
    # contained in triangle
    if point_in_triangle(triangle, circle_centre):
        return True
    
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

# Player / Item -- Triangle / Rect
def triangle_overlaps_rect(triangle: TriangleShape, rect: pygame.Rect) -> bool:
    # Check if any point of rect is inside triangle // handles the case of full rect being contained
    rect_points = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]
    for point in rect_points:
        if point_in_triangle(triangle, point):
            return True
    
    # For each point of the triangle, check if it's inside the rectangle
    for point in triangle:
        if rect.collidepoint(point):
            return True
        
    edges = [[triangle[0], triangle[1]], [triangle[0], triangle[2]], [triangle[1], triangle[2]]]
    # Check if any edge is within the rectangle
    for edge in edges:
        if rect.clipline(edge):
            return True
        
    return False

# Check if a given point is contained within the triangle
def point_in_triangle(triangle: TriangleShape, point: tuple[int, int] | pygame.Vector2) -> bool:
    # Get triangle edges - [A>B, B>C, C>A]
    edges = [[triangle[0], triangle[1]], [triangle[1], triangle[2]], [triangle[2], triangle[0]]]
    # Counter for the point being on the same edge side
    inside_count = 0

    for edge in edges:  
        edge_a = edge[0]  # A
        edge_b = edge[1]  # B
        edge_direction = edge_b - edge_a  # d
        point_vector = point - edge_a # v

        # Cross product of 2D vectors is <, =, or > than 0 depending on
        # which side the point vector is on
        if edge_direction.cross(point_vector) >= 0:
            inside_count += 1 # Point is on the left of triangle edge

    # If point is on the left of all the edges (and so is contained)
    if inside_count == 3:
        return True
    
    return False
            
            