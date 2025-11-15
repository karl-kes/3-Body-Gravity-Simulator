import numpy as np

def generate_cluster():
    n_bodies = 100
    radius = 1.0e11  # 100 million km cluster
    
    print(f"Generating {n_bodies} bodies...")

    with open('bodies.csv', 'w') as f:
        # Write header comment
        f.write("# Cluster Simulation\n")
        
        for i in range(n_bodies):
            # 1. Random Position in a Sphere
            u, v, w = np.random.random(3)
            r = radius * (u ** (1/3))
            theta = np.arccos(2 * v - 1)
            phi = 2 * np.pi * w
            
            x = r * np.sin(theta) * np.cos(phi)
            y = r * np.sin(theta) * np.sin(phi)
            z = r * np.cos(theta)
            
            # 2. Velocity
            dist = np.sqrt(x*x + y*y + z*z)
            base_vel = 10000.0
            
            # Add some randomness so it looks chaotic
            vx = np.random.uniform(-base_vel, base_vel)
            vy = np.random.uniform(-base_vel, base_vel)
            vz = np.random.uniform(-base_vel, base_vel)
            
            # 3. Random Mass (Between 1e24 and 1e26 kg)
            mass = 10 ** np.random.uniform(24, 26)
            
            # Write line: x, y, z, vx, vy, vz, mass
            f.write(f"{x},{y},{z},{vx},{vy},{vz},{mass}\n")

    print("Success: 'bodies.csv' created.")

if __name__ == "__main__":
    generate_cluster()