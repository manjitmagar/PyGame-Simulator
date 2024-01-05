import pygame
import sys
from intersection import handle_events, update_game_logic, draw_on_screen
from constants import WIDTH, HEIGHT, clock

# Initialize pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Intersection Simulation")

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
    left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter = update_game_logic(
        left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars,
        left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter
    )
    draw_on_screen(
        left_lane_cars, right_lane_cars, top_lane_cars, bottom_lane_cars,
        left_lane_counter, top_lane_counter, right_lane_counter, bottom_lane_counter
    )
    clock.tick(30)  # Set the frame rate

pygame.quit()
sys.exit()
