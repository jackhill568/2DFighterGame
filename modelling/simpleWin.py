import pygame


pygame.init()
pygame.display.set_mode((0,0), pygame.FULLSCREEN)


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    if key[pygame.K_RETURN]:
        run = False

    pygame.display.update()























































