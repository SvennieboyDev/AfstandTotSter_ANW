import pygame
import math

t_earth = 0
t_moon = 0
t_mars = 0
t_jupiter = 0

def heliocentricSystem(screen):
    center_x, center_y = 350, 350 #Makkelijkere manier?

    # Zon
    sun_size = 50
    pygame.draw.circle(screen, (255, 245, 237), (center_x, center_y), sun_size, sun_size) # Kleur aangeraden door ChatGPT, lijkt wit vanaf de ruimte gezien

    # Aarde
    earth_a, earth_b = 150, 150 # Straal van ellips
    earth_border_distance_x = center_x - earth_a # Afstand tot rand
    earth_border_distance_y = center_y - earth_b 
    pygame.draw.ellipse(screen, (255, 255, 255), (earth_border_distance_x, earth_border_distance_y, earth_a * 2, earth_b * 2), width=1) # Rect: locatie_x, locatie_y, afstand_x, afstand_y
    
    global t_earth # Locatie
    t_earth_increment = 0.01
    earth_x, earth_y, t_earth = createOrbit(center_x, center_y, earth_a, earth_b, t_earth, t_earth_increment)

    earth_size = 20
    pygame.draw.circle(screen, (28, 163, 236), (earth_x, earth_y), earth_size, earth_size) # Kleur van ondiep water, turquoise of cyaan, door ChatGPT

    # Maan
    moon_a, moon_b = 40, 40

    global t_moon
    t_moon_increment = t_earth_increment * 13.4 # Maan beweegt 13.4 keer rond de aarde in een jaar
    moon_x, moon_y, t_moon = createOrbit(earth_x, earth_y, moon_a, moon_b, t_moon, t_moon_increment)

    moon_size = int(earth_size * 0.27)
    pygame.draw.circle(screen, (255, 255, 255), (moon_x, moon_y), moon_size, moon_size)

    # Mars
    mars_a, mars_b = earth_a + 100, earth_b + 100 # 150 + 250 bijvoorbeeld
    mars_border_distance_x = center_x - mars_a
    mars_border_distance_y = center_y - mars_b
    pygame.draw.ellipse(screen, (255, 255, 255), (mars_border_distance_x, mars_border_distance_y, mars_a * 2, mars_b * 2), width=1)

    global t_mars
    t_mars_increment = t_earth_increment * 0.81 # Mars gaat 0.81 keer langzamer dan de aarde
    mars_x, mars_y, t_mars = createOrbit(center_x, center_y, mars_a, mars_b, t_mars, t_mars_increment)

    mars_size = int(earth_size * 0.53)
    pygame.draw.circle(screen, (200, 100, 50), (mars_x, mars_y), mars_size, mars_size)

    # Jupiter
    jupiter_a, jupiter_b = earth_a + 250, earth_b + 250
    jupiter_border_distance_x = center_x - jupiter_a
    jupiter_border_distance_y = center_y - jupiter_b
    pygame.draw.ellipse(screen, (255, 255, 255), (jupiter_border_distance_x, jupiter_border_distance_y, jupiter_a * 2, jupiter_b * 2), width=1)

    global t_jupiter
    t_jupiter_increment = t_earth_increment * 0.44
    jupiter_x, jupiter_y, t_jupiter = createOrbit(center_x, center_y, jupiter_a, jupiter_b, t_jupiter, t_jupiter_increment)

    jupiter_size = 40 #int(earth_size * 10.98) INACCURAAT
    pygame.draw.circle(screen, (189, 153, 111), (jupiter_x, jupiter_y), jupiter_size, jupiter_size)


def createOrbit(center_x, center_y, a, b, t, t_increment):    
    x = center_x + a * math.cos(t)
    y = center_y + b * math.sin(t)

    t += t_increment
    return x, y, t


def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Afstand tot ster")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("black")

        heliocentricSystem(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
        

if __name__ == "__main__":
    main()