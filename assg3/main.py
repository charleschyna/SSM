import utils.session
import pygame
import random
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Used Car Inventory")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 100, 200)
RED = (200, 0, 0)
GREEN = (0, 150, 0)

# Fonts
title_font = pygame.font.SysFont('Arial', 36, bold=True)
header_font = pygame.font.SysFont('Arial', 24, bold=True)
detail_font = pygame.font.SysFont('Arial', 20)
button_font = pygame.font.SysFont('Arial', 22)

# Vehicle data structure
class Vehicle:
    def __init__(self, vehicle_type):
        self.type = vehicle_type
        self.make = self._get_make()
        self.model = self._get_model()
        self.mileage = random.randint(5000, 80000)
        self.price = self._get_price()
        self.color = self._get_random_color()
        self.passenger_capacity = self._get_capacity()
        self.flower_colors = [self._get_random_color() for _ in range(6)]
        
    def _get_make(self):
        makes = {
            "Car": ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "Volvo"],
            "SUV": ["Toyota", "Honda", "Ford", "Jeep", "Subaru", "Volvo"],
            "Truck": ["Ford", "Chevrolet", "Ram", "Toyota", "GMC", "Volvo"]
        }
        return random.choice(makes[self.type])
    
    def _get_model(self):
        models = {
            "Car": ["Camry", "Civic", "Focus", "Malibu", "Altima", "S60"],
            "SUV": ["RAV4", "CR-V", "Explorer", "XC90", "Outback", "XC60"],
            "Truck": ["F-150", "Silverado", "1500", "Tundra", "Sierra", "VNL"]
        }
        return random.choice(models[self.type])
    
    def _get_price(self):
        if self.type == "Car":
            return round(random.uniform(10000, 30000), 2)
        elif self.type == "SUV":
            return round(random.uniform(20000, 50000), 2)
        else:  # Truck
            return round(random.uniform(30000, 60000), 2)
    
    def _get_capacity(self):
        if self.type == "Car":
            return random.choice([4, 5, 6])
        elif self.type == "SUV":
            return random.choice([5, 7, 8])
        else:  # Truck
            return random.choice([2, 3, 5])
    
    def _get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def regenerate(self):
        self.color = self._get_random_color()
        self.flower_colors = [self._get_random_color() for _ in range(6)]

# Drawing functions
def draw_rounded_rect(surface, color, rect, radius=10):
    x, y, width, height = rect
    pygame.draw.rect(surface, color, (x + radius, y, width - 2*radius, height))
    pygame.draw.rect(surface, color, (x, y + radius, width, height - 2*radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + height - radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + height - radius), radius)

def draw_details_panel(surface, vehicle, x, y):
    # Main panel
    panel_rect = (x, y, 300, 300)
    draw_rounded_rect(surface, GRAY, panel_rect)
    
    # Title
    title = header_font.render(f"{vehicle.make} {vehicle.model}", True, BLACK)
    surface.blit(title, (x + 20, y + 20))
    
    # Details
    details = [
        f"Type: {vehicle.type}",
        f"Mileage: {vehicle.mileage:,} miles",
        f"Price: ${vehicle.price:,.2f}",
        f"Passenger Capacity: {vehicle.passenger_capacity}"
    ]
    
    for i, detail in enumerate(details):
        text = detail_font.render(detail, True, BLACK)
        surface.blit(text, (x + 20, y + 70 + i * 30))

