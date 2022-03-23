## Home-made 2 servo 2DOF pan-tilt web controller

Goal: RPi IR-CUT camera webview with IR filter and IR led toggle buttons + 2DOF pan-tilt servo control via arrow buttons

- Server inspired by https://github.com/waveshare/Pan-Tilt-HAT
- Servo control through GPIO via [pigpio](https://abyz.me.uk/rpi/pigpio/)
- IR filter toggle on Pi3 via https://github.com/6by9/rpi3-gpiovirtbuf
- Camera mjpeg via running uv4l_raspicam server on same Pi
