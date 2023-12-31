import pygame
import sys
import random

# Define colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
BROWN = (218, 160, 109)

# Define road properties
ROAD_WIDTH = 100
CAR_RADIUS = 8
CAR_SPEED = 5
MAX_LEFT_LANE_CARS = 5
MAX_RIGHT_LANE_CARS = 10
MAX_TOP_LANE_CARS = 5
MAX_BOTTOM_LANE_CARS = 10
CAR_DELAY = 30

# Initialize pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Intersection Simulation")

# Initialize clock outside the main loop
clock = pygame.time.Clock()

# Move the initialization of MAX_CAR_X here
MAX_CAR_X = WIDTH

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def check_collision(car1, car2):
    return pygame.Rect(car1[0], car1[1], CAR_RADIUS * 2, CAR_RADIUS * 2).colliderect(pygame.Rect(car2[0], car2[1], CAR_RADIUS * 2, CAR_RADIUS * 2))

def update_game_logic(left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars, left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter):
    # Update positions of left lane cars
    for car in left_lane_cars:
        car[0] += CAR_SPEED

    # Update positions of right lane cars
    for car in right_lane_cars:
        car[0] -= CAR_SPEED

    # Update positions of top lane cars
    for car in top_lane_cars:
        car[1] += CAR_SPEED

    # Update positions of bottom lane cars
    for car in bottom_lane_cars:
        car[1] -= CAR_SPEED

    # Remove cars that have moved out of the screen width or height
    left_lane_cars[:] = [car for car in left_lane_cars if car[0] < WIDTH]
    right_lane_cars[:] = [car for car in right_lane_cars if car[0] > 0]
    top_lane_cars[:] = [car for car in top_lane_cars if car[1] < HEIGHT]
    bottom_lane_cars[:] = [car for car in bottom_lane_cars if car[1] > 0]

    # Handle collisions between left and right lanes
    for left_car in left_lane_cars:
        for right_car in right_lane_cars:
            if check_collision(left_car, right_car):
                if left_car[0] < right_car[0]:
                    right_car[0] = left_car[0] - 2 * CAR_RADIUS
                else:
                    left_car[0] = right_car[0] + 2 * CAR_RADIUS

    # Handle collisions between top and bottom lanes
    for top_car in top_lane_cars:
        for bottom_car in bottom_lane_cars:
            if check_collision(top_car, bottom_car):
                if top_car[1] < bottom_car[1]:
                    bottom_car[1] = top_car[1] - 2 * CAR_RADIUS
                else:
                    top_car[1] = bottom_car[1] + 2 * CAR_RADIUS

    # Count the number of cars entering the left lane
    if random.randint(1, CAR_DELAY) == 1 and len(left_lane_cars) < MAX_LEFT_LANE_CARS:
        left_lane_cars.append([-CAR_RADIUS, HEIGHT // 2 - CAR_RADIUS // 2])
        left_lane_counter += 1

    # Spawn new cars for the right lane
    if len(right_lane_cars) < MAX_RIGHT_LANE_CARS and random.randint(1, CAR_DELAY) == 1:
        right_lane_cars.append([WIDTH, HEIGHT // 2 - CAR_RADIUS // 2])
        right_lane_counter += 1

    # Count the number of cars entering the top lane
    if random.randint(1, CAR_DELAY) == 1 and len(top_lane_cars) < MAX_TOP_LANE_CARS:
        top_lane_cars.append([WIDTH // 2 - CAR_RADIUS // 2, -CAR_RADIUS])
        top_lane_counter += 1

    # Spawn new cars for the bottom lane
    if len(bottom_lane_cars) < MAX_BOTTOM_LANE_CARS and random.randint(1, CAR_DELAY) == 1:
        bottom_lane_cars.append([WIDTH // 2 - CAR_RADIUS // 2, HEIGHT])
        bottom_lane_counter += 1

    return left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter

def draw_on_screen(left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars, left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter):
    screen.fill(BROWN)

    # Draw roads
    pygame.draw.rect(screen, GRAY, (0, HEIGHT // 2 - ROAD_WIDTH // 2, WIDTH, ROAD_WIDTH))  # Bottom road
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT))  # Right road

    # Draw white lines to split the roads
    pygame.draw.line(screen, WHITE, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)  # Split bottom road
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)  # Split right road

    # Draw road names
    font = pygame.font.Font(None, 36)
    text = font.render("Bottom Road", True, WHITE)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2 + ROAD_WIDTH // 4))

    text = font.render("Right Road", True, WHITE)
    rotated_text = pygame.transform.rotate(text, -90)
    screen.blit(rotated_text, (WIDTH // 2 + ROAD_WIDTH // 4, HEIGHT // 4))

    text = font.render("Top Road", True, WHITE)
    rotated_text = pygame.transform.rotate(text, 180)
    screen.blit(rotated_text, (WIDTH // 4, HEIGHT // 2 - ROAD_WIDTH // 2 - ROAD_WIDTH // 4))

    text = font.render("Left Road", True, WHITE)
    rotated_text = pygame.transform.rotate(text, 90)
    screen.blit(rotated_text, (WIDTH // 2 - ROAD_WIDTH // 2 - ROAD_WIDTH // 4, HEIGHT // 4))

    # Draw intersections
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - ROAD_WIDTH // 2, 0, ROAD_WIDTH, ROAD_WIDTH))  # Top
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - ROAD_WIDTH // 2, HEIGHT - ROAD_WIDTH, ROAD_WIDTH, ROAD_WIDTH))  # Bottom
    pygame.draw.rect(screen, GRAY, (0, HEIGHT // 2 - ROAD_WIDTH // 2, ROAD_WIDTH, ROAD_WIDTH))  # Left
    pygame.draw.rect(screen, GRAY, (WIDTH - ROAD_WIDTH, HEIGHT // 2 - ROAD_WIDTH // 2, ROAD_WIDTH, ROAD_WIDTH))  # Right

    # Draw red lines before every intersection
    pygame.draw.line(screen, RED, (WIDTH // 2 - ROAD_WIDTH // 2 - 10, 250), (WIDTH // 2 - ROAD_WIDTH // 2 - 10, HEIGHT - 250), 5)  # Left intersection line
    pygame.draw.line(screen, RED, (WIDTH // 2 + ROAD_WIDTH // 2 + 10, 250), (WIDTH // 2 + ROAD_WIDTH // 2 + 10, HEIGHT - 250), 5)  # Right intersection line
    pygame.draw.line(screen, RED, (350, HEIGHT // 2 - ROAD_WIDTH // 2 - 10), (450, HEIGHT // 2 - ROAD_WIDTH // 2 - 10), 5)  # Top intersection line
    pygame.draw.line(screen, RED, (350, HEIGHT // 2 + ROAD_WIDTH // 2 + 10), (450, HEIGHT // 2 + ROAD_WIDTH // 2 + 10), 5)  # Bottom intersection line

    # Draw left lane cars
    for car in left_lane_cars:
        pygame.draw.circle(screen, RED, (int(car[0]), int(car[1])), CAR_RADIUS)

    # Draw right lane cars
    for car in right_lane_cars:
        pygame.draw.circle(screen, RED, (int(car[0]), int(car[1])), CAR_RADIUS)

    # Draw top lane cars
    for car in top_lane_cars:
        pygame.draw.circle(screen, RED, (int(car[0]), int(car[1])), CAR_RADIUS)

    # Draw bottom lane cars
    for car in bottom_lane_cars:
        pygame.draw.circle(screen, RED, (int(car[0]), int(car[1])), CAR_RADIUS)

    # Display left lane car count
    text = font.render(f"Left Lane Cars: {left_lane_counter}", True, WHITE)
    screen.blit(text, (10, 360))

    # Display top lane car count
    text = font.render(f"Top Lane Cars: {top_lane_counter}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 100, 20))

    # Display right lane car count
    text = font.render(f"Right Lane Cars: {right_lane_counter}", True, WHITE)
    screen.blit(text, (WIDTH - 250, HEIGHT // 2 + 50))

    # Display bottom lane car count
    text = font.render(f"Bottom Lane Cars: {bottom_lane_counter}", True, WHITE)
    screen.blit(text, (WIDTH - 480, 560))

    pygame.display.flip()  # Update the display

# Initialize left and right lane cars, top and bottom lane cars
left_lane_cars = []
right_lane_cars = []
top_lane_cars = []
bottom_lane_cars = []

# Initialize left lane, top lane, right lane, and bottom lane counters
left_lane_counter = 0
top_lane_counter = 0
right_lane_counter = 0
bottom_lane_counter = 0

# Main game loop
running = True
while running:
    running = handle_events()
    left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter = update_game_logic(left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars, left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter)
    draw_on_screen(left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars, left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter)
    clock.tick(30)  # Set the frame rate

pygame.quit()
sys.exit()
