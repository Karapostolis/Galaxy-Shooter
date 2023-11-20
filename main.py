import pygame
import sys 
import time,datetime
# Import random for random numbers
import random
import pygame_menu as pm 
from os import path

from Sqlite3 import *

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

# Global enemy speed
enemy_speed = 7

# Global Player Lives
player_Lives = 3

player_Name = "Player 1"

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
    global all_sprites

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Player, self).__init__()

        # Enter an image a the variable surf and converts it so it has transparent background
        self.surf = pygame.image.load("Assets/Spaceship.png").convert_alpha()

        # Fetch the rectangle object that has the dimensions of surf
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 100))
        # The x value of center
        self.rect.centerx = SCREEN_WIDTH/2
        # The shoot delay 
        self.shoot_delay = 250
        # The last shot
        self.last_shot = pygame.time.get_ticks()
        # Players lives
        self.lives = player_Lives


    # Fuction that handles shooting 
    def shoot(self):
        ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
             self.last_shot = now
             bullet = Bullet(self.rect.centerx, self.rect.top)
             all_sprites.add(bullet)
             bullets.add(bullet)
             #shooting_sound.play()

    # Move the sprite based on user keypresses
    def update(self):
        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()
        #Player.Lives(Player)

        if pressed_keys[K_UP]:
             self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
             self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
             self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
             self.rect.move_ip(10, 0)
        if pressed_keys[pygame.K_SPACE]:
             self.shoot()

        # Keep player on the screen
        if self.rect.left < 0:
             self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
             self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
             self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
             self.rect.bottom = SCREEN_HEIGHT
    """
    # Function for Player's Lives
    def Lives(self):
         if player_Lives == 0:
              Player.kill()
              print(player_Lives)
    """
# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()

        # Enter an image a the variable surf and converts it so it has transparent background
        self.surf = pygame.image.load("Assets/Enemy.png").convert_alpha()

        # Makes the enemy to be drawn at the top of the screen 
        # Between random(x = 0 - screem_width) and y = -20
        self.rect = self.surf.get_rect(
            center=(
               random.randint(0, SCREEN_WIDTH),
               -5,
            )
        )
        # The speed at which the enemy will be moving
        self.speed = enemy_speed

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        global score        
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, bullets):
               score = score + 20               
               self.kill()
     
    def set_Difficulty(self):
         global enemy_speed
         global game_difficulty
         if game_difficulty == "Easy":
              enemy_speed = 7

         elif game_difficulty == "Medium":
              enemy_speed = 10
              print("I am inside medium if")
         else:
              enemy_speed = 15
         

## defines the sprite for bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Enter an image a the variable surf and converts it so it has transparent background
        self.surf = pygame.image.load('Assets/Laser.png').convert_alpha()
        self.rect = self.surf.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.bottom < 0:
            self.kill()

# Function that changes the difficulty of the game
def Game_Difficulty(dif_list,dif):
      global game_difficulty

      # Change the game difficulty
      game_difficulty = str(dif)
      Enemy.set_Difficulty(Enemy)
      

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

     # Unpause Music
     pygame.mixer.music.unpause()

# Fuction to Pause the Game
def paused():
     global pause

     # Pause Music
     pygame.mixer.music.pause()
     
     while pause:
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

          # Makes the text
          largeText = pygame.font.SysFont("comicsansms",115)
          textSurf, textRect = text_objects("Paused", largeText)
          textRect.center = ( (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2) )
          screen.blit(textSurf,textRect)

          # Makes the buttons
          button("Resume",150,450,100,50,GREEN,BRIGHT_GREEN,unpause)
          button("Quit",450,450,100,50,RED,BRIGHT_RED,quit_Game)

          # Displays the buttons and the text
          pygame.display.update()
          clock.tick(15)  
        
# Fuction that restarts the game after he/she loses
def restart():
     global pause
     global score

     # Stop Music
     pygame.mixer.music.stop()
     score = 0
     while pause:
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

          smallText = pygame.font.SysFont("comicsansms",115)
          textSurf, textRect = text_objects("You Lost",smallText)
          textRect.center = ( (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2) )
          screen.blit(textSurf,textRect)

          button("Restart",150,450,100,50,GREEN,BRIGHT_GREEN,playFun)
          button("Quit",450,450,100,50,RED,BRIGHT_RED,quit_Game)

          pygame.display.update()
          clock.tick(15) 

# Fuction that displays the Score  
def Score():
     smallText = pygame.font.Font("freesansbold.ttf",20)
     textSurf, textRect = text_objects(f"Score: {score}",smallText)
     textRect.center = ( SCREEN_WIDTH-70, SCREEN_HEIGHT-30 )
     screen.blit(textSurf,textRect)
     pygame.display.update()

# Change the name of the player
def change_Name(name):
     global player_Name
     player_Name = name

# Fuctoin of the main game
def playFun():
     # Set up the drawing window
     game_screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

     # Enters the Score Variable in the scope of playFun() Function
     global score
     
     # Enter the global variable pause so we can pause the game
     global pause

     # Create a custom event for adding a new enemy
     ADDENEMY = pygame.USEREVENT + 1
     pygame.time.set_timer(ADDENEMY, 250)

     # Instantiate player. 
     player = Player()

     # Create groups to hold enemy sprites and all sprites
     # - enemies is used for collision detection and position updates
     # - all_sprites is used for rendering
     global enemies
     enemies = pygame.sprite.Group()

     # Create groups to hold bullets sprites and all sprites
     # - bullets is used for the shooting function
     # - all_sprites is used for rendering
     global bullets
     bullets = pygame.sprite.Group()

     # Make a group for all sprites
     global all_sprites
     all_sprites = pygame.sprite.Group()
     all_sprites.add(player)

     pygame.mixer.music.load('Music/Background_Music.wav')
     pygame.mixer.music.play(-1)

     # Initialize the running variable
     running = True
     while running:
          Score()
          for event in pygame.event.get():
               if event.type == KEYDOWN:
                    # If player presses Escape
                    if event.key == K_ESCAPE:
                         pause = True
                         # Pause the game
                         paused()
                    

               elif event.type == pygame.QUIT:
                    quit_Game()
               # Add a new enemy?
               elif event.type == ADDENEMY:
                    # Create the new enemy and add it to sprite groups
                    new_enemy = Enemy()
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
               
                    
          # Update all sprites
          all_sprites.update()
          
          # Fills the screen with the color black
          game_screen.fill((255, 255,255))
          
          # Draw all sprites
          for entity in all_sprites:
               screen.blit(entity.surf, entity.rect)
          

          # Check if any enemies have collided with the player
          if pygame.sprite.spritecollideany(player, enemies):
               # If so, then remove the player and stop the loop
               player.kill()
               insert_Data_To_SQL()
               running = False
               pause = True
               restart()


          # Flips the screen
          pygame.display.flip()

          # Ensure program maintains a rate of 30 frames per second
          clock.tick(60)

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
    
    # Text input that takes in the username 
    settings.add.text_input(title="User Name : ", textinput_id="username",default=player_Name,align=pm.locals.ALIGN_LEFT,onchange=change_Name)
    
    # Dummy label to add some spacing between the Restore Defaults button and Return To Main Menu button 
    settings.add.label(title="") 
    
    # Selector to choose between the types of difficulties available 
    settings.add.selector(title="Difficulty\t", items=difficulty,onchange = Game_Difficulty, 
                          selector_id="difficulty", default=0, align=pm.locals.ALIGN_LEFT)
    
    # Dummy label to add some spacing between the Restore Defaults button and Return To Main Menu button 
    settings.add.label(title="") 
    
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
     main_SQL()
