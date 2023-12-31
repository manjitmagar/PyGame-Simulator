import pygame
import sys
import random

# Define colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
Brown = (218, 160, 109)

# Define road properties
ROAD_WIDTH = 100
LANE_WIDTH = 20  # Width of each lane
CAR_RADIUS = 8  # Set the radius of the circular car
CAR_SPEED = 5
MAX_LEFT_LANE_CARS = 5
MAX_RIGHT_LANE_CARS = 10
MAX_TOP_LANE_CARS = 5
MAX_BOTTOM_LANE_CARS = 10
CAR_DELAY = 30  # frames between car spawns

# Define the number of lanes for each direction
NUM_LEFT_LANES = 4
NUM_RIGHT_LANES = 4
NUM_TOP_LANES = 4
NUM_BOTTOM_LANES = 4

# Initialize pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Intersection Simulation")

# Initialize clock outside the main loop
clock = pygame.time.Clock()

# Move the initialization of MAX_CAR_X here
MAX_CAR_X = WIDTH  # Adjust this value based on your requirements

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def check_collision(car, other_cars):
    for other_car in other_cars:
        distance = ((car[0] - other_car[0]) ** 2 + (car[1] - other_car[1]) ** 2) ** 0.5
        if distance < 2 * CAR_RADIUS:
            return True  # Collision detected
    return False

