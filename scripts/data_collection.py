import carla, time, pygame, math, random, cv2
import numpy as np

def spawn_vehicle(vehicle_index=0, spawn_index=0, pattern='vehicle.*'):
  blueprint_library = world.get_blueprint_library()
  vehicle_bp = blueprint_library.filter(pattern)[vehicle_index]
  spawn_point = world.get_map().get_spawn_points()[spawn_index]
  vehicle = world.spawn_actor(vehicle_bp, spawn_point)
  return vehicle

def spawn_camera(attach_to=None, transform=carla.Transform(carla.Location(x=1.5, z=1.5), carla.Rotation(pitch=-10)), width=800, height=600, frequency = 0):
  camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
  camera_bp.set_attribute('image_size_x', str(width))
  camera_bp.set_attribute('image_size_y', str(height))
  camera_bp.set_attribute('sensor_tick', str(frequency))
  camera = world.spawn_actor(camera_bp, transform, attach_to=attach_to)
  return camera

try:
  client = carla.Client('localhost', 2000)
  client.set_timeout(10.0)

  world = client.get_world()
  spectator = world.get_spectator()

  settings = world.get_settings()
  settings.synchronous_mode = True
  settings.fixed_delta_seconds = 0.05
  world.apply_settings(settings)

  vehicle = spawn_vehicle(spawn_index=40, pattern="vehicle.dodge.charger_2020")
  
  transforms = [
      carla.Transform(carla.Location(x=-0.16, y=-0.9, z=2.4), carla.Rotation(yaw=-100)),  # Left side camera
      carla.Transform(carla.Location(x=-0.16, y=0.9, z=2.4), carla.Rotation(yaw=100)),  # Right side camera
      carla.Transform(carla.Location(x=-1.5, z=2.4), carla.Rotation(yaw=180))  # Rear camera
  ]
  cameras = []

  for i in range(3):
    camera = spawn_camera(attach_to=vehicle, transform=transforms[i], frequency=0.5, width=300, height=300)
    camera.listen(lambda image, idx=i: image.save_to_disk(f'output_5/{idx}/{image.frame}.png'))
    cameras.append(camera)

  vehicle.set_autopilot(True, 8000)

  while(True):
    world.wait_for_tick()

finally:
  vehicle.destroy()
  camera.destroy()
  settings = world.get_settings()
  settings.synchronous_mode = False
  settings.no_rendering_mode = False
  settings.fixed_delta_seconds = None
  world.apply_settings(settings)