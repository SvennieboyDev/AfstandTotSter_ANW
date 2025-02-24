import pygame
import math

t_earth, t_moon, t_mars, t_jupiter, t_venus, t_mercurius = 0, 0, 0, 0, 0, 0

def heliocentricSystem(screen, zoom_scale):
    center_x, center_y = 350, 350 #Makkelijkere manier?
    earth_size = 40

    # Zon
    sun_size = int(109.2 * 2 * zoom_scale)
    pygame.draw.circle(screen, (255, 245, 237), (center_x, center_y), sun_size, sun_size) # Kleur aangeraden door ChatGPT, lijkt wit vanaf de ruimte gezien


    # Aarde
    earth_a, earth_b = 1000 * zoom_scale, 1000 * zoom_scale # Straal van ellips
    earth_border_distance_x = center_x - earth_a # Afstand tot rand
    earth_border_distance_y = center_y - earth_b 
    pygame.draw.ellipse(screen, (255, 255, 255), (earth_border_distance_x, earth_border_distance_y, earth_a * 2, earth_b * 2), width=1) # Rect: locatie_x, locatie_y, afstand_x, afstand_y
    
    global t_earth # Locatie
    t_earth_increment = 0.01
    earth_x, earth_y, t_earth = createOrbit(center_x, center_y, earth_a, earth_b, t_earth, t_earth_increment)

    earth_scaled_size = int(earth_size * zoom_scale)
    pygame.draw.circle(screen, (28, 163, 236), (earth_x, earth_y), earth_scaled_size, earth_scaled_size) # Kleur van ondiep water, turquoise of cyaan, door ChatGPT

    if earth_a >= earth_b:
        largest_earth_radius = earth_a
    else:
        largest_earth_radius = earth_b


    # Maan
    moon_a, moon_b = 75 * zoom_scale, 75 * zoom_scale

    global t_moon
    t_moon_increment = t_earth_increment * 13.4 # Maan beweegt 13.4 keer rond de aarde in een jaar
    moon_x, moon_y, t_moon = createOrbit(earth_x, earth_y, moon_a, moon_b, t_moon, t_moon_increment)

    moon_scaled_size = int(earth_scaled_size * 0.27)
    pygame.draw.circle(screen, (255, 255, 255), (moon_x, moon_y), moon_scaled_size, moon_scaled_size)


    # Mars
    mars_a, mars_b = largest_earth_radius + 250 * zoom_scale, largest_earth_radius + 250 * zoom_scale # 150 + 250 bijvoorbeeld
    mars_border_distance_x = center_x - mars_a
    mars_border_distance_y = center_y - mars_b
    pygame.draw.ellipse(screen, (255, 255, 255), (mars_border_distance_x, mars_border_distance_y, mars_a * 2, mars_b * 2), width=1)

    global t_mars
    t_mars_increment = t_earth_increment * 0.81 # Mars gaat 0.81 keer langzamer dan de aarde
    mars_x, mars_y, t_mars = createOrbit(center_x, center_y, mars_a, mars_b, t_mars, t_mars_increment)

    mars_scaled_size = int(earth_scaled_size * 0.53)
    pygame.draw.circle(screen, (200, 100, 50), (mars_x, mars_y), mars_scaled_size, mars_scaled_size)


    # Jupiter
    jupiter_a, jupiter_b = largest_earth_radius + 1000 * zoom_scale, largest_earth_radius + 1000 * zoom_scale
    jupiter_border_distance_x = center_x - jupiter_a
    jupiter_border_distance_y = center_y - jupiter_b
    pygame.draw.ellipse(screen, (255, 255, 255), (jupiter_border_distance_x, jupiter_border_distance_y, jupiter_a * 2, jupiter_b * 2), width=1)

    global t_jupiter
    t_jupiter_increment = t_earth_increment * 0.44
    jupiter_x, jupiter_y, t_jupiter = createOrbit(center_x, center_y, jupiter_a, jupiter_b, t_jupiter, t_jupiter_increment)

    jupiter_size = int(10.97 * 10 * zoom_scale)
    pygame.draw.circle(screen, (189, 153, 111), (jupiter_x, jupiter_y), jupiter_size, jupiter_size)


    # Venus
    venus_a, venus_b = largest_earth_radius - 250 * zoom_scale, largest_earth_radius - 250 * zoom_scale
    venus_border_distance_x = center_x - venus_a
    venus_border_distance_y = center_y - venus_b
    pygame.draw.ellipse(screen, (255, 255, 255), (venus_border_distance_x, venus_border_distance_y, venus_a * 2, venus_b * 2), width=1)

    global t_venus
    t_venus_increment = t_earth_increment * 1.18
    venus_x, venus_y, t_venus = createOrbit(center_x, center_y, venus_a, venus_b, t_venus, t_venus_increment)

    venus_scaled_size = int(earth_scaled_size * 0.95)
    pygame.draw.circle(screen, (213, 171, 114), (venus_x, venus_y), venus_scaled_size, venus_scaled_size)


    # Mercurius
    mercurius_a, mercurius_b = largest_earth_radius - 500 * zoom_scale, largest_earth_radius - 500 * zoom_scale
    mercurius_distance_x = center_x - mercurius_a
    mercurius_distance_y = center_x - mercurius_b
    pygame.draw.ellipse(screen, (255, 255, 255), (mercurius_distance_x, mercurius_distance_y, mercurius_a * 2, mercurius_b * 2), width=1)

    global t_mercurius
    t_mercurius_increment = t_earth_increment * 1.6
    mercurius_x, mercurius_y, t_mercurius = createOrbit(center_x, center_y, mercurius_a, mercurius_b, t_mercurius, t_mercurius_increment)

    mercurius_scaled_size = int(earth_scaled_size * 0.38)
    pygame.draw.circle(screen, (140, 133, 122), (mercurius_x, mercurius_y), mercurius_scaled_size, mercurius_scaled_size)



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

    zoom_scale = 1.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    zoom_scale *= 1.1
                elif event.key == pygame.K_DOWN:
                    zoom_scale *= 0.9
        
        screen.fill("black")

        heliocentricSystem(screen, zoom_scale)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
        

if __name__ == "__main__":
    main()