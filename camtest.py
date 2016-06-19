# ####################################### #
# Camera test for night sky image capture #
# ####################################### #


import picamera
from fractions import Fraction

camera = picamera.PiCamera()

camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
#camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'off'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
#camera.image_effect = 'none'
#camera.color_effects = None
#camera.rotation = 0
#camera.hflip = False
#camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)
camera.resolution = (1024, 768)
camera.ISO = 800
camera.framerate = Fraction(1, 6)
camera.shutter_speed = 6000000  # 6 sec 

camera.capture('im1.jpg')


