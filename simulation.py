import pygame
import math

class CreateStars():
    def __init__(self, domain, reach):
        self.domain = domain
        self.reach = reach
        self.size = 1
        self.amount = 10
    
    def random_positions(self):
        print(self.domain)


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    domain, reach = screen.get_size() # Domein is x-as en bereik is y-as
    pygame.display.set_caption("Afstand tot ster")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        CreateStars(domain, reach)
        

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()