import pygame    

def heliocentricSystem(screen):
    # Zon
    pygame.draw.circle(screen, (255, 245, 237), (500, 500), 100, 100) # Kleur aangeraden door ChatGPT, lijkt wit vanaf de ruimte gezien

    # Aarde
    pygame.draw.ellipse(screen, (255, 255, 255), (100, 200, 800, 600), width=1)
    pygame.draw.circle(screen, (28, 163, 236), (500, 200), 10, 10) # Kleur van ondiep water, turquoise of cyaan, door ChatGPT

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
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