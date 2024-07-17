from particle import *

def schwarzschild_radial_acceleration(radius, radial_velocity, angular_velocity):
    radial_dist = radius - schwarzschild_radius
    radial_acceleration = 1.5 * (radial_velocity ** 2) * schwarzschild_radius / radius / radial_dist
    radial_acceleration -= 0.5 * radial_dist * schwarzschild_radius / (radius ** 3)
    radial_acceleration += radial_dist * (angular_velocity ** 2)
    return radial_acceleration

def schwarzschild_angular_acceleration(radius, radial_velocity, angular_velocity):
    radial_dist = radius - schwarzschild_radius
    return -radial_velocity * angular_velocity * (2 - 3 * schwarzschild_radius / radius) / radial_dist

def schwarzschild_speed(radius, radial_velocity, angular_velocity):
    radial_dist = radius - schwarzschild_radius
    return math.sqrt(
        (radial_velocity * radius / radial_dist) ** 2
        + (angular_velocity ** 2) * (radius ** 3) / radial_dist
    )

class SchwarzschildParticle(Particle):
    def get_radial_acceleration(self, radius, radial_velocity, angular_velocity):
        if radius <= schwarzschild_radius:
            return -radial_velocity
            
        return schwarzschild_radial_acceleration(radius, radial_velocity, angular_velocity)

    def get_angular_acceleration(self, radius, radial_velocity, angular_velocity):
        if radius <= schwarzschild_radius:
            return -angular_velocity

        return schwarzschild_angular_acceleration(radius, radial_velocity, angular_velocity)

    def get_speed(self):
        if self.radius <= schwarzschild_radius:
            return 0
        
        return schwarzschild_speed(self.radius, self.radial_velocity, self.angular_velocity)

    def normalize_speed(self):
        # Normalize velocity to be lightlike
        speed = self.get_speed()
        self.radial_velocity /= speed
        self.angular_velocity /= speed

    def get_lagrangian(self):
        radial_dist = self.radius - schwarzschild_radius
        lagrangian = radial_dist / self.radius
        lagrangian -= (self.radial_velocity ** 2) * self.radius / radial_dist
        lagrangian -= (self.radius * self.angular_velocity) ** 2
        return -math.sqrt(lagrangian)

    def get_radial_momentum(self):
        if self.radius <= schwarzschild_radius:
            return 0

        lagrangian = self.get_lagrangian()
        if lagrangian >= 0:
            return 0

        radial_dist = self.radius - schwarzschild_radius
        radial_momentum = self.radial_velocity * self.radius / radial_dist
        return radial_momentum / -lagrangian

    def get_angular_momentum(self):
        if self.radius <= schwarzschild_radius:
            return 0

        lagrangian = self.get_lagrangian()
        if lagrangian >= 0:
            return 0

        angular_momentum = self.angular_velocity * (self.radius ** 2)
        return angular_momentum / -lagrangian
    
def create_lightlike(position, velocity, color) -> SchwarzschildParticle:
    # Convert position to polar
    radius = math.sqrt(position[0] ** 2 + position[1] ** 2)
    angle = math.atan2(position[1], position[0])

    radial_velocity = (position[0] * velocity[0] + position[1] * velocity[1]) / radius
    angular_velocity = (position[0] * velocity[1] - position[1] * velocity[0]) / (radius ** 2)

    particle = SchwarzschildParticle(radius, angle, radial_velocity, angular_velocity)
    particle.particle_color = color
    particle.normalize_speed()

    return particle