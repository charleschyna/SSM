import pygame
import random
import math
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Used Car Inventory")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 128, 0)
WINDOW_COLOR = (200, 230, 255)
HEADLIGHT_COLOR = (255, 255, 200)
RED = (200, 0, 0)

# Font
font = pygame.font.SysFont('Arial', 20)
title_font = pygame.font.SysFont('Arial', 30, bold=True)

# Vehicle details generator
def generate_vehicle_details(vehicle_type):
    makes_models = {
        "Car": [("Toyota", "Corolla"), ("Honda", "Civic"), ("Ford", "Focus"), 
                ("Chevrolet", "Malibu"), ("Nissan", "Altima")],
        "SUV": [("Toyota", "RAV4"), ("Honda", "CR-V"), ("Ford", "Explorer"),
                ("Jeep", "Grand Cherokee"), ("Subaru", "Outback")],
        "Truck": [("Ford", "F-150"), ("Chevrolet", "Silverado"), ("Ram", "1500"),
                  ("Toyota", "Tundra"), ("GMC", "Sierra")]
    }
    
    make, model = random.choice(makes_models[vehicle_type])
    mileage = random.randint(1000, 100000)
    price = random.randint(5000, 30000) if vehicle_type == "Car" else \
            random.randint(15000, 45000) if vehicle_type == "SUV" else \
            random.randint(25000, 60000)
    
    return {
        "type": vehicle_type,
        "make": make,
        "model": model,
        "mileage": mileage,
        "price": price
    }

