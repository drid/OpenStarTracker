# ####################################### #
# Camera test for night sky image capture #
# ####################################### #


import picamera
from fractions import Fraction

camera = picamera.PiCamera()

camera.opacity = 255
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 1600
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'night'
camera.awb_mode = 'off'
camera.image_effect = 'none'
camera.meter_mode = 'average'
camera.color_effects = (128,128)
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)
#camera.resolution = (1024, 768)
camera.framerate = Fraction(1, 6)
camera.shutter_speed = 6000000  # 6 sec 

camera.capture('im4.jpg')


