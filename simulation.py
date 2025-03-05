import pygame
import math
import random
import time

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

class Button:
    def __init__(self, size, position, color, t):
        self.size = size
        self.position = position
        self.color = color
        self.t = t

    def draw(self, screen):
        pass


class CelestialBody:
    def __init__(self, size, color, t_increment, a, b):
        self.size = size
        self.position = (0, 0)
        self.color = color
        self.t_increment = t_increment
        self.a = a
        self.b = b
        self.t = 0

    def createBody(self, screen, center_x, center_y):
        distance_x, distance_y = center_x - self.a, center_y - self.b
        pygame.draw.ellipse(screen, (255, 255, 255), (distance_x, distance_y, self.a*2, self.b*2), width=1)

        self.position = self.createOrbit(center_x, center_y)
            
        pygame.draw.circle(screen, self.color, self.position, self.size)
    
    def createOrbit(self, center_x, center_y):
        x = center_x + self.a * math.cos(self.t)
        y = center_y + self.b * math.sin(self.t)

        self.t += self.t_increment
        return (x, y)


def solarSystem():
    sun = CelestialBody(200, (255, 240, 200), 0, 0, 0) # 255, 245, 237

    earth_a, earth_b = 500, 500 # Aanpassen voor kleinere schermen
    t_earth_increment = 0.01
    earth = CelestialBody(25, (28, 163, 236), t_earth_increment, earth_a, earth_b)

    return sun, earth

def xRayBinaryStar():
    scorpiiV818 = CelestialBody(150, (255, 200, 100), 0, 0, 0)

    sco_a, sco_b = 400, 400
    t_sco_increment = 0.1
    scorpiusX1 = CelestialBody(10, (28, 163, 236), t_sco_increment, sco_a, sco_b)

    return scorpiiV818, scorpiusX1

def switchScene(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1):
    match POI:
            case 1:
                createUniverse(screen, domain, reach)
            case 2:
                sun.createBody(screen, domain // 2, reach // 2)
                earth.createBody(screen, domain // 2, reach // 2)
            case 3:
                scorpiiV818.createBody(screen, domain // 2, reach // 2)
                scorpiusX1.createBody(screen, domain // 2, reach // 2)
                
def parallaxSimulation(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1):
    POI = 2
    switchScene(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1)

    print(earth.position)
    if earth.position == (945.400238849355, 1039.7868015207525):
        earth.t_increment = 0
        pygame.draw.line(screen, (255, 255, 255), earth.position, (0, 0))
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    domain, reach = screen.get_size() # Domein is x-as en bereik is y-as
    pygame.display.set_caption("Afstand tot ster")
    clock = pygame.time.Clock()
    running = True

    POI = 1
    amount_of_POIs = 3
    parallax_simulation = False

    sun, earth = solarSystem()
    scorpiiV818, scorpiusX1 = xRayBinaryStar()

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
                if event.key == pygame.K_RIGHT and POI < amount_of_POIs:
                    screen.fill("black")
                    POI += 1
                if event.key == pygame.K_SPACE:
                    parallax_simulation = True

        screen.fill("black")
        if not parallax_simulation:
            switchScene(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1)
        else:
            parallaxSimulation(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()