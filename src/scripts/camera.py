#everything written by RoboMarchello😁
import pygame
from pygame.locals import *


class Mode7:
    def __init__(self, screen, GameMap):
        self.NearPoint1 = pygame.Vector2
        self.NearPoint2 = pygame.Vector2
        self.FarPoint1 = pygame.Vector2
        self.FarPoint2 = pygame.Vector2

        self.screen = screen
        self.halfScreen = [64, 32]
        self.MapArray = pygame.pixelarray.PixelArray(GameMap)
        self.MapSize = self.MapArray.shape

        self.surface = pygame.Surface(self.halfScreen)
        self.SurfArr = pygame.pixelarray.PixelArray(self.surface)
        
        self.BlankColor = self.surface.map_rgb((100, 100, 255))
        
    def draw(self):
        for row in range(self.halfScreen[1]):
            for cell in range(self.halfScreen[0]):
                NormalPos = [
                    cell / self.halfScreen[0],
                    1 / (row / self.halfScreen[1] + 0.0001),
                    1.0 - row / self.halfScreen[1],
                ]
                MappedPos = self.MapPixel(NormalPos)
                if MappedPos[0] < 0 or MappedPos[0] > self.MapSize[0] - 1:
                    self.SurfArr[cell][row] = self.BlankColor
                    
                elif MappedPos[1] < 0 or MappedPos[1] > self.MapSize[1] - 1:
                    self.SurfArr[cell][row] = self.BlankColor
                    
                else:
                    self.SurfArr[cell][row] = self.MapArray[MappedPos[0]][MappedPos[1]]

        self.screen.blit(self.SurfArr.make_surface(), (0, self.halfScreen[1]))

    def MapPixel(self, normalPos):
        '''
        This function finds the pixel in our view frustum
        First we are finding two points and applying interpolation
        (FarNear1, FarNear2), then we find the vector between them
        and interpolating it by our normalPos value
        '''
        FarNear1 = (self.FarPoint1 - self.NearPoint1) * normalPos[1] 
        FarNear2 = (self.FarPoint2 - self.NearPoint2) * normalPos[1]
        
        FarNear1 += self.NearPoint1
        FarNear2 += self.NearPoint2

        FarNearIntr = (FarNear2 - FarNear1) * normalPos[0] + FarNear1
        return [int(FarNearIntr[0]), int(FarNearIntr[1])]

    def UpdateViewPort(self, NearPoint1, NearPoint2, FarPoint1, FarPoint2):
        self.NearPoint1 = NearPoint1
        self.NearPoint2 = NearPoint2
        self.FarPoint1 = FarPoint1
        self.FarPoint2 = FarPoint2

        
class Camera:
    def __init__(self, position, angle, screen, GameMap):
        self.position = position
        self.angle = angle
        self.FOV = 60

        self.moveDir = {'forward': False, 'back': False}
        self.moveVector = pygame.Vector2(0, -1)
        self.moveSpeed = 2
        self.moveVector = pygame.Vector2(0, -1).rotate(self.angle)
        
        self.turnDir = {'left': False, 'right': False}
        self.turnSpeed = 2

        self.nearest = 15
        self.furthest = 100

        self.pixelPos = pygame.Vector2(0.5, 0.5)
        self.drawCam = False

        self.Mode7 = Mode7(screen, GameMap)

        self.tweak = {
            'IncreaseNearest': False,
            'DecreaseNearest': False,
            'IncreaseFurthest': False,
            'DecreaseFurthest': False,
            'IncreaseFov': False,
            'DecreaseFov': False,
        }

    def draw(self, screen):
        self.move()
        
        NearPoint1 = self.moveVector.rotate(-self.FOV / 2) * self.nearest + self.position
        NearPoint2 = self.moveVector.rotate(self.FOV / 2) * self.nearest + self.position
        FarPoint1 = self.moveVector.rotate(-self.FOV / 2) * self.furthest + self.position
        FarPoint2 = self.moveVector.rotate(self.FOV / 2) * self.furthest + self.position
        
        self.Mode7.UpdateViewPort(NearPoint1, NearPoint2, FarPoint1, FarPoint2)
        self.Mode7.draw()

        #for debug!
        if self.drawCam:
            pygame.draw.circle(screen, (0, 0, 0), self.position, 3)

            pygame.draw.line(screen, (0, 0, 0), NearPoint1, NearPoint2)
            pygame.draw.line(screen, (0, 0, 0), NearPoint1, FarPoint1)
            pygame.draw.line(screen, (0, 0, 0), FarPoint1, FarPoint2)
            pygame.draw.line(screen, (0, 0, 0), FarPoint2, NearPoint2)


    def move(self):
        if self.turnDir['left']:
            self.angle -= self.turnSpeed
            self.moveVector = pygame.Vector2(0, -1).rotate(self.angle)
            
        if self.turnDir['right']:
            self.angle += self.turnSpeed
            self.moveVector = pygame.Vector2(0, -1).rotate(self.angle)
            
        if self.moveDir['forward']:
            self.position += self.moveVector * self.moveSpeed

        if self.moveDir['back']:
            self.position -= self.moveVector * self.moveSpeed


        #for debugging
        if self.tweak['DecreaseNearest']:
            self.nearest -= 1

        elif self.tweak['IncreaseNearest']:
            self.nearest += 1

        if self.tweak['DecreaseFurthest']:
            self.furthest -= 1
        
        elif self.tweak['IncreaseFurthest']:
            self.furthest += 1

        if self.tweak['DecreaseFov']:
            self.FOV -= 1
        
        elif self.tweak['IncreaseFov']:
            self.FOV += 1

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.turnDir['left'] = True

            elif event.key == K_d:
                self.turnDir['right'] = True

            if event.key == K_w:
                self.moveDir['forward'] = True

            elif event.key == K_s:
                self.moveDir['back'] = True

            if event.key == K_z:
                self.tweak['DecreaseNearest'] = True
            
            if event.key == K_x:
                self.tweak['IncreaseNearest'] = True
            
            if event.key == K_c:
                self.tweak['DecreaseFurthest'] = True

            if event.key == K_v:
                self.tweak['IncreaseFurthest'] = True

            if event.key == K_b:
                self.tweak['DecreaseFov'] = True

            if event.key == K_n:
                self.tweak['IncreaseFov'] = True

        if event.type == KEYUP:
            if event.key == K_a:
                self.turnDir['left'] = False

            elif event.key == K_d:
                self.turnDir['right'] = False

            if event.key == K_w:
                self.moveDir['forward'] = False

            elif event.key == K_s:
                self.moveDir['back'] = False

            if event.key == K_z:
                self.tweak['DecreaseNearest'] = False
            
            if event.key == K_x:
                self.tweak['IncreaseNearest'] = False
            
            if event.key == K_c:
                self.tweak['DecreaseFurthest'] = False
                
            if event.key == K_v:
                self.tweak['IncreaseFurthest'] = False

            if event.key == K_b:
                self.tweak['DecreaseFov'] = False

            if event.key == K_n:
                self.tweak['IncreaseFov'] = False