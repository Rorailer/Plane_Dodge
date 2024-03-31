import pygame
from random import randint

#!/home/cryption/Documents/Projects/Snake/snake/bin/python3

from pygame import (K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYDOWN,K_ESCAPE,K_SPACE,RLEACCEL, QUIT)


# Starting pygame and creating window
pygame.init()
    
window_height = 1080
window_width = 1920

window = pygame.display.set_mode((window_width,window_height))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        image = pygame.image.load("image.png").convert_alpha()
        scaled = pygame.transform.scale(image,(50,50))
        self.surf = scaled
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self,pressed_keys):
        # Player Movement
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2,0)

        # Keep Player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_width:
            self.rect.right = window_width
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height
        if self.rect.top < 0:
            self.rect.top = 0
        

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((15, 20))
        self.surf.fill((96,75,17))
        self.rect = self.surf.get_rect(
            center=(
            randint(window_width+20,window_width+100),
            randint(0,window_height),
        )
    )
        self.speed=  randint(1,6)
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Clouds(pygame.sprite.Sprite):

    def __init__(self):
        super(Clouds, self).__init__()
        image = pygame.image.load('cloud.png')
        scaled = pygame.transform.scale(image,(35,35))
        self.surf = scaled
        self.rect = self.surf.get_rect(
            center=(
            randint(window_width+20,window_width+100),
            randint(0,window_height),
        )
    )
        self.speed= 1 #randint(1,3)
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


def score():
    pass


def main():
    running = False  # Flag to control the game loop
    wait = True  # Flag to control the waiting screen loop
    
    while wait:
        for event in pygame.event.get():
            if event.type == QUIT:
                wait = False  # Exit the waiting screen loop if the user closes the window
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    wait = False  # Exit the waiting screen loop if the user presses the ESC key
                else:
                    wait = False  # Exit the waiting screen loop if the user presses any other key
                    running = True  # Start the game loop
        
        # Starting pygame and creating the screen
        # Color Windows
        window.fill('blue')
        
        text = 'Press any key to start'
        font = pygame.font.Font(None, 36)  # You can choose the font and size here
        text_surface = font.render(text, True, (255, 255, 255))  # RGB color for the text (white in this case)
        text_rect = text_surface.get_rect(center=(400, 300))  # Position the text at the center of the screen
        window.blit(text_surface, text_rect)  # Blit (draw) the text surface onto the screen
        
        clock = pygame.time.Clock()
        clock.tick(24)  # Limit the frame rate to 24 frames per second
        
        ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(ADDENEMY, 250)  # Create a timer event that triggers every 250 milliseconds
        ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(ADDCLOUD, 750)  # Create a timer event that triggers every 750 milliseconds
        
        player = Player()  # Create an instance of the Player class
        clouds = pygame.sprite.Group()  # Create a group to hold the cloud sprites
        enemies = pygame.sprite.Group()  # Create a group to hold the enemy sprites
        all_sprites = pygame.sprite.Group()  # Create a group to hold all sprites
        all_sprites.add(player)  # Add the player sprite to the all_sprites group
        
        pygame.display.flip()  # Update the display
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False  # Exit the game loop if the user closes the window
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False  # Exit the game loop if the user presses the ESC key
                elif event.type == ADDENEMY:
                    new_enemy = Enemy()  # Create a new instance of the Enemy class
                    enemies.add(new_enemy)  # Add the enemy sprite to the enemies group
                    all_sprites.add(new_enemy)  # Add the enemy sprite to the all_sprites group
                elif event.type == ADDCLOUD:
                    new_cloud = Clouds()  # Create a new instance of the Clouds class
                    clouds.add(new_cloud)  # Add the cloud sprite to the clouds group
                    all_sprites.add(new_cloud)  # Add the cloud sprite to the all_sprites group
                    
            pressed_keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
        
            clouds.update()  # Update the position of the cloud sprites
            player.update(pressed_keys)  # Update the position of the player sprite
            enemies.update()  # Update the position of the enemy sprites
            window.fill('light blue')  # Clear the screen with a light blue color
            
            for entity in all_sprites:
                window.blit(entity.surf, entity.rect)  # Draw each sprite onto the screen
            
            if pygame.sprite.spritecollideany(player, enemies):
                player.kill()  # Kill the player sprite if it collides with any enemy sprite
                running = False  # Exit the game loop
            
            pygame.display.flip()  # Update the display


main()
