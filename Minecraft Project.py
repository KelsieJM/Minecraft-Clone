from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
player.speed = 8
player.gravity = 0
window.fullscreen = False
window.borderless = False
window.size = (1000, 700)
paused = False
pause_text = Text(text='Game Paused', origin=(0,0), scale=2, color=color.white, enabled=False)
Sky()

crosshair_size = 0.005
gap = 0.01

Entity(parent=camera.ui, model='quad', color=color.black, scale=(crosshair_size, 0.01), position=(0, gap))
Entity(parent=camera.ui, model='quad', color=color.black, scale=(crosshair_size, 0.01), position=(0, -gap))
Entity(parent=camera.ui, model='quad', color=color.black, scale=(0.01, crosshair_size), position=(gap, 0))
Entity(parent=camera.ui, model='quad', color=color.black, scale=(0.01, crosshair_size), position=(-gap, 0))
Text("Use SPACE to fly and X to go lower", parent=camera.ui, position=(-0.5, 0.45), origin=(-0.5, 0.5), scale=1.2, color=color.azure)

boxes = []
for i in range(20):
  for j in range(20):
    box = Button(color=color.white, model='cube', position=(j,0,i),
          texture='Assets/grass.png', parent=scene, origin_y=0.5)
    boxes.append(box)

def input(key):
  pause_logic(key)

  for box in boxes:
    if box.hovered:
      if key == 'left mouse down':
        new = Button(color=color.white, model='cube', position=box.position + mouse.normal,
                    texture='Assets/rock.png', parent=scene, origin_y=0.5)
        boxes.append(new)
      if key == 'right mouse down':
        boxes.remove(box)
        destroy(box)

def update():
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

    if paused:
        return

app.run()