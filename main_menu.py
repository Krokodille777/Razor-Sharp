import pygame
# Main menu panel is going to be implemented here.

class MainMenu:
    def __init__(self,screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        #old-school pixelated font 
        self.font = pygame.font.SysFont("Courier New", 48, bold=True)
        self.title_text = self.font.render("Razor Sharp", True, (0, 255, 0))

        # Stylesheet for buttons 
        self.button_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.button_color = (0, 0, 0)
        self.button_color_hover = (0, 255, 0)
        self.border_color = (0, 255, 0)
        self.text_color = (0, 255, 0)
        self.button_width = 200
        self.button_height = 60
        self.button_padding = 20
        self.buttons = {
            "start": {
                "text": self.button_font.render("Start Game", True, self.text_color),
                "rect": pygame.Rect(
                    (self.screen_width - self.button_width) // 2,
                    (self.screen_height - self.button_height) // 2,
                    self.button_width,
                    self.button_height,
                ),
                "border_rect": pygame.Rect(
                    (self.screen_width - self.button_width) // 2 - 2,
                    (self.screen_height - self.button_height) // 2 - 2,
                    self.button_width + 4,
                    self.button_height + 4,
                ),
            },
            "about": {
                "text": self.button_font.render("About", True, self.text_color),
                "rect": pygame.Rect(
                    (self.screen_width - self.button_width) // 2,
                    (self.screen_height - self.button_height) // 2 + self.button_height + self.button_padding,
                    self.button_width,
                    self.button_height,
                ),
                "border_rect": pygame.Rect(
                    (self.screen_width - self.button_width) // 2 - 2,
                    (self.screen_height - self.button_height) // 2 + self.button_height + self.button_padding - 2,
                    self.button_width + 4,
                    self.button_height + 4,
                ),
            },
            "quit": {
                "text": self.button_font.render("Quit", True, self.text_color),
                "rect": pygame.Rect(
                    (self.screen_width - self.button_width) // 2,
                    (self.screen_height - self.button_height) // 2 + 2 * (self.button_height + self.button_padding),
                    self.button_width,
                    self.button_height,
                ),
                "border_rect": pygame.Rect(
                    (self.screen_width - self.button_width) // 2 - 2,
                    (self.screen_height - self.button_height) // 2 + 2 * (self.button_height + self.button_padding) - 2,
                    self.button_width + 4,
                    self.button_height + 4,
                ),
            }
        }


    def draw(self, screen):
        screen.fill((0, 0, 0))
        # Draw title
        title_rect = self.title_text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 4)
        )
        screen.blit(self.title_text, title_rect)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            pygame.draw.rect(screen, self.border_color, button["border_rect"])
            if button["rect"].collidepoint(mouse_pos):
                pygame.draw.rect(screen, self.button_color_hover, button["rect"])
            else:
                pygame.draw.rect(screen, self.button_color, button["rect"])
            text_rect = button["text"].get_rect(center=button["rect"].center)
            screen.blit(button["text"], text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for name, button in self.buttons.items():
                if button["rect"].collidepoint(mouse_pos):
                    return name  # Return the name of the button clicked
        return None
        
class AboutScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_lines = [
            "Razor Sharp is a knife-throwing game where you aim to hit a rotating log.",
            "Each round has different rules and challenges. Can you master the blade?",
            "Created by Krokodille777. Thanks for playing!",


            "Keys and Controls:",
            " SPACE - Throw knife",
            " R - Restart game after victory or defeat",
            " Esc - Return to main menu from about screen or from game itself"
        ]
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        y_offset = self.screen_height // 4
        for line in self.text_lines:
            text_surface = self.font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 40  # Space between lines
