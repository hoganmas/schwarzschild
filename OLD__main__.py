import pygame
import random
import math
from schwarzschild import *
from newtonian import *
from particle import *

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
pygame.display.set_caption("Particle Trail")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Particle properties
particle_size = 5
trail_length = 2048

# angular_velocity = 0.003
# radius = ((schwarzschild_radius * 0.5) ** (1 / 3)) * (angular_velocity ** (-2 / 3))

radius = 8 * schwarzschild_radius
angular_velocity = math.sqrt(schwarzschild_radius * 0.5) * (radius ** (-3 / 2))
angular_velocity *= 1.9

# Make trajectory light-like
radial_dist = radius - schwarzschild_radius
radial_velocity = -math.sqrt(
    (radial_dist / radius) ** 2
    - radius * radial_dist * (angular_velocity ** 2)
)

schwarzschild_particle = SchwarzschildParticle(radius, 0, radial_velocity, angular_velocity)
schwarzschild_particle.particle_color = (255, 0, 0)

newtonian_particle = NewtonianParticle(radius, 0, radial_velocity, angular_velocity)
newtonian_particle.particle_color = (0, 0, 255)

# Main loop flag
running = True
ms_per_frame = 10
ticks_per_frame = 1
time_per_tick = 2

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the particle
    for _ in range(ticks_per_frame):
        schwarzschild_particle.tick(time_per_tick)
        newtonian_particle.tick(time_per_tick)

    # print("angular momentum of newtonian: {}".format(newtonian_particle.get_angular_momentum()))
    # print("hamiltonian of newtonian: {}".format(newtonian_particle.get_hamiltonian()))
    print("speed of newtonian: {}".format(newtonian_particle.get_speed()))

    # print("angular momentum of schwarzschild: {}".format(schwarzschild_particle.get_angular_momentum()))
    # print("hamiltonian of schwarzschild: {}".format(schwarzschild_particle.get_hamiltonian() - 1))
    print("speed of schwarzschild: {}".format(schwarzschild_particle.get_speed()))

    # Clear screen
    screen.fill(white)

    # Draw the Black Hole
    pygame.draw.circle(screen, black, (screen.get_width() / 2, screen.get_height() / 2), schwarzschild_radius)

    # Draw the particle
    schwarzschild_particle.draw(screen)
    newtonian_particle.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(ms_per_frame)

# Quit Pygame
pygame.quit()
