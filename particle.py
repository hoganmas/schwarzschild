import math
import numpy as np
import pygame

schwarzschild_radius = 60

def newtonian_radial_acceleration(radius, radial_velocity, angular_velocity):
    return radius * (angular_velocity ** 2) - 0.5 * schwarzschild_radius / (radius ** 2)

def newtonian_angular_acceleration(radius, radial_velocity, angular_velocity):
    return -2 * radial_velocity * angular_velocity / radius


class Particle:
    radius = 2
    angle = 0

    radial_velocity = 1
    angular_velocity = 1

    def __init__(self, radius, angle, radial_velocity, angular_velocity):
        self.radius = radius
        self.angle = angle
        self.radial_velocity = radial_velocity
        self.angular_velocity = angular_velocity
        self.trail = np.empty([0, 2])

    def is_moving(self):
        return self.radial_velocity != 0 or self.angular_velocity != 0

    def tick(self, delta_time):
        if self.radius == schwarzschild_radius:
            self.tick_trail()
            return

        coeffs = [0, 0.5, 0.5, 1]
        k = np.zeros((5, 4))
        for index in range(4):
            coeff = coeffs[index]

            radial_acceleration = self.get_radial_acceleration(
                self.radius + k[index][0] * coeff,
                self.radial_velocity + k[index][2] * 0.5,
                self.angular_velocity + k[index][3] * 0.5
            )
            angular_acceleration = self.get_angular_acceleration(
                self.radius + k[index][0] * coeff,
                self.radial_velocity + k[index][2] * 0.5,
                self.angular_velocity + k[index][3] * 0.5
            )

            k[index + 1] = delta_time * np.array([
                self.radial_velocity + k[index][2] * coeff,
                self.angular_velocity + k[index][3] * coeff,
                radial_acceleration,
                angular_acceleration
            ])

        weights = np.array([0, 1 / 6, 1 / 3, 1 / 3, 1 / 6])
        self.radius += np.dot(k[:,0], weights)
        self.angle += np.dot(k[:,1], weights)
        self.radial_velocity += np.dot(k[:,2], weights)
        self.angular_velocity += np.dot(k[:,3], weights)
        self.tick_trail()

    def tick_trail(self):
        if not self.is_moving():
            self.trail = self.trail[1:,:]
            return

        # Add to trail
        position = self.get_position()
        self.trail = np.vstack([self.trail, position])
        if self.trail.shape[0] > self.trail_length:
            self.trail = self.trail[1:,:]

            
    def get_radial_acceleration(self, radius, radial_velocity, angular_velocity):
        return 0

    def get_angular_acceleration(self, radius, radial_velocity, angular_velocity):
        return 0

    def get_position(self):
        return np.array([
            self.radius * math.cos(self.angle), 
            self.radius * math.sin(self.angle)
        ])
    
    def get_speed(self):
        return math.sqrt(
            (self.radial_velocity ** 2)
            + (self.angular_velocity * self.radius) ** 2
        )
    
    def get_lagrangian(self):
        return 0

    def get_radial_momentum(self):
        return self.radial_velocity

    def get_angular_momentum(self):
        return (self.radius ** 2) * self.angular_velocity

    def get_hamiltonian(self):
        hamiltonian = self.get_radial_momentum() * self.radial_velocity
        hamiltonian += self.get_angular_momentum() * self.angular_velocity
        hamiltonian -= self.get_lagrangian()
        return hamiltonian
    
    particle_size = 1
    particle_color = (0, 0, 0)
    trail_length = 128
    trail = np.empty([0, 2])
    frame_counter = 0
    frames_per_trail = 1
    def draw(self, screen):
        # Draw the trail
        index = 1
        (r, g, b) = self.particle_color
        
        center = 0.5 * np.array([screen.get_width(), screen.get_height()])
        trail_size = self.trail.shape[0]
        for index in range(trail_size):
            trail_position = self.trail[trail_size - index - 1]
            radius = self.particle_size
            hue = (1 - index / self.trail_length) % 1
            color = hsv_to_rgb(hue, 1, 1)
            pygame.draw.circle(screen, color, tuple(trail_position + center), radius)

        # Draw the particle
        # pygame.draw.circle(screen, self.particle_color, tuple(position + center), self.particle_size)

def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - abs((h * 6) % 2 - 1))
    m = v - c
    
    if 0 <= h < 1/6:
        r_prime, g_prime, b_prime = c, x, 0
    elif 1/6 <= h < 2/6:
        r_prime, g_prime, b_prime = x, c, 0
    elif 2/6 <= h < 3/6:
        r_prime, g_prime, b_prime = 0, c, x
    elif 3/6 <= h < 4/6:
        r_prime, g_prime, b_prime = 0, x, c
    elif 4/6 <= h < 5/6:
        r_prime, g_prime, b_prime = x, 0, c
    else:  # 5/6 <= h < 1
        r_prime, g_prime, b_prime = c, 0, x
    
    # Convert to 0-1 range for RGB
    r = r_prime + m
    g = g_prime + m
    b = b_prime + m
    
    # Convert to 0-255 range and return as integers
    return int(r * 255), int(g * 255), int(b * 255)