def update_game_logic(left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars, left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter):
    for cars in left_lane_cars:
        for car in cars:
            car[0] += CAR_SPEED
            if check_collision(car, [other_car for other_cars in left_lane_cars for other_car in other_cars if other_cars != cars]):
                car[0] -= CAR_SPEED  # Move back if collision occurs

    for cars in right_lane_cars:
        for car in cars:
            car[0] -= CAR_SPEED
            if check_collision(car, [other_car for other_cars in right_lane_cars for other_car in other_cars if other_cars != cars]):
                car[0] += CAR_SPEED  # Move back if collision occurs

    for cars in top_lane_cars:
        for car in cars:
            car[1] += CAR_SPEED
            if check_collision(car, [other_car for other_cars in top_lane_cars for other_car in other_cars if other_cars != cars]):
                car[1] -= CAR_SPEED  # Move back if collision occurs

    for cars in bottom_lane_cars:
        for car in cars:
            car[1] -= CAR_SPEED
            if check_collision(car, [other_car for other_cars in bottom_lane_cars for other_car in other_cars if other_cars != cars]):
                car[1] += CAR_SPEED  # Move back if collision occurs

    # Remove cars that have moved out of the screen width or height
    left_lane_cars[:] = [[car for car in cars if car[0] < WIDTH] for cars in left_lane_cars]
    right_lane_cars[:] = [[car for car in cars if car[0] > 0] for cars in right_lane_cars]
    top_lane_cars[:] = [[car for car in cars if car[1] < HEIGHT] for cars in top_lane_cars]
    bottom_lane_cars[:] = [[car for car in cars if car[1] > 0] for cars in bottom_lane_cars]

    # Count the number of cars entering the left lane
    if random.randint(1, CAR_DELAY) == 1 and len(left_lane_cars[0]) < MAX_LEFT_LANE_CARS and left_lane_counter < MAX_LEFT_LANE_CARS:
        new_car = [0, HEIGHT // 2 - CAR_RADIUS // 2]
        if not check_collision(new_car, [other_car for other_cars in left_lane_cars for other_car in other_cars]):
            left_lane_cars[0].append(new_car)
            left_lane_counter += 1

    # Spawn new cars with a delay if the maximum number of cars is not reached for the right lane
    if len(right_lane_cars[0]) < MAX_RIGHT_LANE_CARS and random.randint(1, CAR_DELAY) == 1:
        new_car = [WIDTH, HEIGHT // 2 - CAR_RADIUS // 2]
        if not check_collision(new_car, [other_car for other_cars in right_lane_cars for other_car in other_cars]):
            right_lane_cars[0].append(new_car)
            right_lane_counter += 1

    # Count the number of cars entering the top lane
    if random.randint(1, CAR_DELAY) == 1 and len(top_lane_cars[0]) < MAX_TOP_LANE_CARS and top_lane_counter < MAX_TOP_LANE_CARS:
        new_car = [WIDTH // 2 - CAR_RADIUS // 2, 0]
        if not check_collision(new_car, [other_car for other_cars in top_lane_cars for other_car in other_cars]):
            top_lane_cars[0].append(new_car)
            top_lane_counter += 1

    # Spawn new cars with a delay if the maximum number of cars is not reached for the bottom lane
    if len(bottom_lane_cars[0]) < MAX_BOTTOM_LANE_CARS and random.randint(1, CAR_DELAY) == 1:
        new_car = [WIDTH // 2 - CAR_RADIUS // 2, HEIGHT]
        if not check_collision(new_car, [other_car for other_cars in bottom_lane_cars for other_car in other_cars]):
            bottom_lane_cars[0].append(new_car)
            bottom_lane_counter += 1

    return left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter

def draw_on_screen(left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars, left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter):
    screen.fill(Brown)  # Fill screen with white color

    # Draw roads
    pygame.draw.rect(screen, GRAY, (0, HEIGHT // 2 - ROAD_WIDTH // 2, WIDTH, ROAD_WIDTH))
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT))

    # Draw intersections
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - ROAD_WIDTH // 2, 0, ROAD_WIDTH, ROAD_WIDTH))  # Top
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - ROAD_WIDTH // 2, HEIGHT - ROAD_WIDTH, ROAD_WIDTH, ROAD_WIDTH))  # Bottom
    pygame.draw.rect(screen, GRAY, (0, HEIGHT // 2 - ROAD_WIDTH // 2, ROAD_WIDTH, ROAD_WIDTH))  # Left
    pygame.draw.rect(screen, GRAY, (WIDTH - ROAD_WIDTH, HEIGHT // 2 - ROAD_WIDTH // 2, ROAD_WIDTH, ROAD_WIDTH))  # Right

    # Draw red lines before every intersection
    pygame.draw.line(screen, RED, (WIDTH // 2 - ROAD_WIDTH // 2 - 10, HEIGHT // 2), (WIDTH // 2 - ROAD_WIDTH // 2 - 10, HEIGHT - 250), 5)  # Left intersection line
    pygame.draw.line(screen, RED, (WIDTH // 2 + ROAD_WIDTH // 2 + 10, HEIGHT // 2), (WIDTH // 2 + ROAD_WIDTH // 2 + 10, HEIGHT - 250), 5)  # Right intersection line
    pygame.draw.line(screen, RED, (WIDTH // 2, HEIGHT // 2 - ROAD_WIDTH // 2 - 10), (WIDTH // 2, HEIGHT // 2 + ROAD_WIDTH // 2 + 10), 5)  # Top intersection line
    pygame.draw.line(screen, RED, (WIDTH // 2, HEIGHT // 2 + ROAD_WIDTH // 2 + 10), (WIDTH // 2, HEIGHT - 250), 5)  # Bottom intersection line

    # Draw lanes
    lane_positions = [(WIDTH // 2 - LANE_WIDTH // 2, 0), (WIDTH // 2 - LANE_WIDTH // 2, HEIGHT - LANE_WIDTH),
                      (0, HEIGHT // 2 - LANE_WIDTH // 2), (WIDTH - LANE_WIDTH, HEIGHT // 2 - LANE_WIDTH // 2)]

    for lane_position in lane_positions:
        pygame.draw.rect(screen, WHITE, (*lane_position, LANE_WIDTH, ROAD_WIDTH))

    # Draw left lane cars
    for cars in left_lane_cars:
        for car in cars:
            pygame.draw.circle(screen, RED, (int(car[0]), int(car[1])), CAR_RADIUS)

    # Draw right lane cars
    for cars in right_lane_cars:
        for car in cars:
            pygame.draw.circle(screen, RED, (int(car[0]), int(car[1])), CAR_RADIUS)

    # Draw top lane cars
    for cars in top_lane_cars:
        for car in cars:
            pygame.draw.circle(screen, RED, (int(car[0]), int(car[1])), CAR_RADIUS)

    # Draw bottom lane cars
    for cars in bottom_lane_cars:
        for car in cars:
            pygame.draw.circle(screen, RED, (int(car[0]), int(car[1])), CAR_RADIUS)

    # Display left lane car count
    font = pygame.font.Font(None, 36)
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
left_lane_cars = [[] for _ in range(NUM_LEFT_LANES)]
right_lane_cars = [[] for _ in range(NUM_RIGHT_LANES)]
top_lane_cars = [[] for _ in range(NUM_TOP_LANES)]
bottom_lane_cars = [[] for _ in range(NUM_BOTTOM_LANES)]

# Initialize left lane, top lane, right lane, and bottom lane counters
left_lane_counter = 0
top_lane_counter = 0
right_lane_counter = 0
bottom_lane_counter = 0

# Main game loop
running = True
while running:
    running = handle_events()
    left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter = update_game_logic(
        left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars, left_lane_counter, top_lane_counter,
        right_lane_counter, bottom_lane_counter
    )
    draw_on_screen(left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars, left_lane_counter, top_lane_counter,
                    right_lane_counter, bottom_lane_counter)
    clock.tick(30)  # Set the frame rate

pygame.quit()
sys.exit()
