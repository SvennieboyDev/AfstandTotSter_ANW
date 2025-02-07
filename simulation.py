import pygame
import math

t_earth = 0
t_moon = 0

def heliocentricSystem(screen):
    center_x, center_y = 350, 350 #Makkelijkere manier?

    # Zon
    sun_size = 100
    pygame.draw.circle(screen, (255, 245, 237), (center_x, center_y), sun_size, sun_size) # Kleur aangeraden door ChatGPT, lijkt wit vanaf de ruimte gezien

    # Aarde
    earth_a, earth_b = 250, 250
    global t_earth

    border_distance = 100
    earth_orbit_size = 500
    pygame.draw.ellipse(screen, (255, 255, 255), (border_distance, border_distance, earth_orbit_size, earth_orbit_size), width=1)
    
    t_earth_increment = 0.01
    earth_x, earth_y, t_earth = createOrbit(center_x, center_y, earth_a, earth_b, t_earth, t_earth_increment)
    pygame.draw.circle(screen, (28, 163, 236), (earth_x, earth_y), 15, 15) # Kleur van ondiep water, turquoise of cyaan, door ChatGPT

    # Maan
    moon_a, moon_b = 30, 30
    global t_moon

    #moon_orbit_size = 60
    #pygame.draw.ellipse(screen, (255, 255, 255), (earth_x - moon_a, earth_y - moon_b, moon_orbit_size, moon_orbit_size), width=1)

    t_moon_increment = t_earth_increment * 13.4
    moon_x, moon_y, t_moon = createOrbit(earth_x, earth_y, moon_a, moon_b, t_moon, t_moon_increment)
    pygame.draw.circle(screen, (255, 255, 255), (moon_x, moon_y), 3, 3)


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