from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# ------------------ UI / MENU SETUP ------------------ #
menu_bg = Entity(model='quad', texture='Assets/flower sunset.png', scale=Vec2(2, 1), parent=camera.ui, z=1)
menu = Entity(parent=camera.ui)
title = Text("Minecraft", parent=menu, y=0.4, scale=3, origin=(0, 0), color=color.white)

play_button = Button(text="Play", parent=menu, scale=(0.3, 0.1), y=0.1)
settings_button = Button(text="Settings", parent=menu, scale=(0.3, 0.1), y=-0.05)
quit_button = Button(text="Quit", parent=menu, scale=(0.3, 0.1), y=-0.2)

# ------------------ PLAYER SETUP ------------------ #
player = FirstPersonController(enabled=False)
player.speed = 8
player.gravity = 0
mouse.locked = False

# ------------------ WINDOW SETTINGS ------------------ #
window.fullscreen = False
window.borderless = False
window.size = (1000, 700)

# ------------------ SKY ------------------ #
Sky()

# ------------------ CROSSHAIR & HUD ------------------ #
crosshair_size = 0.005
gap = 0.01

# Group all HUD elements together to control visibility
hud = Entity(parent=camera.ui, enabled=False)

Entity(parent=hud, model='quad', color=color.black, scale=(crosshair_size, 0.01), position=(0, gap))
Entity(parent=hud, model='quad', color=color.black, scale=(crosshair_size, 0.01), position=(0, -gap))
Entity(parent=hud, model='quad', color=color.black, scale=(0.01, crosshair_size), position=(gap, 0))
Entity(parent=hud, model='quad', color=color.black, scale=(0.01, crosshair_size), position=(-gap, 0))
Text("Use SPACE to fly and X to go lower", parent=hud, position=(-0.5, 0.45), origin=(-0.5, 0.5), scale=1.2, color=color.azure)

# ------------------ GAME WORLD ------------------ #
boxes = []

def generate_world():
    for i in range(20):
        for j in range(20):
            box = Entity(color=color.white, model='cube', position=(j, 0, i),
                         texture='Assets/grass.png', parent=scene, origin_y=0.5, collider='box')
            boxes.append(box)

# ------------------ GAME STATES ------------------ #
paused = False
pause_text = Text(text='Game Paused', origin=(0, 0), scale=2, color=color.white, enabled=False)
camera_view = camera.fov

# ------------------ BUTTON ACTIONS ------------------ #
def start_game():
    menu.enabled = False
    menu_bg.enabled = False
    hud.enabled = True         # ✅ Show the HUD only now
    player.enabled = True
    mouse.locked = True

play_button.on_click = start_game
quit_button.on_click = application.quit

# ------------------ INPUT HANDLING ------------------ #
def input(key):
    pause_logic(key)
    zoom_logic(key)

    if paused:
        return

    for box in boxes:
        if box.hovered:
            if key == 'left mouse down':
                new = Entity(color=color.white, model='cube', position=box.position + mouse.normal + Vec3(0, 0.01, 0),
                             texture='Assets/rock.png', parent=scene, origin_y=0.5, collider='box')
                boxes.append(new)
            if key == 'right mouse down':
                boxes.remove(box)
                destroy(box)

# ------------------ GAME LOOP ------------------ #
def update():
    global camera_view
    camera.fov += (camera_view - camera.fov) * 4 * time.dt
    if not paused:
        movement_logic()

def movement_logic():
    if held_keys['space']:
        player.y += time.dt * player.speed
    if held_keys['x']:
        player.y -= time.dt * player.speed

def pause_logic(key):
    global paused

    if key == 'escape':
        paused = not paused
        pause_text.enabled = paused
        mouse.locked = not paused
        player.enabled = not paused

def zoom_logic(key):
    global camera_view
    if key == 'scroll up':
        camera_view = max(10, camera_view - 5)
    elif key == 'scroll down':
        camera_view = min(120, camera_view + 5)

# ------------------ START ------------------ #
generate_world()
app.run()
