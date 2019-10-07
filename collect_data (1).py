import glob
import os
import sys
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


####################################################################


import random
import time
import numpy as np
import cv2

starttime=time.time()

actor_list = []
try:
	client = carla.Client('localhost', 2000)
	client.set_timeout(10.0) # seconds
	world = client.get_world()
	blueprint_library = world.get_blueprint_library()

	vehicle_bp = random.choice(blueprint_library.filter('vehicle.bmw.*'))
	print(vehicle_bp)


	spawn_point = random.choice(world.get_map().get_spawn_points())



	vehicle = world.spawn_actor(vehicle_bp, spawn_point)
	vehicle.set_autopilot(True)


	#vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    # vehicle.set_autopilot(True)  # if you just wanted some NPCs to drive.
	actor_list.append(vehicle)


	camera_bp = blueprint_library.find('sensor.camera.rgb')
	#camera_bp.set_attribute('image_size_x', 640)
	#camera_bp.set_attribute('image_size_y', 480)
	camera_bp.set_attribute('fov', '110')
	camera_bp.set_attribute('sensor_tick', '1.0')
	transform = carla.Transform(carla.Location(x=0.8, z=1.7))
	#spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))

	camera = world.spawn_actor(camera_bp, transform, attach_to=vehicle)

	camera.listen(lambda image: image.save_to_disk('output/%06d.png' % image.timestamp))
	#sensor.listen(lambda data: do_something(data))
	#camera.listen(lambda image: image.save_to_disk('output/%06d.png' % image.raw_data))

	#self.vehicle.get_control(carla.VehicleControl())
	#Values = vehicle.get_control(carla.VehicleControl(vehicle))
	#vehicle.get_control()
	#values=__init__.carla.VehicleControl()
	#steering_Angle = vehicle.carla.VehicleControl()
	#print(steering_Angle)
	#print(Values)
	timer = 0
	actor_list.append(camera)
	while True:
		values=vehicle.get_control()
		print(values.steer)
		time.sleep(1)
		timer = timer + 1 
		if timer == 120:
			break


#time.sleep(20)
	


finally:

	print('destroying actors!')
	for actor in actor_list:
		actor.destroy()
	print('done.')