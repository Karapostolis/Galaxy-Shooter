import pygame
import sys 
import pygame_menu as pm 
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init() 

# Screen 
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

# Initialize Game Score
score = 0

# Standard RGB colors 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        # Set the background color
        self.surf.fill((255, 255, 255))
        # Fetch the rectangle object that has the dimensions of surf
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
             self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
             self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
             self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
             self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
             self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
             self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
             self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
             self.rect.bottom = SCREEN_HEIGHT



# Initialize the Game Difficulty
game_difficulty = "Easy"

# Function that changes the difficulty of the game
def Game_Difficulty(dif_list,dif):
      game_difficulty = str(dif)

# Fuction that resumes the game
def Resume_Game():
     running = True
     playFun()

# Fuction that appears if the palyer press the Escape Key in Game
def inGameMenuFun():
     inGameMenu = pm.Menu(title="Menu", 
                       width=SCREEN_WIDTH, 
                       height=SCREEN_HEIGHT, 
                       theme=pm.themes.THEME_GREEN)
     
     # Resume button. If clicked, it takes to the game again
     inGameMenu.add.button(title="Resume", font_color=WHITE,action=Resume_Game,
                        background_color=GREEN)

     # Dummy label to add some spacing between the Resume button and Exit button
     inGameMenu.add.label(title="")
     
     # Exit Button. If clicked, it closes the window
     inGameMenu.add.button(title="Exit", action=pm.events.EXIT, 
                        font_color=WHITE, background_color=RED)
     

     #if inGameMenu.get_widget("Resume",False)._onselect:
         # running = True

     # Lets us loop the in game menu on the screen
     inGameMenu.mainloop(screen)

def playFun():
     # Set up the drawing window
     game_screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

     # Enters the Score Variable in the scope of playFun() Function
     global score

     # Make a global running variable which is used for the game loop
     global running

     # Initialize the running variable
     running = True
     while running:
          for event in pygame.event.get():
               if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                         # If palyer presses Escape show In Game Menu
                         inGameMenuFun()
                         # Pausses the game
                         running = False
               elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
               
          #score +=1
          
          game_screen.fill((255, 255, 255))

          pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

          pygame.display.flip()

# Main Function 
def menuFun(): 
	
	# List that is displayed while selecting the difficulty 
    difficulty = [("Easy", "Easy"), 
                  ("Medium", "Medium"), 
                  ("Hard", "Hard")] 
    
    # Creating the main menu
    mainMenu = pm.Menu(title="Main Menu", 
					width=SCREEN_WIDTH, 
					height=SCREEN_HEIGHT, 
					theme=pm.themes.THEME_GREEN) 
    
    # Creating the settings menu 
    settings = pm.Menu(title="Settings", 
                       width=SCREEN_WIDTH, 
                       height=SCREEN_HEIGHT, 
                       theme=pm.themes.THEME_GREEN)
    
    # Selector to choose between the types of difficulties available 
    settings.add.selector(title="Difficulty\t", items=difficulty,onchange = Game_Difficulty, 
                          selector_id="difficulty", default=0, align=pm.locals.ALIGN_LEFT)
    
    # Button to reset the values in settings tto their default
    settings.add.button(title="Restore Defaults", action=settings.reset_value, 
                        font_color=WHITE, background_color=RED, align=pm.locals.ALIGN_LEFT)
    
    # Dummy label to add some spacing between the Restore Defaults button and Return To Main Menu button 
    settings.add.label(title="") 

    # Button to return to the main menu                 
    settings.add.button(title="Return To Main Menu", 
                        action=pm.events.BACK,font_color=BLACK, align=pm.locals.ALIGN_CENTER)


	# Settings button. If clicked, it takes to the settings menu 
    mainMenu.add.button(title="Play",action=playFun ,font_color=WHITE, 
						background_color=GREEN)
    
    # Dummy label to add some spacing between the settings button and exit button 
    mainMenu.add.label(title="") 

	# Exit Button. If clicked, it closes the window 
    mainMenu.add.button(title="Settings", action=settings, 
                        font_color=WHITE, background_color=CYAN)  

	# Dummy label to add some spacing between the settings button and exit button 
    mainMenu.add.label(title="") 

	# Exit Button. If clicked, it closes the window 
    mainMenu.add.button(title="Exit", action=pm.events.EXIT, 
						font_color=WHITE, background_color=RED) 
    
    # Lets us loop the main menu on the screen
    mainMenu.mainloop(screen) 

if __name__ == "__main__":
     menuFun()