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

def spawn_radar(attach_to=None, transform=carla.Transform(carla.Location(x=1.5, z=1.5), carla.Rotation(pitch=-10)), horizontal_fov = 35, vertical_fov = 20):
    radar_bp = world.get_blueprint_library().find('sensor.other.radar')
    radar_bp.set_attribute('horizontal_fov', str(horizontal_fov))
    radar_bp.set_attribute('vertical_fov', str(vertical_fov))
    radar = world.spawn_actor(radar_bp, transform, attach_to=attach_to)
    return radar

def radar_callback(radar_data):
    current_rot = radar_data.transform.rotation
    for detect in radar_data:
        azi = math.degrees(detect.azimuth)
        alt = math.degrees(detect.altitude)
        # The 0.25 adjusts a bit the distance so the dots can be properly seen
        fw_vec = carla.Vector3D(x=detect.depth)
        # fw_vec = carla.Vector3D(x=detect.depth - 0.25)
        carla.Transform(
            carla.Location(),
            carla.Rotation(
                pitch=current_rot.pitch + alt,
                yaw=current_rot.yaw + azi,
                roll=current_rot.roll)).transform(fw_vec)
        def clamp(min_v, max_v, value):
            return max(min_v, min(value, max_v))
        norm_velocity = detect.velocity / 7.5 # range [-1, 1]
        r = int(clamp(0.0, 1.0, 1.0 - norm_velocity) * 255.0)
        g = int(clamp(0.0, 1.0, 1.0 - abs(norm_velocity)) * 255.0)
        b = int(abs(clamp(- 1.0, 0.0, - 1.0 - norm_velocity)) * 255.0)
        world.debug.draw_point(
            radar_data.transform.location + fw_vec,
            size=0.075,
            life_time=0.06,
            persistent_lines=False,
            color=carla.Color(r, g, b))

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
        carla.Transform(carla.Location(x=0, y=-0.9, z=2.4), carla.Rotation(yaw=-130)),  # [0] Left side camera  
        carla.Transform(carla.Location(x=0, y=0.9, z=2.4), carla.Rotation(yaw=130)),    # [1] Right side camera
        carla.Transform(carla.Location(x=1.5, z=2.4)),                                      # [2] Front camera
        carla.Transform(carla.Location(x=-1.5, z=2.4), carla.Rotation(yaw=180))
    ]
    cameras = []
    radars = []

    for i in range(4):
        if i != 3: #solo uno alla volta
            continue
        camera = spawn_camera(attach_to=vehicle, transform=transforms[i], frequency=1, width=300, height=300)
        camera.listen(lambda image, idx=i: image.save_to_disk(f'output_radar/{idx}/{image.frame}.png'))
        cameras.append(camera)
        radar = spawn_radar(attach_to=vehicle, transform=transforms[i], horizontal_fov=60, vertical_fov=40)
        radar.listen(lambda data: radar_callback(data))
        radars.append(radar)

    vehicle.set_autopilot(True, 8000)

    while(True):
        world.tick()

finally:
    vehicle.destroy()
    for camera in cameras:
        camera.destroy()
    for radar in radars:
        radar.destroy()
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.fixed_delta_seconds = None
    world.apply_settings(settings)