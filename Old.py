import pygame
import math

t_earth = 0

def x_rayBinary(screen, center, earth_size, zoom_scale):
    scorpius_size = int(earth_size * 45.5 * zoom_scale)
    pygame.draw.circle(screen, (255, 255, 255), (center - 300, center - 300), scorpius_size, scorpius_size)


def heliocentricSystem(screen, center, zoom_scale, earth_size):
    # Zon
    sun_size = int(109.2 * 1.5 * zoom_scale)
    pygame.draw.circle(screen, (255, 245, 237), (center, center), sun_size, sun_size) # Kleur aangeraden door ChatGPT, lijkt wit vanaf de ruimte gezien

    # Aarde
    earth_a, earth_b = 300 * zoom_scale, 275 * zoom_scale # Straal van ellips
    earth_border_distance_x = center - earth_a # Afstand tot rand
    earth_border_distance_y = center - earth_b 
    pygame.draw.ellipse(screen, (255, 255, 255), (earth_border_distance_x, earth_border_distance_y, earth_a * 2, earth_b * 2), width=1) # Rect: locatie_x, locatie_y, afstand_x, afstand_y
    
    global t_earth # Locatie
    t_earth_increment = 0.01
    earth_x, earth_y, t_earth = createOrbit(center, center, earth_a, earth_b, t_earth, t_earth_increment)

    earth_scaled_size = int(earth_size * zoom_scale)
    pygame.draw.circle(screen, (28, 163, 236), (earth_x, earth_y), earth_scaled_size, earth_scaled_size) # Kleur van ondiep water, turquoise of cyaan, door ChatGPT


def createOrbit(center_x, center_y, a, b, t, t_increment):    
    x = center_x + a * math.cos(t)
    y = center_y + b * math.sin(t)

    t += t_increment
    return x, y, t


def zoomText(screen, text_color, zoom_scale, fontObj):    
    zoom_scale = round(zoom_scale, 2)
    text_zoom = "Zoom: " + str(zoom_scale)
    text_zoomObj = fontObj.render(text_zoom, True, text_color, None)

    screen.blit(text_zoomObj, (50, 650))


def universeText(screen, text_color, fontObj):
    text_solar_systemObj = fontObj.render("Solar System", True, text_color, None)
    


def universe(screen, center):
    pygame.draw.circle(screen, (255, 255, 255), (center, center), 1, 1) # Zon
    pygame.draw.circle(screen, (255, 255, 255), (center -250, center - 200), 1, 1) # Scorpius X-1


def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Afstand tot ster")
    clock = pygame.time.Clock()
    running = True

    fontObj = pygame.font.Font(None, 32) # Standard font, size 32

    center = 350
    zoom_scale = 1.00
    text_color = (255, 255, 255)

    earth_size = 20

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    zoom_scale += 0.1
                elif event.key == pygame.K_DOWN:
                    zoom_scale -= 0.1
        
        screen.fill("black")

        # universe(screen, center)
        zoomText(screen, text_color, zoom_scale, fontObj)
        # universeText(screen, text_color, fontObj)

        heliocentricSystem(screen, center, zoom_scale, earth_size)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
        

if __name__ == "__main__":
    main()