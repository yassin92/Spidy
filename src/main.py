import sys, pygame
from time import sleep

from src.heros import Spidey, Rhino
from src.screen import frequency, black, screen

pygame.init()

speed = [2, 2]

character_list = [Spidey("./img/spidy.png"), Rhino("./img/tenor.gif", initial_position=(1000, 50))]

while True:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT: sys.exit()

    for character in character_list:
        character.handle_events(event_list)
        character.move()
        character.react_to_environment(character_list)

    sleep(1 / frequency)
    screen.fill(black)
    for character in character_list:
        screen.blit(character.image, character.rect)
    pygame.display.flip()
