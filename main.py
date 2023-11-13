import pygame
import sys 
import time
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

# Initialize pygame
pygame.init() 

# Screen 
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

# Initialize Game Score
score = 0

# Initialize the Game Difficulty
game_difficulty = "Easy"

# Global Variable Clock
clock = pygame.time.Clock()

# Global Variable Pause
pause = False

# Standard RGB colors 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 
BRIGHT_RED = (255,51,51)
BRIGHT_GREEN = (51,204,51)


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



# Function that changes the difficulty of the game
def Game_Difficulty(dif_list,dif):
      global game_difficulty

      # Change the game difficulty
      game_difficulty = str(dif)

# Fuction that creates and returns Text for the Screen
def text_objects(text, font):
     # Create the text
     textSurface = font.render(text, True, BLACK)

     # Returns the text and it's rectangle (So we can position the Text)
     return textSurface, textSurface.get_rect()

# Fuction that creates Buttons
def button(msg,x,y,width,height,inactive_Color,active_Color,action = None):
     mouse = pygame.mouse.get_pos()
     click = pygame.mouse.get_pressed()
     
     if x+width > mouse[0] > x and y+height > mouse[1] > y:
          pygame.draw.rect(screen, active_Color, (x,y,width,height))
          if click[0] == 1 and action != None:
               action()
     else:
          pygame.draw.rect(screen, inactive_Color, (x,y,width,height))

     smallText = pygame.font.Font("freesansbold.ttf",20)
     textSurf, textRect = text_objects(msg,smallText)
     textRect.center = ( (x+(width/2)), (y+(height/2)) )
     screen.blit(textSurf,textRect)

# Fuction that Quits the Game
def quit_Game():
     pygame.quit()
     sys.exit()

# Fuction that Unpause the Game
def unpause():
     global pause
     pause = False

# Fuction to Pause the Game
def paused():
    global pause
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
    screen.blit(TextSurf, TextRect)

    

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #screen.fill(WHITE)
        

        button("Resume",150,450,100,50,GREEN,BRIGHT_GREEN,unpause)
        button("Quit",450,450,100,50,RED,BRIGHT_RED,quit_Game)

        pygame.display.update()
        clock.tick(15)  
   

# Fuctoin of the main game
def playFun():
     # Set up the drawing window
     game_screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

     # Enters the Score Variable in the scope of playFun() Function
     global score
     
     # Enter the global variable pause so we can pause the game
     global pause

     # Instantiate player. 
     player = Player()

     # Initialize the running variable
     running = True
     while running:
          for event in pygame.event.get():
               if event.type == KEYDOWN:
                    # If player presses Escape
                    if event.key == K_ESCAPE:
                         pause = True
                         # Pause the game
                         paused()
               elif event.type == pygame.QUIT:
                    quit_Game()

               
          #score +=1
          
          # Get all the keys currently pressed
          pressed_keys = pygame.key.get_pressed()

          # Update the player sprite based on user keypresses
          player.update(pressed_keys)
          
          # Fills the screen with the color black
          game_screen.fill((0, 0, 0))

          # Draw the player on the screen
          screen.blit(player.surf, player.rect)

          # Flips the screen
          pygame.display.flip()

# Main Function (That is also the main menu at the start of the game)
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