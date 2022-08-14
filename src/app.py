import pygame
from pygame.locals import *
import asyncio
from src.scripts.camera import *

pygame.init()


class App():
    def __init__(self):
        self.ScreenSize = pygame.Rect(0, 0, 64, 64)
        self.GameScreen = pygame.Surface(self.ScreenSize.size)

        ScaleBy = 8
        self.ScaledScreenSize = [
            self.ScreenSize.width * ScaleBy,
            self.ScreenSize.height * ScaleBy]

        self.screen = pygame.display.set_mode(self.ScaledScreenSize)
        pygame.display.set_caption('mode 7')

        self.map = pygame.image.load('src/assets/map.png').convert()
        self.camera = Camera(
            pygame.Vector2(512, 515), 0, self.GameScreen, self.map.copy()
            )

        self.clock = pygame.time.Clock()
        self.fps = 0

        self.event_handlers = [self.camera]

    async def loop(self):
        screen = self.screen
        while True:
            self.GameScreen.fill((100, 100, 255))

            self.camera.draw(self.GameScreen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)
                

            ScaledScreen = pygame.transform.scale(self.GameScreen, self.ScaledScreenSize)
            self.screen.blit(ScaledScreen, [0, 0])
            
            pygame.display.update()
            pygame.display.set_caption(str(self.clock.get_fps()))

            self.clock.tick(self.fps)
            await asyncio.sleep(0)