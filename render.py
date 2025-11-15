from vpython import *
import pandas as pd

# 1. Load Data
data = pd.read_csv('trajectories.csv')
cols = ['x', 'y', 'z', 'body_id', 'step']
for col in cols:
    if col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')
data.dropna(inplace=True)
data['body_id'] = data['body_id'].astype(int)
data['step'] = data['step'].astype(int)
body_ids = data['body_id'].unique()
print(f"Loaded {len(data)} valid rows for {len(body_ids)} bodies.")

# 2. Setup the Scene with Resizable Window
scene.title = "Orbital Simulation with Space-Time Grid"
scene.background = color.black
scene.width = 1200  # Initial width
scene.height = 800  # Initial height
scene.resizable = True  # Enable window resizing
scene.autoscale = False  # Disable autoscaling to maintain view
scene.range = 5e11
scene.userzoom = True  # Allow user to zoom
scene.userspin = True  # Allow user to rotate view
scene.userpan = True  # Allow user to pan view

# Add camera controls info
scene.caption = """<b>Controls:</b>
• Right-click drag: Rotate view
• Mouse wheel or pinch: Zoom in/out  
• Shift + Left-click drag: Pan view
• Window is resizable - drag edges to resize
"""

# 3. Create Coordinate Axes
axis_length = scene.range * 1.2
axis_thickness = scene.range * 0.002
axis_opacity = 0.6

# Function to calculate label size based on scene
def get_label_size():
    return int(scene.width / 50)  # Dynamic label size based on window width

# X-axis (Red)
x_axis = arrow(pos=vector(0, 0, 0), 
               axis=vector(axis_length, 0, 0),
               shaftwidth=axis_thickness,
               color=color.red,
               opacity=axis_opacity)
x_label = label(pos=vector(axis_length, 0, 0),
                text='X',
                color=color.red,
                opacity=0.8,
                height=get_label_size(),
                box=False)

# Y-axis (Green)
y_axis = arrow(pos=vector(0, 0, 0),
               axis=vector(0, axis_length, 0),
               shaftwidth=axis_thickness,
               color=color.green,
               opacity=axis_opacity)
y_label = label(pos=vector(0, axis_length, 0),
                text='Y',
                color=color.green,
                opacity=0.8,
                height=get_label_size(),
                box=False)

# Z-axis (Blue)
z_axis = arrow(pos=vector(0, 0, 0),
               axis=vector(0, 0, axis_length),
               shaftwidth=axis_thickness,
               color=color.blue,
               opacity=axis_opacity)
z_label = label(pos=vector(0, 0, axis_length),
                text='Z',
                color=color.blue,
                opacity=0.8,
                height=get_label_size(),
                box=False)

# 4. Create Space-Time Grid
grid_size = scene.range
grid_spacing = grid_size / 5  # 5 divisions per axis
grid_color = color.gray(0.2)  # Very faint gray
grid_thickness = scene.range * 0.0005
grid_opacity = 0.15  # Very transparent

# XY plane grid
for i in range(-5, 6):
    # Lines parallel to X axis
    curve(pos=[vector(-grid_size, i * grid_spacing, 0),
               vector(grid_size, i * grid_spacing, 0)],
          color=grid_color,
          radius=grid_thickness,
          opacity=grid_opacity)
    # Lines parallel to Y axis
    curve(pos=[vector(i * grid_spacing, -grid_size, 0),
               vector(i * grid_spacing, grid_size, 0)],
          color=grid_color,
          radius=grid_thickness,
          opacity=grid_opacity)

# XZ plane grid
for i in range(-5, 6):
    # Lines parallel to X axis
    curve(pos=[vector(-grid_size, 0, i * grid_spacing),
               vector(grid_size, 0, i * grid_spacing)],
          color=grid_color,
          radius=grid_thickness,
          opacity=grid_opacity)
    # Lines parallel to Z axis
    curve(pos=[vector(i * grid_spacing, 0, -grid_size),
               vector(i * grid_spacing, 0, grid_size)],
          color=grid_color,
          radius=grid_thickness,
          opacity=grid_opacity)

# YZ plane grid
for i in range(-5, 6):
    # Lines parallel to Y axis
    curve(pos=[vector(0, -grid_size, i * grid_spacing),
               vector(0, grid_size, i * grid_spacing)],
          color=grid_color,
          radius=grid_thickness,
          opacity=grid_opacity)
    # Lines parallel to Z axis
    curve(pos=[vector(0, i * grid_spacing, -grid_size),
               vector(0, i * grid_spacing, grid_size)],
          color=grid_color,
          radius=grid_thickness,
          opacity=grid_opacity)

# 5. Create Objects
spheres = []
colors = [color.red, color.cyan, color.yellow, color.green, color.magenta, color.orange, color.white]
for idx, b_id in enumerate(body_ids):
    col = colors[idx % len(colors)]
    obj = sphere(
        radius=2e9,
        color=col, 
        make_trail=True, 
        trail_type="curve", 
        retain=100
    )
    spheres.append(obj)

# 6. Animation Controls
running = True
animation_speed = 60  # Default frame rate

def play_pause(b):
    global running
    running = not running
    b.text = "Play" if not running else "Pause"

def speed_up(b):
    global animation_speed
    animation_speed = min(animation_speed + 20, 200)
    speed_label.text = f"Speed: {animation_speed} fps"

def slow_down(b):
    global animation_speed
    animation_speed = max(animation_speed - 20, 10)
    speed_label.text = f"Speed: {animation_speed} fps"

def reset_view(b):
    scene.range = 5e11
    scene.forward = vector(0, 0, -1)
    scene.up = vector(0, 1, 0)

# Create control buttons
scene.append_to_caption('\n\n')
button(text="Pause", bind=play_pause)
scene.append_to_caption('   ')
button(text="Speed -", bind=slow_down)
scene.append_to_caption('   ')
button(text="Speed +", bind=speed_up)
scene.append_to_caption('   ')
button(text="Reset View", bind=reset_view)
scene.append_to_caption('\n')
speed_label = wtext(text=f"Speed: {animation_speed} fps")

# 7. Animation Loop
steps = data['step'].unique()
current_step = 0

while current_step < len(steps):
    rate(animation_speed)
    
    if running:
        s = steps[current_step]
        step_data = data[data['step'] == s]
        
        for i, b_id in enumerate(body_ids):
            row = step_data[step_data['body_id'] == b_id]
            if not row.empty:
                new_pos = vector(row['x'].values[0], row['y'].values[0], row['z'].values[0])
                spheres[i].pos = new_pos
        
        current_step += 1
        
        # Loop back to beginning when finished
        if current_step >= len(steps):
            current_step = 0
            print("Simulation restarting...")

print("Simulation finished.")