# Random color generator
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Draw a flower with fixed colors
def draw_flower(surface, x, y, size, color1, color2):
    # Stem
    pygame.draw.line(surface, GREEN, (x, y), (x, y + size*2), 2)
    
    # Petals
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        petal_x = x + math.cos(rad) * size
        petal_y = y + math.sin(rad) * size
        pygame.draw.circle(surface, color1, (int(petal_x), int(petal_y)), size//2)
    
    # Center
    pygame.draw.circle(surface, color2, (x, y), size//3)

# Draw a car with clear front/back
def draw_car(surface, x, y, width, height, color):
    # Main body
    body_height = height // 2
    pygame.draw.rect(surface, color, (x - width//2, y - body_height, width, body_height))
    
    # Roof
    roof_width = width * 0.7
    pygame.draw.rect(surface, color, (x - roof_width//2, y - body_height - height//3, roof_width, height//4))
    
    # Front windshield
    front_windshield = [(x - roof_width//2, y - body_height - height//4),
                       (x - roof_width//4, y - body_height),
                       (x + roof_width//4, y - body_height),
                       (x + roof_width//2, y - body_height - height//4)]
    pygame.draw.polygon(surface, WINDOW_COLOR, front_windshield)
    
    # Rear windshield
    rear_windshield = [(x - roof_width//2, y - body_height - height//4),
                      (x - roof_width//4, y - body_height),
                      (x + roof_width//4, y - body_height),
                      (x + roof_width//2, y - body_height - height//4)]
    pygame.draw.polygon(surface, WINDOW_COLOR, rear_windshield)
    
    # Front of car (grill/bumper)
    pygame.draw.rect(surface, DARK_GRAY, (x + width//2 - width//10, y - body_height, width//10, body_height//3))
    
    # Headlights
    pygame.draw.ellipse(surface, HEADLIGHT_COLOR, (x + width//2 - width//8, y - body_height + height//10, width//6, height//8))
    
    # Wheels
    wheel_radius = min(width, height) // 4
    pygame.draw.circle(surface, BLACK, (x - width//3, y), wheel_radius)
    pygame.draw.circle(surface, BLACK, (x + width//3, y), wheel_radius)
    pygame.draw.circle(surface, GRAY, (x - width//3, y), wheel_radius//2)
    pygame.draw.circle(surface, GRAY, (x + width//3, y), wheel_radius//2)
    
    # Side windows
    pygame.draw.rect(surface, WINDOW_COLOR, (x - width//4, y - body_height - height//6, width//2, height//6))

# Draw an SUV with clear front/back
def draw_suv(surface, x, y, width, height, color):
    # Main body
    body_height = height // 1.8
    pygame.draw.rect(surface, color, (x - width//2, y - body_height, width, body_height))
    
    # Roof
    roof_width = width * 0.8
    roof_height = height // 3
    pygame.draw.rect(surface, color, (x - roof_width//2, y - body_height - roof_height, roof_width, roof_height))
    
    # Front windshield
    front_windshield = [(x - roof_width//2, y - body_height - roof_height),
                       (x - roof_width//4, y - body_height),
                       (x + roof_width//4, y - body_height),
                       (x + roof_width//2, y - body_height - roof_height)]
    pygame.draw.polygon(surface, WINDOW_COLOR, front_windshield)
    
    # Front of SUV (grill/bumper)
    pygame.draw.rect(surface, DARK_GRAY, (x + width//2 - width//8, y - body_height, width//8, body_height//3))
    
    # Headlights
    pygame.draw.ellipse(surface, HEADLIGHT_COLOR, (x + width//2 - width//6, y - body_height + height//10, width//5, height//7))
    
    # Wheels (larger for SUV)
    wheel_radius = min(width, height) // 3
    pygame.draw.circle(surface, BLACK, (x - width//3, y), wheel_radius)
    pygame.draw.circle(surface, BLACK, (x + width//3, y), wheel_radius)
    pygame.draw.circle(surface, GRAY, (x - width//3, y), wheel_radius//2)
    pygame.draw.circle(surface, GRAY, (x + width//3, y), wheel_radius//2)
    
    # Side windows
    window_height = roof_height * 0.7
    pygame.draw.rect(surface, WINDOW_COLOR, (x - width//3, y - body_height - roof_height + roof_height*0.1, width//1.5, window_height))

# Draw a truck with clear front/back
def draw_truck(surface, x, y, width, height, color):
    # Cab
    cab_width = width // 2.5
    cab_height = height // 1.5
    pygame.draw.rect(surface, color, (x - width//2, y - cab_height, cab_width, cab_height))
    
    # Trailer
    trailer_width = width
    trailer_height = height // 3
    pygame.draw.rect(surface, color, (x - width//2, y - trailer_height, trailer_width, trailer_height))
    
    # Front windshield
    windshield_width = cab_width * 0.7
    windshield_points = [
        (x - width//2 + cab_width*0.15, y - cab_height),
        (x - width//2 + cab_width*0.15, y - cab_height + cab_height*0.3),
        (x - width//2 + cab_width*0.85, y - cab_height + cab_height*0.3),
        (x - width//2 + cab_width*0.85, y - cab_height)
    ]
    pygame.draw.polygon(surface, WINDOW_COLOR, windshield_points)
    
    # Front of truck (grill)
    grill_height = cab_height * 0.3
    pygame.draw.rect(surface, DARK_GRAY, (x - width//2 + cab_width, y - grill_height, cab_width*0.3, grill_height))
    
    # Headlights
    pygame.draw.ellipse(surface, HEADLIGHT_COLOR, (x - width//2 + cab_width*1.3, y - grill_height + grill_height*0.2, cab_width*0.2, grill_height*0.6))
    
    # Wheels (more wheels for truck)
    wheel_radius = min(width, height) // 5
    wheel_positions = [-0.35, -0.1, 0.15, 0.4]  # Positions relative to truck width
    
    for pos in wheel_positions:
        wheel_x = x + (width * pos)
        pygame.draw.circle(surface, BLACK, (int(wheel_x), y), wheel_radius)
        pygame.draw.circle(surface, GRAY, (int(wheel_x), y), wheel_radius//2)
    
    # Side window
    pygame.draw.rect(surface, WINDOW_COLOR, (x - width//2 + cab_width*0.15, y - cab_height + cab_height*0.1, cab_width*0.7, cab_height*0.2))
    
    # Exhaust pipe
    pygame.draw.rect(surface, DARK_GRAY, (x - width//2 + cab_width*0.1, y - cab_height*0.7, cab_width*0.08, cab_height*0.4))

# Draw vehicle details
def draw_details(surface, vehicle, x, y):
    details = [
        f"Type: {vehicle['type']}",
        f"Make: {vehicle['make']}",
        f"Model: {vehicle['model']}",
        f"Mileage: {vehicle['mileage']} miles",
        f"Price: ${vehicle['price']:,}"
    ]
    
    for i, detail in enumerate(details):
        text = font.render(detail, True, BLACK)
        surface.blit(text, (x, y + i * 30))

# Main menu
def main_menu():
    current_screen = "menu"
    
    # Initialize vehicle data with details that won't change when reselecting
    car_data = {
        "details": generate_vehicle_details("Car"),
        "color": random_color(),
        "flower_colors": [],
        "width": random.randint(200, 300),
        "height": random.randint(100, 150)
    }
    
    suv_data = {
        "details": generate_vehicle_details("SUV"),
        "color": random_color(),
        "flower_colors": [],
        "width": random.randint(250, 350),
        "height": random.randint(150, 200)
    }
    
    truck_data = {
        "details": generate_vehicle_details("Truck"),
        "color": random_color(),
        "flower_colors": [],
        "width": random.randint(350, 450),
        "height": random.randint(120, 180)
    }
    
    # Generate flower colors for each vehicle type
    for _ in range(6):
        car_data["flower_colors"].append((random_color(), random_color()))
        suv_data["flower_colors"].append((random_color(), random_color()))
        truck_data["flower_colors"].append((random_color(), random_color()))
    
    while True:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if current_screen == "menu":
                    if 400 <= mouse_pos[0] <= 800 and 200 <= mouse_pos[1] <= 280:
                        current_screen = "car"
                        # Only change color and dimensions, not details
                        car_data["color"] = random_color()
                        car_data["width"] = random.randint(200, 300)
                        car_data["height"] = random.randint(100, 150)
                        # Regenerate flower colors
                        car_data["flower_colors"] = []
                        for _ in range(6):
                            car_data["flower_colors"].append((random_color(), random_color()))
                    elif 400 <= mouse_pos[0] <= 800 and 320 <= mouse_pos[1] <= 400:
                        current_screen = "suv"
                        # Only change color and dimensions, not details
                        suv_data["color"] = random_color()
                        suv_data["width"] = random.randint(250, 350)
                        suv_data["height"] = random.randint(150, 200)
                        # Regenerate flower colors
                        suv_data["flower_colors"] = []
                        for _ in range(6):
                            suv_data["flower_colors"].append((random_color(), random_color()))
                    elif 400 <= mouse_pos[0] <= 800 and 440 <= mouse_pos[1] <= 520:
                        current_screen = "truck"
                        # Only change color and dimensions, not details
                        truck_data["color"] = random_color()
                        truck_data["width"] = random.randint(350, 450)
                        truck_data["height"] = random.randint(120, 180)
                        # Regenerate flower colors
                        truck_data["flower_colors"] = []
                        for _ in range(6):
                            truck_data["flower_colors"].append((random_color(), random_color()))
                else:
                    if 50 <= mouse_pos[0] <= 200 and 700 <= mouse_pos[1] <= 750:
                        current_screen = "menu"
        
        if current_screen == "menu":
            # Draw title
            title = title_font.render("Used Car Inventory", True, BLACK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            # Draw buttons
            pygame.draw.rect(screen, (200, 200, 255), (400, 200, 400, 80))
            pygame.draw.rect(screen, (200, 255, 200), (400, 320, 400, 80))
            pygame.draw.rect(screen, (255, 200, 200), (400, 440, 400, 80))
            
            car_text = font.render("View Car", True, BLACK)
            suv_text = font.render("View SUV", True, BLACK)
            truck_text = font.render("View Truck", True, BLACK)
            
            screen.blit(car_text, (600 - car_text.get_width()//2, 240 - car_text.get_height()//2))
            screen.blit(suv_text, (600 - suv_text.get_width()//2, 360 - suv_text.get_height()//2))
            screen.blit(truck_text, (600 - truck_text.get_width()//2, 480 - truck_text.get_height()//2))
        
        elif current_screen == "car":
            screen.fill(WHITE)
            
            # Draw car with current dimensions and color
            draw_car(screen, WIDTH//2, HEIGHT//2 + 150, car_data["width"], car_data["height"], car_data["color"])
            
            # Draw flowers in a straight line at the bottom with current colors
            flower_spacing = WIDTH // 7
            for i in range(6):
                x_pos = (i+1) * flower_spacing
                color1, color2 = car_data["flower_colors"][i]
                draw_flower(screen, x_pos, HEIGHT - 50, 20, color1, color2)
            
            # Draw details (these remain the same)
            draw_details(screen, car_data["details"], 50, 50)
            
            # Add label showing front of vehicle
            front_label = font.render("FRONT →", True, RED)
            screen.blit(front_label, (WIDTH//2 + car_data["width"]//2 + 10, HEIGHT//2 + 150 - car_data["height"]//2))
            
            # Back button
            pygame.draw.rect(screen, GRAY, (50, 700, 150, 50))
            back_text = font.render("Back to Menu", True, BLACK)
            screen.blit(back_text, (125 - back_text.get_width()//2, 725 - back_text.get_height()//2))
        
        elif current_screen == "suv":
            screen.fill(WHITE)
            
            # Draw SUV with current dimensions and color
            draw_suv(screen, WIDTH//2, HEIGHT//2 + 150, suv_data["width"], suv_data["height"], suv_data["color"])
            
            # Draw flowers in a straight line at the bottom with current colors
            flower_spacing = WIDTH // 7
            for i in range(6):
                x_pos = (i+1) * flower_spacing
                color1, color2 = suv_data["flower_colors"][i]
                draw_flower(screen, x_pos, HEIGHT - 50, 20, color1, color2)
            
            # Draw details (these remain the same)
            draw_details(screen, suv_data["details"], 50, 50)
            
            # Add label showing front of vehicle
            front_label = font.render("FRONT →", True, RED)
            screen.blit(front_label, (WIDTH//2 + suv_data["width"]//2 + 10, HEIGHT//2 + 150 - suv_data["height"]//2))
            
            # Back button
            pygame.draw.rect(screen, GRAY, (50, 700, 150, 50))
            back_text = font.render("Back to Menu", True, BLACK)
            screen.blit(back_text, (125 - back_text.get_width()//2, 725 - back_text.get_height()//2))
        
        elif current_screen == "truck":
            screen.fill(WHITE)
            
            # Draw Truck with current dimensions and color
            draw_truck(screen, WIDTH//2, HEIGHT//2 + 150, truck_data["width"], truck_data["height"], truck_data["color"])
            
            # Draw flowers in a straight line at the bottom with current colors
            flower_spacing = WIDTH // 7
            for i in range(6):
                x_pos = (i+1) * flower_spacing
                color1, color2 = truck_data["flower_colors"][i]
                draw_flower(screen, x_pos, HEIGHT - 50, 20, color1, color2)
            
            # Draw details (these remain the same)
            draw_details(screen, truck_data["details"], 50, 50)
            
            # Add label showing front of vehicle
            front_label = font.render("FRONT →", True, RED)
            screen.blit(front_label, (WIDTH//2 + truck_data["width"]//2 + 10, HEIGHT//2 + 150 - truck_data["height"]//2))
            
            # Back button
            pygame.draw.rect(screen, GRAY, (50, 700, 150, 50))
            back_text = font.render("Back to Menu", True, BLACK)
            screen.blit(back_text, (125 - back_text.get_width()//2, 725 - back_text.get_height()//2))
        
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()