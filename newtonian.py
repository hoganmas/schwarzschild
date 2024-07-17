from particle import *

def newtonian_radial_acceleration(radius, radial_velocity, angular_velocity):
    return radius * (angular_velocity ** 2) - 0.5 * schwarzschild_radius / (radius ** 2)

def newtonian_angular_acceleration(radius, radial_velocity, angular_velocity):
    return -2 * radial_velocity * angular_velocity / radius

class NewtonianParticle(Particle):
    def get_radial_acceleration(self, radius, radial_velocity, angular_velocity):
        if radius <= schwarzschild_radius:
            return -radial_velocity

        return newtonian_radial_acceleration(radius, radial_velocity, angular_velocity)

    def get_angular_acceleration(self, radius, radial_velocity, angular_velocity):
        if radius <= schwarzschild_radius:
            return -angular_velocity

        return newtonian_angular_acceleration(radius, radial_velocity, angular_velocity)

    def get_lagrangian(self):
        lagrangian = 0.5 * (self.radial_velocity ** 2)
        lagrangian += 0.5 * (self.radius * self.angular_velocity) ** 2
        lagrangian += 0.5 * schwarzschild_radius / self.radius
        return lagrangian
