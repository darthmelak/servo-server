# Home-made 2 servo 2DOF pan-tilt web controller

Goal: RPi IR-CUT camera webview with IR filter and IR led toggle buttons + 2DOF pan-tilt servo control via arrow buttons

- Server inspired by https://github.com/waveshare/Pan-Tilt-HAT
- Servo control through GPIO via [pigpio](https://abyz.me.uk/rpi/pigpio/)
- IR filter toggle on Pi3 via https://github.com/6by9/rpi3-gpiovirtbuf
- Camera mjpeg via running uv4l_raspicam server on same Pi [https://www.linux-projects.org/uv4l/installation/]

## Setup:

Follow pigpio installation;
Follow uv4l installation;
```
sudo apt-get install uv4l uv4l-raspicam uv4l-raspicam-extras uv4l-server uv4l-mjpegstream
```
Edit /etc/uv4l/uv4l-raspicam.conf:  
width = 1280  
height = 720  

```
pip3 install bottle adafruit-circuitpython-servokit
```

Edit scripts/servor-server.service with working dir/path/user
```
sudo cp scripts/servo-server.service /etc/systemd/system/
sudo systemctl daemon-reload
```

### If running on pi3:
build rpi3-gpiovirtbuf  
```
cd ~
git clone https://github.com/6by9/rpi3-gpiovirtbuf.git
cd rpi3-gpiovirtbuf
make
sudo cp rpi3-gpiovirtbuf /usr/local/bin
```
also
```
sudo cp scripts/nvstart /usr/local/bin
sudo cp scripts/nvstop /usr/local/bin
```
