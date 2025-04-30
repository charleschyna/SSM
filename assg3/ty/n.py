import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.widgets import Button

class VehicleVisualizer:
    def __init__(self):
        self.inventory = [
            self.create_car("Toyota", "Camry", 45000, 22000),
            self.create_suv("Ford", "Explorer", 32000, 35000),
            self.create_truck("Chevrolet", "Silverado", 28000, 42000)
        ]
        self.current_index = 0
        
    def get_random_color(self):
        return (random.randint(0, 255)/255, random.randint(0, 255)/255, random.randint(0, 255)/255)
    
    def get_random_pastel_color(self):
        return (random.randint(150, 255)/255, random.randint(150, 255)/255, random.randint(150, 255)/255)
    
    def draw_flowers(self, ax, x, y, z, num_flowers=6):
        for _ in range(num_flowers):
            flower_x = x + random.uniform(-2, 2)
            flower_y = y + random.uniform(-2, 2)
            flower_z = z
            
            # Stem
            ax.plot([flower_x, flower_x], [flower_y, flower_y], [flower_z, flower_z-0.2], 
                    color='green', linewidth=1)
            
            # Flower head
            u = np.linspace(0, 2 * np.pi, 10)
            v = np.linspace(0, np.pi, 10)
            xx = 0.1 * np.outer(np.cos(u), np.sin(v)) + flower_x
            yy = 0.1 * np.outer(np.sin(u), np.sin(v)) + flower_y
            zz = 0.1 * np.outer(np.ones(np.size(u)), np.cos(v)) + flower_z
            ax.plot_surface(xx, yy, zz, color=self.get_random_pastel_color(), alpha=0.8)
    
    def create_car(self, make, model, mileage, price):
        color = self.get_random_color()
        length = random.uniform(4, 5)
        width = random.uniform(1.8, 2)
        height = random.uniform(1.4, 1.6)
        
        def draw(ax):
            # Main body
            x = np.linspace(0, length, 10)
            y = np.linspace(0, width, 10)
            X, Y = np.meshgrid(x, y)
            Z = np.zeros_like(X) + height/2
            ax.plot_surface(X, Y, Z, color=color)
            
            # Roof
            X_roof, Z_roof = np.meshgrid(x, np.linspace(0, height, 10))
            Y_roof = np.zeros_like(X_roof) + width/2
            ax.plot_surface(X_roof, Y_roof, Z_roof, color=color)
            
            # Windows
            ax.plot_surface(X_roof*0.8, Y_roof*0.8, Z_roof*0.8, color=(0, 0.5, 1, 0.3))
            
            # Wheels
            wheel_radius = 0.3
            u = np.linspace(0, 2 * np.pi, 20)
            v = np.linspace(0, np.pi, 20)
            
            for wheel_pos in [0.8, length-0.8]:
                x_wheel = wheel_radius * np.outer(np.cos(u), np.sin(v)) + wheel_pos
                y_wheel = wheel_radius * np.outer(np.sin(u), np.sin(v)) + 0
                z_wheel = wheel_radius * np.outer(np.ones(np.size(u)), np.cos(v)) + 0.2
                ax.plot_surface(x_wheel, y_wheel, z_wheel, color='black')
                
                y_wheel = wheel_radius * np.outer(np.sin(u), np.sin(v)) + width
                ax.plot_surface(x_wheel, y_wheel, z_wheel, color='black')
            
            self.draw_flowers(ax, length/2, width/2, 0)
            ax.set_title(f"{make} {model}\nMileage: {mileage} miles | Price: ${price:,}")
            ax.set_xlim(0, length + 2)
            ax.set_ylim(0, width + 2)
            ax.set_zlim(0, height + 2)
        
        return {'type': 'Car', 'make': make, 'model': model, 'draw': draw, 'length': length}
    
    def create_suv(self, make, model, mileage, price):
        color = self.get_random_color()
        length = random.uniform(4.5, 5.5)
        width = random.uniform(1.9, 2.2)
        height = random.uniform(1.7, 2.0)
        
        def draw(ax):
            # Main body
            x = np.linspace(0, length, 10)
            y = np.linspace(0, width, 10)
            X, Y = np.meshgrid(x, y)
            Z = np.zeros_like(X) + height/2
            ax.plot_surface(X, Y, Z, color=color)
            
            # Roof
            X_roof, Z_roof = np.meshgrid(x, np.linspace(0, height, 10))
            Y_roof = np.zeros_like(X_roof) + width/2
            ax.plot_surface(X_roof, Y_roof, Z_roof, color=color)
            
            # Windows
            ax.plot_surface(X_roof*0.85, Y_roof*0.85, Z_roof*0.85, color=(0, 0.5, 1, 0.3))
            
            # Wheels
            wheel_radius = 0.4
            u = np.linspace(0, 2 * np.pi, 20)
            v = np.linspace(0, np.pi, 20)
            
            for wheel_pos in [0.8, length-0.8]:
                x_wheel = wheel_radius * np.outer(np.cos(u), np.sin(v)) + wheel_pos
                y_wheel = wheel_radius * np.outer(np.sin(u), np.sin(v)) + 0
                z_wheel = wheel_radius * np.outer(np.ones(np.size(u)), np.cos(v)) + 0.3
                ax.plot_surface(x_wheel, y_wheel, z_wheel, color='black')
                
                y_wheel = wheel_radius * np.outer(np.sin(u), np.sin(v)) + width
                ax.plot_surface(x_wheel, y_wheel, z_wheel, color='black')
            
            # Roof rack
            x_rack = np.linspace(length*0.2, length*0.8, 5)
            for x_pos in x_rack:
                ax.plot([x_pos, x_pos], [width*0.2, width*0.8], 
                        [height, height], color='silver', linewidth=2)
            
            self.draw_flowers(ax, length/2, width/2, 0)
            ax.set_title(f"{make} {model} (SUV)\nMileage: {mileage} miles | Price: ${price:,}")
            ax.set_xlim(0, length + 2)
            ax.set_ylim(0, width + 2)
            ax.set_zlim(0, height + 2)
        
        return {'type': 'SUV', 'make': make, 'model': model, 'draw': draw, 'length': length}
    
    def create_truck(self, make, model, mileage, price):
        color = self.get_random_color()
        length = random.uniform(5, 7)
        width = random.uniform(2, 2.5)
        height = random.uniform(2, 2.5)
        
        def draw(ax):
            # Cabin
            cabin_length = length * 0.4
            x_cabin = np.linspace(0, cabin_length, 10)
            y_cabin = np.linspace(0, width, 10)
            
            X_cabin, Y_cabin = np.meshgrid(x_cabin, y_cabin)
            Z_cabin = np.zeros_like(X_cabin) + height/2
            ax.plot_surface(X_cabin, Y_cabin, Z_cabin, color=color)
            
            # Cabin roof
            X_cabin_roof, Z_cabin_roof = np.meshgrid(x_cabin, np.linspace(0, height, 10))
            Y_cabin_roof = np.zeros_like(X_cabin_roof) + width/2
            ax.plot_surface(X_cabin_roof, Y_cabin_roof, Z_cabin_roof, color=color)
            
            # Truck bed
            bed_length = length - cabin_length
            x_bed = np.linspace(cabin_length, length, 10)
            X_bed, Y_bed = np.meshgrid(x_bed, y_cabin)
            Z_bed = np.zeros_like(X_bed) + height*0.5
            ax.plot_surface(X_bed, Y_bed, Z_bed, color=color)
            
            # Wheels
            wheel_radius = 0.5
            u = np.linspace(0, 2 * np.pi, 20)
            v = np.linspace(0, np.pi, 20)
            
            # Front wheels
            wheel_pos = cabin_length*0.7
            x_wheel = wheel_radius * np.outer(np.cos(u), np.sin(v)) + wheel_pos
            y_wheel = wheel_radius * np.outer(np.sin(u), np.sin(v)) + 0
            z_wheel = wheel_radius * np.outer(np.ones(np.size(u)), np.cos(v)) + 0.4
            ax.plot_surface(x_wheel, y_wheel, z_wheel, color='black')
            
            y_wheel = wheel_radius * np.outer(np.sin(u), np.sin(v)) + width
            ax.plot_surface(x_wheel, y_wheel, z_wheel, color='black')
            
            # Rear wheels (double wheels)
            for wheel_pos in [cabin_length + bed_length*0.3, cabin_length + bed_length*0.3 + 0.3]:
                x_wheel = wheel_radius * np.outer(np.cos(u), np.sin(v)) + wheel_pos
                y_wheel = wheel_radius * np.outer(np.sin(u), np.sin(v)) + 0
                z_wheel = wheel_radius * np.outer(np.ones(np.size(u)), np.cos(v)) + 0.4
                ax.plot_surface(x_wheel, y_wheel, z_wheel, color='black')
                
                y_wheel = wheel_radius * np.outer(np.sin(u), np.sin(v)) + width
                ax.plot_surface(x_wheel, y_wheel, z_wheel, color='black')
            
            self.draw_flowers(ax, length/2, width/2, 0)
            ax.set_title(f"{make} {model} (Truck)\nMileage: {mileage} miles | Price: ${price:,}")
            ax.set_xlim(0, length + 2)
            ax.set_ylim(0, width + 2)
            ax.set_zlim(0, height + 2)
        
        return {'type': 'Truck', 'make': make, 'model': model, 'draw': draw, 'length': length}
    
    def show_vehicle(self, index):
        self.current_index = index
        plt.close('all')
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        vehicle = self.inventory[index]
        vehicle['draw'](ax)
        
        ax.set_xlabel('Length (m)')
        ax.set_ylabel('Width (m)')
        ax.set_zlabel('Height (m)')
        
        # Add navigation buttons
        ax_prev = plt.axes([0.2, 0.05, 0.1, 0.075])
        ax_next = plt.axes([0.7, 0.05, 0.1, 0.075])
        
        btn_prev = Button(ax_prev, 'Previous')
        btn_next = Button(ax_next, 'Next')
        
        btn_prev.on_clicked(self.previous_vehicle)
        btn_next.on_clicked(self.next_vehicle)
        
        plt.tight_layout()
        plt.show()
        
    def next_vehicle(self, event):
        self.show_vehicle((self.current_index + 1) % len(self.inventory))
        
    def previous_vehicle(self, event):
        self.show_vehicle((self.current_index - 1) % len(self.inventory))
        
    def start(self):
        self.show_vehicle(0)

if __name__ == "__main__":
    visualizer = VehicleVisualizer()
    visualizer.start()