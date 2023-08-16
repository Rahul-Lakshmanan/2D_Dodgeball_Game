import pygame
import os
import config
from dodgeball_class import Dodgeball

class Player:
    def __init__(self, player_section):
        # attributes: player_selection, dodgeballs, player, hitbox, balls
        self.player_section = player_section
        self.dodgeballs = []
        self.balls = config.DODGEBALL_NUMBERS
        self.hands_full = False
        self.holding_ball = None


        if player_section == 'RIGHT' or player_section ==  'LEFT':
            pass
        else:
            raise TypeError("Invalid player_section during Player object initialization")
        

        if (player_section == 'RIGHT'):
            RIGHT_PLAYER_IMAGE = pygame.image.load(os.path.join('Assets', 'rightPlayer.png'))
            self.player = pygame.transform.scale(RIGHT_PLAYER_IMAGE, (config.PLAYER_WIDTH, config.PLAYER_HEIGHT))

            self.hitbox = pygame.Rect((3 * config.WIDTH)//4 - config.PLAYER_WIDTH, 
                                      config.HEIGHT//2 - config.PLAYER_HEIGHT, config.PLAYER_WIDTH, 
                                      config.PLAYER_HEIGHT)
            
            for i in range(config.DODGEBALL_NUMBERS):
                self.dodgeballs.append(Dodgeball('RIGHT', i))

        else:
            LEFT_PLAYER_IMAGE = pygame.image.load(os.path.join('Assets', 'rightPlayer.png'))
            self.player = pygame.transform.flip(pygame.transform.scale(LEFT_PLAYER_IMAGE, 
                                                (config.PLAYER_WIDTH, config.PLAYER_HEIGHT)), True, False)
            
            self.hitbox = pygame.Rect(config.WIDTH//4 - config.PLAYER_WIDTH, 
                                      config.HEIGHT//2 - config.PLAYER_HEIGHT,config.PLAYER_WIDTH, 
                                      config.PLAYER_HEIGHT)
            
            for i in range(config.DODGEBALL_NUMBERS):
                self.dodgeballs.append(Dodgeball('LEFT', i))
    


    def _Move_Left(self):
        self.hitbox.x -= config.PLAYER_VELOCITY
    def _Move_Right(self):
        self.hitbox.x += config.PLAYER_VELOCITY
    def _Move_Up(self):
        self.hitbox.y -= config.PLAYER_VELOCITY
    def _Move_Down(self):
        self.hitbox.y += config.PLAYER_VELOCITY

    def _Handle_Movement(self, keys_pressed):
        if self.player_section == 'LEFT':
            if keys_pressed[pygame.K_w] and self.hitbox.y - config.PLAYER_VELOCITY > 0:
                self._Move_Up()
            if keys_pressed[pygame.K_s] and self.hitbox.y + config.PLAYER_HEIGHT + \
                config.PLAYER_VELOCITY < config.HEIGHT:
                self._Move_Down()
            if keys_pressed[pygame.K_a] and self.hitbox.x - config.PLAYER_VELOCITY > 0:
                self._Move_Left()
            if keys_pressed[pygame.K_d] and self.hitbox.x + config.PLAYER_WIDTH + \
                config.PLAYER_VELOCITY < config.WIDTH // 2 - config.DIVIDER_WIDTH:
                self._Move_Right()
        else:
            if keys_pressed[pygame.K_UP] and self.hitbox.y - config.PLAYER_VELOCITY > 0:
                self._Move_Up()
            if keys_pressed[pygame.K_DOWN] and (self.hitbox.y + config.PLAYER_HEIGHT +
                config.PLAYER_VELOCITY < config.HEIGHT):
                self._Move_Down()
            if keys_pressed[pygame.K_LEFT] and (self.hitbox.x - config.PLAYER_VELOCITY > 
                config.WIDTH // 2):
                self._Move_Left()
            if keys_pressed[pygame.K_RIGHT] and (self.hitbox.x + config.PLAYER_WIDTH +
                config.PLAYER_VELOCITY < config.WIDTH):
                self._Move_Right()
    
    def _Handle_Grab_Ball(self):
        if not self.hands_full:
            ball_id = 0
            for ball in self.dodgeballs:
                if ball.hitbox.colliderect(self.hitbox):
                    self.holding_ball = ball_id
                    ball._Stick(self, self.holding_ball)
                    self.hands_full = True
                    break
                ball_id += 1
        else:
            self.dodgeballs[self.holding_ball]._Stick(self, self.holding_ball)

    def _Throw(self):
        if self.holding_ball != None:
            self.dodgeballs[self.holding_ball]._Travel(self)
            self.hands_full = False
            self.holding_ball = None