from typing import cast
from circle_shape import CircleShape, TriangleShape
import pygame
from asteroid import Asteroid

def collides(shape_1: CircleShape, shape_2: CircleShape) -> bool:
    """ Master Collision Check / Router
    
    This is the collision check dispatcher to keep things simple.
    Takes the arguments passed in and if no result, flips them and tries again.
    """
    attempt = 0
    while attempt < 2:
        match shape_1.hitbox_kind, shape_2.hitbox_kind:
            case "circle", "circle":
                return circle_vs_circle(
                    cast(CircleShape, shape_1.get_hitbox()),
                    cast(CircleShape, shape_2.get_hitbox()),
                )
            case "circle", "rect":
                return circle_vs_rect(
                    cast(CircleShape, shape_1.get_hitbox()),
                    cast(pygame.Rect, shape_2.get_hitbox()),
                )
            case "triangle", "circle":
                return triangle_vs_asteroid(
                    cast(TriangleShape, shape_1.get_hitbox()),
                    cast(Asteroid, shape_2),
                )
            case "triangle", "rect":
                return triangle_vs_rect(
                    cast(TriangleShape, shape_1.get_hitbox()),
                    cast(pygame.Rect, shape_2.get_hitbox()),
                )
            case "triangle", "asteroid":
                return triangle_vs_asteroid(
                    cast(TriangleShape, shape_1.get_hitbox()),
                    cast(Asteroid, shape_2)
                )
            case _:
                if attempt == 1: # If this is the second pass after they were flipped
                    break
                shape_1, shape_2 = shape_2, shape_1 # Flip them about
                attempt += 1
                    
    raise NotImplementedError(
        f"Collision case not found for object_1: {shape_1.__class__.__name__}" +
        f" and object_2: {shape_2.__class__.__name__}")

def circle_vs_circle(circle_1: CircleShape, circle_2: CircleShape) -> bool:
    """ Bomb Explosion / Asteroid -- Circle / Circle """
    # Calculate distance between center of each CircleShape object
    center_distances = pygame.math.Vector2.distance_to(circle_1.position, circle_2.position)
    
    # When distance between center points is the same or less than both radius's put together --- return true
    if center_distances <= (circle_1.radius + circle_2.radius):
        return True
        
    return False

# TODO: Implement this maybe
def asteroid_vs_asteroid(asteroid_1, asteroid_2):
    asteroid_1_points = asteroid_1.get_world_coords()
    asteroid_1_edges = asteroid_1.get_asteroid_edges()
    
    asteroid_2_points = asteroid_2.get_world_coords()
    asteroid_2_edges = asteroid_2.get_asteroid_edges()
    
    
def triangle_overlaps_circle(triangle: TriangleShape, circle: CircleShape) -> bool:
    """ Player / Asteroid -- Triangle / Circle
    
    Checks whether a circular object overlaps any edge of the triangle.
    Triangle edges:
    - nose -> back_left
    - nose -> back_right
    - back_left -> back_right
    """
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

def triangle_vs_rect(triangle: TriangleShape, rect: pygame.Rect) -> bool:
    """ Player / Item -- Triangle / Rect """
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

def triangle_vs_asteroid(triangle: TriangleShape, asteroid: Asteroid) -> bool:
    
    asteroid_centre = asteroid.position
    if point_in_triangle(triangle, asteroid_centre):
        return True
    
    asteroid_coords_points = asteroid.get_world_coords()
    for point in asteroid_coords_points:
        if point_in_triangle(triangle, point):
            return True
        
    triangle_edges = [[triangle[0], triangle[1]], [triangle[0], triangle[2]], [triangle[1], triangle[2]]]
    
    asteroid_edges = asteroid.get_asteroid_edges()
    #for point_index in range(0, len(asteroid_coords_points) - 1):
    #    asteroid_edges.append([asteroid_coords_points[point_index], 
    #                           asteroid_coords_points[point_index + 1]])
    #asteroid_edges.append([asteroid_coords_points[-1], asteroid_coords_points[0]])

    for triangle_edge in triangle_edges:
        for asteroid_edge in asteroid_edges:
            intersects = check_line_segements_intersect(triangle_edge[0], triangle_edge[1], asteroid_edge[0], asteroid_edge[1])
            if intersects:
                return True
    
    return False

def point_in_triangle(triangle: TriangleShape, point: tuple[int, int] | pygame.Vector2) -> bool:
    """ Check if a given point is contained within the triangle """
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

def check_line_segements_intersect(point_a, point_b, point_c, point_d) -> bool:
    """Check if a given line segement between AB and CD intersect each other."""
    
    ab = point_b - point_a
    ac = point_c - point_a
    ad = point_d - point_a
    
    # Calculate cross product for A(C/D), which can determine the side the vector
    # points relative to AB
    cross_ac = ab.cross(ac)
    cross_ad = ab.cross(ad)
    
    cd = point_d - point_c
    ca = point_a - point_c
    cb = point_b - point_c
    
    # This calculates C(A/B) relative to CD. This is needed as CD can technically 
    # be on the left/right side of AB, but outside the bounds of the line
    cross_ca = cd.cross(ca)
    cross_cb = cd.cross(cb)
    
    # Since cross product returns +ve for one side, -ve for the other
    # You can multiply them and check if the result is -ve (+ve * -ve = -ve)
    if (cross_ac * cross_ad < 0) and (cross_ca * cross_cb < 0):
        return True # Lines intersect
    
    return False

#* Not in use
def circle_vs_rect(circle: CircleShape, rect:pygame.Rect) -> bool: 
    raise Exception("circle_vs_rect collision isn't used right now, you need to reennable it")
#//    # This takes the center position of the circle, and finds the closest point within the bounds of the Rect
#//    # If circle x is left of Rect - use that.. right of Rect - use that, somewhere in the middle, circle x
#//    closest_x = max(rect.left, min(circle.position.x, rect.right))
#//    closest_y = max(rect.top, min(circle.position.y, rect.bottom))
#//    
#//    # Get the distance from the centre of the circle to the closest points
#//    circle_coords_dist = pygame.math.Vector2.distance_to(circle.position, (closest_x, closest_y))
#//    
#//    # If the distance is within the size of the radius
#//    if circle_coords_dist <= circle.radius:
#//        return True
#//    
#//    return False