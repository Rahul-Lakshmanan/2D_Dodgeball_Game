import pygame
import config
pygame.font.init()

# button colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (10, 143, 245)
ORANGE = (255, 153, 0)
YELLOW = (247, 255, 0)

clicked = False


class Button: 
    BUTTON_FONT = pygame.font.SysFont('comicsans', 45)

    def __init__(self, width, height, x_location, y_location, text):
        self.width = width
        self.height = height
        self.text = text
        self.x = x_location
        self.y = y_location
        self.disabled = False
        self.frame = 0

    def Draw_Button(self):
        pressed = False

        # get mouse position and build button
        mouse_pos = pygame.mouse.get_pos()
        button = pygame.Rect(self.x, self.y, self.width, self.height)

        # draw button according to actions
        if button.collidepoint(mouse_pos):
            # button pressed
            if pygame.mouse.get_pressed()[0] == 1: 
                global clicked
                clicked = True
                pygame.draw.rect(config.WINDOW, YELLOW, button)
            # button has been pressed and released
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                pressed = True
                self.disabled = True
            # mouse hover over button
            else: 
                pygame.draw.rect(config.WINDOW, ORANGE, button)
        else: 
            pygame.draw.rect(config.WINDOW, BLUE, button)

        # add visual detail to button
        pygame.draw.line(config.WINDOW, WHITE, (self.x, self.y), (self.x + self.width, self.y), 4)
        pygame.draw.line(config.WINDOW, WHITE, (self.x, self.y), (self.x, self.y + self.height), 4)
        pygame.draw.line(config.WINDOW, BLACK, (self.x + self.width, self.y), 
                         (self.x + self.width, self.y + self.height), 4)
        pygame.draw.line(config.WINDOW, BLACK, (self.x, self.y + self.height), 
                         (self.x + self.width, self.y + self.height), 4)

        # draw text onto button
        if self.text == "Back": 
            text = Button.BUTTON_FONT.render(self.text, True, BLACK)
            text = pygame.transform.scale(text, (50, 30))
        else:
            text = Button.BUTTON_FONT.render(self.text, True, WHITE)

        config.WINDOW.blit(text, (self.x + (self.width - text.get_width()) // 2, 
                                  self.y + (self.height - text.get_height()) // 2))
        
        return pressed
    
    def Is_Active(self):
        return not self.disabled