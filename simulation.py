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

class UI:
    def __init__(self, size, color, position):
        self.rect = pygame.Rect(position[0], position[1], 200, 50)
        self.size = size
        self.position = (0, 0)
        self.color = color
        self.position = position
        self.font = pygame.font.Font(None, self.size)

    def text(self, screen, inputText):
        text_surface = self.font.render(inputText, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.position)
        screen.blit(text_surface, text_rect)

    def draw(self, screen): # WORK IN PROGRESS
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render("Hey", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class CelestialBody:
    def __init__(self, size, color, t_increment, a, b, t):
        self.size = size
        self.position = (0, 0)
        self.color = color
        self.t_increment = t_increment
        self.a = a
        self.b = b
        self.t = t

    def createBody(self, screen, center_x, center_y, draw_line):
        distance_x, distance_y = center_x - self.a, center_y - self.b
        pygame.draw.ellipse(screen, (255, 255, 255), (distance_x, distance_y, self.a*2, self.b*2), width=1)

        self.position = self.createOrbit(center_x, center_y)
            
        pygame.draw.circle(screen, self.color, self.position, self.size)

        if draw_line == True:
            pygame.draw.line(screen, (255, 255, 255), self.position, (0, 0))
    
    def createOrbit(self, center_x, center_y):
        x = center_x + self.a * math.cos(self.t)
        y = center_y + self.b * math.sin(self.t)

        self.t += self.t_increment
        return (x, y)


def solarSystem():
    sun = CelestialBody(200, (255, 240, 200), 0, 0, 0, 0) # 255, 245, 237

    earth_a, earth_b = 500, 500 # Aanpassen voor kleinere schermen
    t_earth_increment = 0.01
    earth = CelestialBody(25, (28, 163, 236), t_earth_increment, earth_a, earth_b, 0)

    return sun, earth

def xRayBinaryStar():
    scorpiiV818 = CelestialBody(150, (255, 200, 100), 0, 0, 0, 0)

    sco_a, sco_b = 400, 400
    t_sco_increment = 0.1
    scorpiusX1 = CelestialBody(10, (28, 163, 236), t_sco_increment, sco_a, sco_b, 0)

    return scorpiiV818, scorpiusX1

def switchScene(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1, loaded, draw_line, simulation_process, pause_start_time):
    current_time = time.time()

    match POI:
            case 1:
                if not loaded:
                    loaded = True
                    createUniverse(screen, domain, reach)
                return loaded, draw_line, pause_start_time
            case 2:
                screen.fill("black")
                sun.createBody(screen, domain // 2, reach // 2, False)
                earth.createBody(screen, domain // 2, reach // 2, draw_line)

                if earth.position == (945.400238849355, 1039.7868015207525) and simulation_process:
                    if pause_start_time is None:
                        pause_start_time = current_time
                        loaded = True
                        draw_line = True
                        earth.t_increment = 0
                
                if pause_start_time is not None and current_time - pause_start_time >= 3:
                    earth.t_increment = 0.01
                    pause_start_time = None
                
                return loaded, draw_line, pause_start_time
            case 3:
                screen.fill("black")
                scorpiiV818.createBody(screen, domain // 2, reach // 2, False)
                scorpiusX1.createBody(screen, domain // 2, reach // 2, False)
                return loaded, draw_line, pause_start_time


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    domain, reach = screen.get_size() # Domein is x-as en bereik is y-as
    pygame.display.set_caption("Afstand tot ster")
    clock = pygame.time.Clock()
    running = True

    POI = 1
    amount_of_POIs = 3
    loaded = False
    simulation_process = False
    draw_line = False
    pause_start_time = None

    welcome_text = UI(100, (255, 255, 255), (domain // 2, reach // 2))
    name_and_class = UI(50, (255, 255, 255), (domain // 2, reach // 2 + 100))
    teacher_and_subject = UI(40, (255, 255, 255), (domain // 2, reach // 2 + 150))
    close_text = UI(30, (255, 255, 255), (140, 25))

    start_button = UI(100, (255, 255, 255), (domain // 2, reach // 2))

    sun, earth = solarSystem()
    scorpiiV818, scorpiusX1 = xRayBinaryStar()

    screen.fill("black")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT and POI > 1:
                    loaded = False
                    draw_line = False
                    screen.fill("black")
                    POI -= 1
                if event.key == pygame.K_RIGHT and POI < amount_of_POIs:
                    loaded = False
                    draw_line = False
                    screen.fill("black")
                    POI += 1
                if event.key == pygame.K_SPACE:
                    loaded = False
                    draw_line = False
                    screen.fill("black")
                    earth.t = 0
                    simulation_process = True

        if not simulation_process:
            loaded, draw_line, pause_start_time = switchScene(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1, loaded, draw_line, simulation_process, pause_start_time)
        if simulation_process:
            POI = 2
            loaded, draw_line, pause_start_time = switchScene(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1, loaded, draw_line, simulation_process, pause_start_time)
        
        if POI == 1:
            welcome_text.text(screen, "Afstand tot ster")
            name_and_class.text(screen, "Sven & Aarif V41")
            teacher_and_subject.text(screen, "Dyane Til ANW")
            close_text.text(screen, "ESC / Alt + F4 - afluisten")

            start_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()