def draw_car(surface, x, y, width, height, color):
    # Main body
    body_height = height // 2
    pygame.draw.rect(surface, color, (x - width//2, y - body_height, width, body_height))
    
    # Roof
    roof_width = width * 0.7
    pygame.draw.rect(surface, color, (x - roof_width//2, y - body_height - height//3, roof_width, height//4))
    
    # Windows
    pygame.draw.rect(surface, (200, 230, 255), (x - width//4, y - body_height - height//6, width//2, height//6))
    
    # Wheels
    wheel_radius = min(width, height) // 4
    pygame.draw.circle(surface, BLACK, (x - width//3, y), wheel_radius)
    pygame.draw.circle(surface, BLACK, (x + width//3, y), wheel_radius)

def draw_suv(surface, x, y, width, height, color):
    # Main body
    body_height = height // 1.8
    pygame.draw.rect(surface, color, (x - width//2, y - body_height, width, body_height))
    
    # Roof
    roof_width = width * 0.8
    roof_height = height // 3
    pygame.draw.rect(surface, color, (x - roof_width//2, y - body_height - roof_height, roof_width, roof_height))
    
    # Windows
    pygame.draw.rect(surface, (200, 230, 255), (x - width//3, y - body_height - roof_height + roof_height*0.1, width//1.5, roof_height*0.7))
    
    # Wheels
    wheel_radius = min(width, height) // 3
    pygame.draw.circle(surface, BLACK, (x - width//3, y), wheel_radius)
    pygame.draw.circle(surface, BLACK, (x + width//3, y), wheel_radius)

def draw_truck(surface, x, y, width, height, color):
    # Cab
    cab_width = width // 2.5
    cab_height = height // 1.5
    pygame.draw.rect(surface, color, (x - width//2, y - cab_height, cab_width, cab_height))
    
    # Trailer
    trailer_height = height // 3
    pygame.draw.rect(surface, color, (x - width//2, y - trailer_height, width, trailer_height))
    
    # Windows
    pygame.draw.rect(surface, (200, 230, 255), (x - width//2 + cab_width*0.15, y - cab_height + cab_height*0.1, cab_width*0.7, cab_height*0.2))
    
    # Wheels
    wheel_radius = min(width, height) // 5
    wheel_positions = [-0.35, -0.1, 0.15, 0.4]
    for pos in wheel_positions:
        wheel_x = x + (width * pos)
        pygame.draw.circle(surface, BLACK, (int(wheel_x), y), wheel_radius)

def draw_flower(surface, x, y, size, color):
    # Stem
    pygame.draw.line(surface, GREEN, (x, y), (x, y + size*2), 2)
    # Flower head
    pygame.draw.circle(surface, color, (x, y), size)

def draw_flowers(surface, x, y, colors):
    positions = [
        (x - 150, y + 100), (x - 90, y + 120), (x - 30, y + 100),
        (x + 30, y + 120), (x + 90, y + 100), (x + 150, y + 120)
    ]
    for (fx, fy), color in zip(positions, colors):
        draw_flower(surface, fx, fy, 15, color)

def draw_button(surface, x, y, width, height, text, color=BLUE, text_color=WHITE):
    draw_rounded_rect(surface, color, (x, y, width, height))
    btn_text = button_font.render(text, True, text_color)
    surface.blit(btn_text, (x + width//2 - btn_text.get_width()//2, y + height//2 - btn_text.get_height()//2))
    return pygame.Rect(x, y, width, height)

# Main function
def main():
    clock = pygame.time.Clock()
    
    # Create vehicles
    car = Vehicle("Car")
    suv = Vehicle("SUV")
    truck = Vehicle("Truck")
    
    current_screen = "menu"  # menu, car, suv, truck
    
    while True:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if current_screen == "menu":
                    if car_btn.collidepoint(mouse_pos):
                        current_screen = "car"
                        car.regenerate()
                    elif suv_btn.collidepoint(mouse_pos):
                        current_screen = "suv"
                        suv.regenerate()
                    elif truck_btn.collidepoint(mouse_pos):
                        current_screen = "truck"
                        truck.regenerate()
                else:
                    if back_btn.collidepoint(mouse_pos):
                        current_screen = "menu"
        
        # Draw title
        title = title_font.render("USED CAR INVENTORY", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        if current_screen == "menu":
            # Draw menu buttons
            car_btn = draw_button(screen, WIDTH//2 - 150, 150, 300, 60, "View Car")
            suv_btn = draw_button(screen, WIDTH//2 - 150, 250, 300, 60, "View SUV")
            truck_btn = draw_button(screen, WIDTH//2 - 150, 350, 300, 60, "View Truck")
            
        elif current_screen == "car":
            # Draw details panel
            draw_details_panel(screen, car, 50, 50)
            
            # Draw car
            draw_car(screen, WIDTH//2, HEIGHT//2, 300, 150, car.color)
            
            # Draw flowers
            draw_flowers(screen, WIDTH//2, HEIGHT//2, car.flower_colors)
            
            # Back button
            back_btn = draw_button(screen, 50, 600, 150, 50, "Back", RED)
            
        elif current_screen == "suv":
            # Draw details panel
            draw_details_panel(screen, suv, 50, 50)
            
            # Draw SUV
            draw_suv(screen, WIDTH//2, HEIGHT//2, 350, 200, suv.color)
            
            # Draw flowers
            draw_flowers(screen, WIDTH//2, HEIGHT//2, suv.flower_colors)
            
            # Back button
            back_btn = draw_button(screen, 50, 600, 150, 50, "Back", RED)
            
        elif current_screen == "truck":
            # Draw details panel
            draw_details_panel(screen, truck, 50, 50)
            
            # Draw truck
            draw_truck(screen, WIDTH//2, HEIGHT//2, 400, 180, truck.color)
            
            # Draw flowers
            draw_flowers(screen, WIDTH//2, HEIGHT//2, truck.flower_colors)
            
            # Back button
            back_btn = draw_button(screen, 50, 600, 150, 50, "Back", RED)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()