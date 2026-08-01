import pygame

def draw_debug(screen: pygame.Surface, debug_data:dict) -> None:

    draw_offset = [[20, -20], [-90, +10], [20, 10]]
    font_debug = pygame.font.SysFont(None, 20)
    for _ in debug_data.items():
        i = 0
        # player points
        for item in debug_data["points"]:
            pygame.draw.circle(screen, "green", item, 3)
            truncated_x = int(item[0])
            truncated_y = int(item[1])
            #font_coord = font_debug.render(f"({truncated_x}, {truncated_y})", True, (255,255,255))
            #screen.blit(font_coord, (item[0] + draw_offset[i][0], item[1] + draw_offset[i][1]))
            i += 1
        # edge line
        for list in debug_data["edge"].values():
            pygame.draw.line(screen, list[2], list[0], list[1], 3)
        # closest point
        #pygame.draw.circle(screen, "orange", debug_data["edge_point"], 3)
        #font_coord = font_debug.render(f"({int(debug_data['edge_point'][0])}, {int(debug_data['edge_point'][1])})", True, (255,255,255))
        #screen.blit(font_coord, (debug_data["centre"][0], debug_data["centre"][1]))
        # centre to closest
        #pygame.draw.line(screen, "red", debug_data["centre"], debug_data["edge_point"], 3)
    
def triangle_test(player, centre, debug) -> None:
    debug["points"] = [player[0], player[1], player[2], centre]
    edge_dict = {}
    edges = [[player[0], player[1]], [player[1], player[2]], [player[2], player[0]]]
    
    i = 0
    for edge in edges:
        edge_a = edge[0]  # A
        edge_b = edge[1]  # B
        edge_direction = edge_b - edge_a  # d
        point_vector = centre - edge_a
        
        if edge_direction.cross(point_vector) > 0:
            edge_dict[f"edge {i}"] = [edge[0], edge[1], "green"]
        elif edge_direction.cross(point_vector) < 0:
            edge_dict[f"edge {i}"] = [edge[0], edge[1], "red"]
        else:
            edge_dict[f"edge {i}"] = [edge[0], edge[1], "blue"]
        i += 1
            
    debug["edge"] = edge_dict
    
    #    if "dist" not in debug or debug["dist"] > circle_coords_dist:
    #        debug["dist"] = circle_coords_dist        
    #        debug["closest"] = (closest_x, closest_y)               
    #    debug["centre"] = circle.position
    #    debug["points"] = [player[0], player[1], player[2]]
    #    debug["dist"] = float("inf")
    #
    #    if circle_coords_dist < debug["dist"]:
    #        debug["dist"] = circle_coords_dist
    #        debug["edge"] = [edge[0], edge[1]]
    #        debug["edge_point"] = point_on_edge