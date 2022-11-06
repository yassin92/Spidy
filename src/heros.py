import pygame

from src.screen import width, height


class Character:
    IMAGE_SCALE = (150, 100)

    def __init__(self, name, image: str, initial_position: tuple[int, int] = (0, 0), speed=None):
        if speed is None:
            speed = [0, 0]
        self.__name = name
        im = pygame.image.load(image)
        self._scale = Character.IMAGE_SCALE
        self._image = pygame.transform.scale(im, self._scale)
        self._rect = self._image.get_rect()
        self._rect.x, self._rect.y = initial_position
        self.speed = speed

    @property
    def rect(self):
        return self._rect

    @property
    def image(self):
        return self._image

    def move(self):
        self._rect = self._rect.move(self.speed[0], self.speed[1])
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = - self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]

    def handle_events(self, event_list: list):
        pass

    def react_to_environment(self, character_list):
        pass


class MovingCharacters(Character):
    def __init__(self, name, image: str, initial_position: tuple[int, int] = (0, 0), speed=None, commands=None):
        super().__init__(name, image, initial_position, speed)
        if not commands:
            commands = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        else:
            assert len(commands) >= 4, 'minimum commands is 4 for up down left and right'
        self._left_key = commands[2]
        self._right_key = commands[3]
        self._up_key, self._down_key, self._left_key, self._right_key = commands[0], commands[1], commands[2], commands[
            3]

    def handle_events(self, event_list: list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                print(pygame.key.name(event.key))
                if (event.key == self._left_key and self.speed[0] > 0) or (
                        event.key == self._right_key and self.speed[0] < 0):
                    self.speed[0] = -self.speed[0]
                if (event.key == self._up_key and self.speed[1] > 0) or (
                        event.key == self._down_key and self.speed[1] < 0):
                    self.speed[1] = -self.speed[1]


class Spidey(MovingCharacters):
    def __init__(self, image: str, initial_position: tuple[int, int] = (0, 0)):
        super().__init__('Spidey', image, initial_position, speed=[2, 2])


class Rhino(MovingCharacters):
    def __init__(self, image: str, initial_position: tuple[int, int] = (0, 0)):
        super().__init__('Rhino', image, initial_position, speed=[2, 2],
                         commands=[pygame.K_KP8, pygame.K_KP2, pygame.K_KP4, pygame.K_KP6])

    def react_to_environment(self, character_list):
        for char in character_list:
            if char is not self and self.rect.colliderect(char.rect):
                self._image = pygame.transform.scale(self.image, (self._scale[0] - 10, self._scale[1] - 10))
                pygame.mixer.init()
                bullet_sound = pygame.mixer.Sound('sounds/assets_sounds_explosion.wav')
                bullet_sound.play()
                #self._rect = self._image.get_rect()
