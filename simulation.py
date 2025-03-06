import pygame
import math
import random
import time

def createUniverse(screen, domain, reach, default_reach):
    size = 1
    amount = int(2500 * default_reach)
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
        self.size = int(size)
        self.position = (0, 0)
        self.color = color
        self.position = position
        self.font = pygame.font.Font(None, self.size)

    def text(self, screen, inputText):
        text_surface = self.font.render(inputText, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.position)
        screen.blit(text_surface, text_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render("Hey", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def click(self):
        pass


class CelestialBody:
    def __init__(self, size, color, t_increment, a, b, t, line_positions, stop_positions=None):
        self.size = size
        self.position = (0, 0)
        self.color = color
        self.t_increment = t_increment
        self.a = a
        self.b = b
        self.t = t
        self.lines = []
        self.stopped = False
        self.stop_start_time = None
        self.current_stop_index = 0
        self.stop_positions = stop_positions if stop_positions else []
        self.line_positions = line_positions
        

    def createBody(self, screen, center_x, center_y, draw_line, is_orbit):
        if is_orbit == True:
            distance_x, distance_y = center_x - self.a, center_y - self.b
            pygame.draw.ellipse(screen, (255, 255, 255), (distance_x, distance_y, self.a*2, self.b*2), width=1)

        self.position = self.createOrbit(center_x, center_y)
                
        pygame.draw.circle(screen, self.color, self.position, self.size)

        if draw_line == True:
            pygame.draw.line(screen, (255, 255, 255), self.position, (0, 0), width=2)
    
    def createOrbit(self, center_x, center_y):
        x = center_x + self.a * math.cos(self.t)
        y = center_y + self.b * math.sin(self.t)

        self.t += self.t_increment
        return (x, y)
    
    def bodyHover(self, mouse_pos, color):
        distance = math.dist(mouse_pos, self.position)
        if distance <= self.size:
            if self.color == color:
                self.color = tuple(int(c * 0.7) for c in self.color)
        else:
            self.color = color
    
    def bodyClick(self, screen, mouse_pos):
        distance = math.dist(mouse_pos, self.position)
        if distance <= self.size:
            return True
        return False


def solarSystem(default_reach, domain, reach):
    sun = CelestialBody(175 * default_reach, (255, 240, 200), 0, 0, 0, 0, 0) # 255, 245, 237

    earth_a, earth_b = 500 * default_reach - 25 * default_reach, 500 * default_reach - 25 * default_reach # Aanpassen voor kleinere schermen
    t_earth_increment = 0.01
    stop_positions = [(domain // 2, reach // 2 + earth_b), (domain // 2, reach // 2 - earth_b)]
    earth = CelestialBody(25 * default_reach, (28, 163, 236), t_earth_increment, earth_a, earth_b, 0, [(0, 900 * default_reach), (150 * default_reach, 0)],stop_positions)

    return sun, earth


def xRayBinaryStar(default_reach, domain, reach):
    scorpiiV818 = CelestialBody(150 * default_reach, (0, 0 , 255), 0, 0, 0, 0, 0)

    sco_a, sco_b = 400 * default_reach - 10 * default_reach, 400 * default_reach - 10 * default_reach
    t_sco_increment = 0.05
    scorpiusX1 = CelestialBody(20 * default_reach, (28, 163, 236), t_sco_increment, sco_a, sco_b, 0, [(domain, reach - 150 * default_reach), (domain - 150 * default_reach, reach)], 0)

    return scorpiiV818, scorpiusX1


def switchScene(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1, loaded, draw_line, simulation_process, pause_start_time, default_reach):
    current_time = time.time()

    match POI:
            case 1:
                if not loaded:
                    loaded = True
                    createUniverse(screen, domain, reach, default_reach)
                    pause_start_time = pygame.time.get_ticks()

                if simulation_process:
                    pygame.draw.line(screen, (255, 255, 255), (domain // 2 + 150 * default_reach, reach // 2), (0 + 100 * default_reach, 0 + 400 * default_reach))

                    if pygame.time.get_ticks() - pause_start_time >= 5000:
                        POI = 3
                        screen.fill("black")
                        pause_start_time = None
                        return loaded, draw_line, pause_start_time, POI, False

                return loaded, draw_line, pause_start_time, POI, False
            case 2:
                screen.fill("black")
                sun.createBody(screen, domain // 2, reach // 2, False, False)

                for line in earth.lines:
                    pygame.draw.line(screen, (255, 255, 255), line[0], line[1])

                earth.createBody(screen, domain // 2, reach // 2, draw_line, True)

                target_position = earth.stop_positions[earth.current_stop_index]
                distance = math.dist(earth.position, target_position)

                if distance < 15 and not earth.stopped and simulation_process:
                    earth.t_increment = 0
                    draw_line = True

                    if earth.line_positions:
                        # Gebruik de juiste positie op basis van de stop
                        line_index = earth.current_stop_index
                        earth.lines.append((earth.position, earth.line_positions[line_index]))
                        earth.line_positions = [] # Reset de posities
                    earth.stopped = True
                    earth.stop_start_time = current_time

                if earth.stopped and current_time - earth.stop_start_time > 3:
                    earth.t_increment = 0.01
                    earth.stopped = False
                    earth.current_stop_index = (earth.current_stop_index + 1) % len(earth.stop_positions)

                    if earth.current_stop_index == 0:
                        POI = 1
                        screen.fill("black")
                        return loaded, draw_line, pause_start_time, POI, False

                return loaded, draw_line, pause_start_time, POI, False
            case 3:
                screen.fill("black")
                scorpiiV818.createBody(screen, domain // 2, reach // 2, False, False)

                if not simulation_process:
                    scorpiusX1.createBody(screen, domain // 2, reach // 2, False, True)
                    if pause_start_time is None:
                        pause_start_time = pygame.time.get_ticks()
                else:
                    scorpiusX1.createBody(screen, domain // 2, reach // 2, False, True)

                    radius = scorpiusX1.a
                    center_x = domain // 2 + scorpiusX1.a
                    center_y = reach // 2 + scorpiusX1.b
                    angle1 = math.pi / 4
                    angle2 = math.pi / 8

                    line_positions = [
                        (center_x + radius * math.cos(angle1), center_y + radius * math.sin(angle1)),
                        (center_x + radius * math.cos(angle2), center_y + radius * math.sin(angle2))
                    ]

                    for i, pos in enumerate(line_positions):
                        if i < len(scorpiusX1.lines):
                            pygame.draw.line(screen, (255, 255, 255), scorpiusX1.lines[i][0], pos, 2)
                        else:
                            scorpiusX1.lines.append((scorpiusX1.position, pos))
                            pygame.draw.line(screen, (255, 255, 255), scorpiusX1.position, pos, 2)

                    if pause_start_time is None:
                        pause_start_time = pygame.time.get_ticks()

                    if pause_start_time is not None and pygame.time.get_ticks() - pause_start_time >= 5000:
                        pause_start_time = None
                        return loaded, draw_line, None, POI, True  # Laat parallax_info True

                return loaded, draw_line, pause_start_time, POI, False
        

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    #screen = pygame.display.set_mode((700, 600)) # Test
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
    text_generated = False
    simulation = False

    default_reach = reach / 1000

    welcome_text = UI(100 * default_reach, (255, 255, 255), (domain // 2, reach // 2))
    name_and_class = UI(50 * default_reach, (255, 255, 255), (domain // 2, reach // 2 + 100 * default_reach))
    teacher_and_subject = UI(40 * default_reach, (255, 255, 255), (domain // 2, reach // 2 + 150 * default_reach))
    close_text = UI(30 * default_reach, (255, 255, 255), (140 * default_reach, 25 * default_reach))
    control_text = UI(40 * default_reach, (255, 255, 255), (domain // 2, reach // 2 + 250 * default_reach))

    sun_text = ["Dit is de zon.",
        "Een middelgrote ster in het centrum van ons zonnestelsel.",
        "Het is de belangrijkste energiebron,",
        "door al het licht en warmte dat het uitstraalt.",
        "Diameter: 1,39 miljoen km.",
        "Oppervlaktetemperatuur: ~5500°C.",
        "Leeftijd: 4,6 miljard jaar.",
        "Evolueert over 5 miljard jaar tot een rode reus."]
    
    earth_text = ["Dit is de aarde.",
        "De derde planeet vanaf de zon en de enige bekende planeet met leven.",
        "Het heeft een atmosfeer rijk aan zuurstof en water,",
        "essentieel voor levende organismen.",
        "Verder heeft de aarde een diameter van 12,742 km",
        "en een gemiddele oppervlaktetemperatuur van 15°C.",
        "~71% van het oppervlak is bedekt met water.",
        "Het draait in ~24 uur om haar as,",
        "terwijl ze in 365,25 dagen een baan rond de zon voltooit.",
        "De enige natuurlijke satelliet van de aarde is de maan."]
    
    scorpiiV818_text = ["Dit is Scorpii V818",
        "Een dubbelstersysteem in het sterrenbeeld Schorpioen",
        "Samen met Scorpius X-1 vormt het een röntgendubbelster,",
        "waarbij Scorpii V818 de blauwe, variabele, begeleidende ster is.",
        "Door de krachtige uitbarstingen van energie,",
        "is het een belangrijk studieobject voor astronomen."]
    
    scorpiusX1_text = ["Dit is Scorpius X-1",
        "De helderste röntgenbron aan de hemel (buiten de zon)",
        "en bevindt zich in het sterrenbeeld Schorpioen.",
        "Samen met Scorpii V818 vormt het een röntgendubbelster,",
        "waarvan Scorpius X-1 de neutronenster is die de materie aantrekt.",
        "Dat proces veroorzaakt extreem hete accretieschijven",
        "en ontzettend krachtige röntgenuitbarstingen.",
        "In 1962 werd het ontdekt als eerste bekende röntgenbron",
        "buiten ons zonnestelsel.",
        "Deze ster speelt een cruciale rol in het begrijpen",
        "van neutronensterren en hun omgevingen."]
    
    parallax_text = ["De parallaxmethode is een techniek om de afstand tot nabije sterren te bepalen,",
        "door de schijnbare verschuiving van de ster",
        "ten opzichte van de achtergrondsterren te meten.",
        "Deze verschuiving ontstaat doordat de aarde in een baan om de zon beweegt.",
        "De parallaxhoek geeft aan hoeveel de ster verschuift.",
        "Dat wordt in boogseconden gemeten.",
        "Hoe klein de parallaxhoek, hoe groter de afstand tot de ster.",
        "De afstand wordt in parsec uitgedrukt",
        "en wordt berkend met de formule: d=1/p of tan(π) = overstaand/aanliggend,",
        "zie Word-document voor korte uitleg.",
        "d is de afstand in parsec en p de parallaxhoek.",
        "De berekende afstand is 2,8 kpc",
        "dus is in lichtjaren is dat: 2,8 X 3,26 = 9,128 kly (kilolichtjaar).",
        "Dat is 9128 lichtjaar, wat overeenkomt met de afstand op het internet."]
    
    start_y = 25 * default_reach  # Beginpositie voor de tekst 
    line_spacing = 30 * default_reach  # Afstand tussen regels

    information = UI(40 * default_reach, (255, 255, 255), (domain - 250 * default_reach, start_y))
    parallax_UI = UI(40 * default_reach, (255, 255, 255), (domain - 250 * default_reach, start_y))

    sun_info = False
    earth_info = False
    scorpiiV818_info = False
    scorpiusX1_info = False
    parallax_info = False

    #start_button = UI(100 * default_reach, (255, 255, 255), (domain // 2, reach // 2))

    sun, earth = solarSystem(default_reach, domain, reach)
    scorpiiV818, scorpiusX1 = xRayBinaryStar(default_reach, domain, reach)

    screen.fill("black")

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if POI > 1:
                        loaded = False
                        screen.fill("black")
                        sun_info = False
                        earth_info = False
                        scorpiiV818_info = False
                        scorpiusX1_info = False
                        POI -= 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if POI < amount_of_POIs:
                        loaded = False
                        screen.fill("black")
                        sun_info = False
                        earth_info = False
                        scorpiiV818_info = False
                        scorpiusX1_info = False
                        POI += 1
                if event.key == pygame.K_SPACE:
                    loaded = False
                    draw_line = False
                    screen.fill("black")
                    sun_info = False
                    earth_info = False
                    scorpiiV818_info = False
                    scorpiusX1_info = False
                    earth.t = 0
                    POI = 2
                    simulation_process = True
                if event.key == pygame.K_UP:
                    loaded = False
                    draw_line = False
                    earth.t = 0
                    earth.t_increment = 0.01
                    screen.fill("black")
                    simulation_process = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sun.bodyClick(screen, mouse_pos) and POI == 2 and not sun_info:
                    sun_info = True
                elif sun.bodyClick(screen, mouse_pos) and POI == 2 and sun_info:
                    sun_info = False
                
                if earth.bodyClick(screen, mouse_pos) and POI == 2 and not earth_info:
                    earth_info = True
                elif earth.bodyClick(screen, mouse_pos) and POI == 2 and earth_info:
                    earth_info = False

                if scorpiiV818.bodyClick(screen, mouse_pos) and POI == 3 and not scorpiiV818_info:
                    scorpiiV818_info = True
                elif scorpiiV818.bodyClick(screen, mouse_pos) and POI == 3 and scorpiiV818_info:
                    scorpiiV818_info = False

                if scorpiusX1.bodyClick(screen, mouse_pos) and POI == 3 and not scorpiusX1_info:
                    scorpiusX1_info = True
                elif scorpiusX1.bodyClick(screen, mouse_pos) and POI == 3 and scorpiusX1_info:
                    scorpiusX1_info = False


        if not simulation_process and simulation == False:
            loaded, draw_line, pause_start_time, POI, parallax_info = switchScene(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1, loaded, draw_line, simulation_process, pause_start_time, default_reach)
        if simulation_process:
            loaded, draw_line, pause_start_time, POI, parallax_info = switchScene(screen, POI, domain, reach, sun, earth, scorpiiV818, scorpiusX1, loaded, draw_line, simulation_process, pause_start_time, default_reach)
            if parallax_info == True:
                screen.fill("black")
                simulation_process = True

        if POI == 1 and not text_generated and not simulation_process:
            text_generated = True
            welcome_text.text(screen, "Afstand tot ster")
            name_and_class.text(screen, "Sven & Aarif V41")
            teacher_and_subject.text(screen, "Dyane Til ANW")
            close_text.text(screen, "ESC / Alt + F4 - afsluiten")
            control_text.text(screen, "Controls: A/left-arrow, D/right-arrow, Spatie")

            #start_button.draw(screen)

        if POI != 1:
            close_text.text(screen, "ESC / Alt + F4 - afsluiten")
            text_generated = False

        if sun_info:
            if earth_info:
                earth_info = False
            for i, line in enumerate(sun_text):
                information.position = (int(domain * 0.5), int(reach * 0.03 + i * 30 * default_reach))
                information.text(screen, line)

        if earth_info:
            if sun_info:
                sun_info = False
            for i, line in enumerate(earth_text):
                information.position = (int(domain * 0.5), int(reach * 0.03 + i * 30 * default_reach))
                information.text(screen, line)

        if scorpiiV818_info:
            if scorpiusX1_info:
                scorpiusX1_info = False
            for i, line in enumerate(scorpiiV818_text):
                information.position = (int(domain * 0.5), int(reach * 0.03 + i * 30 * default_reach))
                information.text(screen, line)

        if scorpiusX1_info:
            if scorpiiV818_info:
                scorpiiV818_info = False
            for i, line in enumerate(scorpiusX1_text):
                information.position = (int(domain * 0.5), int(reach * 0.03 + i * 30 * default_reach))
                information.text(screen, line)

        if parallax_info:
            for i, line in enumerate(parallax_text):
                parallax_UI.position = (int(domain * 0.5), int(reach * 0.1 + i * 30 * default_reach))
                parallax_UI.text(screen, line)

        sun.bodyHover(mouse_pos, (255, 240, 200))
        earth.bodyHover(mouse_pos, (28, 163, 236))
        scorpiiV818.bodyHover(mouse_pos, (0, 0 , 255))
        scorpiusX1.bodyHover(mouse_pos, (28, 163, 236))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()