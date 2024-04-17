import pygame
import sys
from settings import *
from Level import Level
from cursor import Cursor

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Amber's Quest")
        icon = pygame.image.load('ICON.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        # Initialize menu variables
        self.in_menu = True
        self.play_button_img = pygame.image.load('play_button.png').convert_alpha()
        self.background_img = pygame.image.load('backgrounde.png').convert()  # Load background image

        self.play_button_rect = self.play_button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Initialize game entities
        main_sound = pygame.mixer.Sound('../gameproj/audio/main.mp3')
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)
        self.level = None  # Will be initialized after clicking play button
        self.cursor = Cursor()

        # Variables to track game state
        self.play_button_clicked = False
        self.image_displayed = False

    def main_menu(self):
        while self.in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.play_button_rect.collidepoint(mouse_x, mouse_y):
                        self.play_button_clicked = True  # User clicked the play button

            # Draw the background image
            self.screen.blit(self.background_img, (0, 0))

            # Draw play button
            self.screen.blit(self.play_button_img, self.play_button_rect.topleft)

            # Update and draw the cursor
            self.cursor.update()
            self.screen.blit(self.cursor.image, self.cursor.rect.topleft)

            pygame.display.update()
            self.clock.tick(FPS)

            # Start the game if play button was clicked
            if self.play_button_clicked:
                self.in_menu = False
                self.level = Level()

    def cursor_click(self):
        # Display the image only if the play button was clicked and the game has started
        if self.level is not None and not self.image_displayed:
            print("Cursor clicked anywhere!")
            # Coordinates to display the clicked image
            clicked_image_pos = (-300, 410)  # Set your desired coordinates here

            # Load the clicked image
            clicked_image = pygame.image.load('a.png').convert_alpha()

            # Draw the clicked image at the specified position
            self.screen.blit(clicked_image, clicked_image_pos)
            pygame.display.update()
            pygame.time.delay(4000)  # Adjust the delay as needed
            self.screen.blit(self.background_img, (0, 0))  # Clear the clicked image

            self.image_displayed = True

    def quit_game(self):
        pygame.mouse.set_visible(True)  # Show the system cursor before quitting
        pygame.quit()
        sys.exit()

    def run(self):
        self.main_menu()  # Display the main menu

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("Cursor click start")
                    self.cursor_click()
                    print("Cursor click end")

            self.screen.fill('black')

            # Update and draw the level if the game has started
            if self.level is not None:
                self.level.run()

            # Update and draw the cursor
            self.cursor.update()
            self.screen.blit(self.cursor.image, self.cursor.rect.topleft)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
