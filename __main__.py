import pygame
import random
import math
from schwarzschild import *
from newtonian import *
from particle import *

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1000, 800
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption("Particle Trail")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Particle properties
particle_size = 5
trail_length = 2048

# angular_velocity = 0.003
# radius = ((schwarzschild_radius * 0.5) ** (1 / 3)) * (angular_velocity ** (-2 / 3))

"""
particles = [
    create_lightlike(
        [-screen.get_width() // 2, y], 
        [100, 0],
        (255, 0, 0)
    ) for y in range(-screen.get_height() // 2 + 200, screen.get_height() // 2 - 200, 1)
]
"""

num_particles = 200
y_values = np.concatenate((
    np.arange(schwarzschild_radius, schwarzschild_radius * 2.75, 0.5),
    np.arange(-schwarzschild_radius, schwarzschild_radius, 1.5),
    np.arange(-schwarzschild_radius * 2.75, -schwarzschild_radius, 0.5)
))

particles = [
    create_lightlike(
        [-screen.get_width() // 2, y], 
        [1, 0],
        (255, 0, 0)
    ) for y in y_values
]

# schwarzschild_particle.particle_color = (255, 0, 0)

# Main loop flag
running = True
ms_per_frame = 5
ticks_per_frame = 10
time_per_tick = 1

# Clear screen
screen.fill(white)

# Draw the photon sphere
pygame.draw.circle(screen, (200, 200, 200), (screen.get_width() / 2, screen.get_height() / 2), schwarzschild_radius * 1.5)

# Draw the Black Hole
pygame.draw.circle(screen, black, (screen.get_width() / 2, screen.get_height() / 2), schwarzschild_radius)

# Main loop
time = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    # screen.fill(white)

    # Draw the particle
    for _ in range(ticks_per_frame):
        hue = (time / 1000) % 1
        color = hsv_to_rgb(hue, 1, 1)
        time += time_per_tick

        for particle in particles:
            if (particle.is_moving()):
                particle.normalize_speed()
                particle.tick(time_per_tick)
                particle.draw(screen, color)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(ms_per_frame)

# Quit Pygame
pygame.quit()
