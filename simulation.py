import pygame
import math
import random
import time

class Button:
    def __init__(self, size, position, color, t):
        self.size = size
        self.position = position
        self.color = color
        self.t = t

    def draw(self, screen):
        pass


class CelestialBody:
    def __init__(self, size, position, color, t_increment):
        self.size = size
        self.position = position
        self.color = color
        self.t = 0
        self.t_increment = t_increment

    def createBody(self, screen, center_x, center_y, a, b):
        distance_x, distance_y = center_x - a, center_y - b
        pygame.draw.ellipse(screen, (255, 255, 255), (distance_x, distance_y, a*2, b*2), width=1)

        self.position, self.t = self.createOrbit(center_x, center_y, a, b, self.t, self.t_increment)
            
        pygame.draw.circle(screen, self.color, self.position, self.size)
    
    def createOrbit(self, center_x, center_y, a, b, t, t_increment):
        x = center_x + a * math.cos(t)
        y = center_y + b * math.cos(t)

        t += t_increment
        return (x, y), t


def solarSystem(screen, domain, reach):
    center_x, center_y = domain // 2, reach // 2

    sun_a, sun_b = 0, 0
    sun = CelestialBody(100, (center_x, center_y), (255, 245, 237), 0)
    sun.createBody(screen, center_x, center_y, sun_a, sun_b)

    earth_a, earth_b = 300, 300
    t_earth_increment = 0.01
    earth = CelestialBody(25, (center_x + earth_a, center_y), (28, 163, 236), t_earth_increment)
    earth.createBody(screen, center_x, center_y, earth_a, earth_b)


def createUniverse(screen, domain, reach):
    size = 1
    amount = 2500
    positions = [] # Verscheidene kleuren toevoegen?

    for position in range(0, amount):
        position_x = random.randint(0, domain)
        position_y = random.randint(0, reach)
        position = (position_x, position_y)
        positions.append(position)

    for star in range(0, amount):
        pygame.draw.circle(screen, (255, 255, 255), positions[star], size)


def switchScene(screen, domain, reach, POI):
    match POI:
            case 1:
                createUniverse(screen, domain, reach)
            case 2:
                solarSystem(screen, domain, reach)


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    domain, reach = screen.get_size() # Domein is x-as en bereik is y-as
    pygame.display.set_caption("Afstand tot ster")
    clock = pygame.time.Clock()
    running = True
    POI = 1
    amount_of_POIs = 3
    
    screen.fill("black")
    switchScene(screen, domain, reach, POI)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT and POI > 1:
                    screen.fill("black")
                    POI -= 1
                    switchScene(screen, domain, reach, POI)
                if event.key == pygame.K_RIGHT and POI < amount_of_POIs:
                    screen.fill("black")
                    POI += 1
                    switchScene(screen, domain, reach, POI)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()