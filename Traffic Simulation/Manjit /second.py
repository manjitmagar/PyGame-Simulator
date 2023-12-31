import pygame
import sys

# Pygame initialization
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def find_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    if denominator == 0:
        return None
    
    intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
    
    return intersection_x, intersection_y

def draw_lanes(screen, road):
    for lane in road:
        pygame.draw.line(screen, WHITE, (lane[0], lane[1]), (lane[2], lane[3]))

def draw_intersection(screen, intersection):
    if intersection:
        pygame.draw.circle(screen, RED, (int(intersection[0]), int(intersection[1])), 5)

def main():
    # Pygame setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Intersection with Two Lanes")

    # Define roads with two lanes each
    horizontal_road = [(50, 200, 350, 200), (50, 250, 350, 250)]
    vertical_road = [(200, 50, 200, 350), (250, 50, 250, 350)]

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        draw_lanes(screen, horizontal_road)
        draw_lanes(screen, vertical_road)
        
        intersection = find_intersection(horizontal_road[0], vertical_road[0])
        draw_intersection(screen, intersection)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
