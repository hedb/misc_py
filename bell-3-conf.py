import random
import math

def measure_particle_spin(particle_spin, measurement_used = None):
    measurement_used = measurement_used if measurement_used is not None else random.randint(0, 2) * (2* math.pi/3)
    angle_diff = particle_spin - measurement_used
    p_up = math.cos(angle_diff/2)**2
    is_up = random.random() < p_up
    return is_up


def tests():
    N = 1000
    sum = 0
    for i in range(N):
        assert measure_particle_spin(0, 0) == True
        assert measure_particle_spin(0, math.pi) == False
        sum += 1 if measure_particle_spin(0, math.pi/2) == True else 0
    assert abs(sum/N - 0.5) < 0.1

def main():

    tests()

    N = 10000
    sum = 0
    for i in range(N):
        entangled_particles = [random.random()*2*math.pi]
        entangled_particles.append(2*math.pi - entangled_particles[0])

        alice_result = measure_particle_spin(entangled_particles[0])
        bob_result = measure_particle_spin(entangled_particles[1])
        sum += 1 if alice_result == bob_result else 0

    print(f'N={N}, sum={sum}, sum/N={sum/N}')


if __name__ == "__main__":
    main()

