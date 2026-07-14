import pygame

def draw_debug(screen: pygame.Surface, debug_data:dict | None) -> None:
    if debug_data is None:
        return
    draw_offset = [[20, -20], [-90, +10], [20, 10]]
    font_debug = pygame.font.SysFont(None, 20)
    for _ in debug_data.items():
        i = 0
        # player points
        for item in debug_data["points"]:
            pygame.draw.circle(screen, "green", item, 3)
            truncated_x = int(item[0])
            truncated_y = int(item[1])
            font_coord = font_debug.render(f"({truncated_x}, {truncated_y})", True, (255,255,255))
            screen.blit(font_coord, (item[0] + draw_offset[i][0], item[1] + draw_offset[i][1]))
            i += 1
        # edge line
        pygame.draw.line(screen, "blue", debug_data["edge"][0], debug_data["edge"][1], 3)
        # closest point
        pygame.draw.circle(screen, "orange", debug_data["edge_point"], 3)
        font_coord = font_debug.render(f"({int(debug_data['edge_point'][0])}, {int(debug_data['edge_point'][1])})", True, (255,255,255))
        screen.blit(font_coord, (debug_data["centre"][0], debug_data["centre"][1]))
        # centre to closest
        pygame.draw.line(screen, "red", debug_data["centre"], debug_data["edge_point"], 3)
    
    #if debug is not None:
    #    if "dist" not in debug or debug["dist"] > circle_coords_dist:
    #        debug["dist"] = circle_coords_dist        
    #        debug["closest"] = (closest_x, closest_y)               
    #    debug["centre"] = circle.position
    #    debug["points"] = [player[0], player[1], player[2]]
    #    debug["dist"] = float("inf")
    #        if debug is not None:
#            if circle_coords_dist < debug["dist"]:
#                debug["dist"] = circle_coords_dist
#                debug["edge"] = [edge[0], edge[1]]
#                debug["edge_point"] = point_on_edge
