# turtlebot

This repo provides simple code for running experiments on a Turtlebot3 Burger (with Raspberry Pi 3 running ROS 2 Humble on an Ubuntu 22.04 image).

## Control Turtlebot Using Keyboard
1. Bring up the turtlebot.
```
ros2 launch turtlebot3_bringup robot.launch.py
```
2. Run the teleop node.
```
source ~/ros2_ws/install/setup.bash
ros2 run turtlebot teleop
``` 

## Setting Up a New Turtlebot
### Resources
* https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/#sbc-setup
* https://www.raspberrypi.com/software/
* https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html

### Downloading the OS (on an Ubuntu machine)
1. Download the Raspberry Pi imager: https://www.raspberrypi.com/software/ 
2. Run the imaging software
```
cd ~/Downloads
chmod +x imager_2.0.7_amd64.AppImage
sudo ./imager_2.0.7_amd64.AppImage
```
3. Select your RPi model under “Device”
4. Select “Other general-purpose OS” → “Ubuntu” → “Ubuntu Server 22.04 LTS (64-bit)” under “OS” 
5. Select the RPi’s SD card under “Storage”
6. Customize as desired, but make sure the enable SSH under “Remote access”
7. Write the image. 

### Setting Up Remote SSH
1. Insert the flashed SD card into the Pi.
2. Connect a monitor and keyboard BEFORE connecting the RPi to power.
3. After logging in, check the wlan0 MAC address using the command `ip a`.
4. Go to networks.utexas.edu and register the Pi’s MAC address under “Wireless”. 
5. Add the new network SSID and password to the RPi’s netplan.
```
sudo nano /etc/netplan/50-cloud-init.yaml
```
7. Reboot.
8. Connect your laptop to `utexas` or `utexas-iot` Wi-Fi. Then SSH into the turtlebot.
```
ssh MACADDRESS.dynamic.utexas.edu
```

### Configure RPi Settings
1. Change the auto upgrade settings from `1` to `0`.
```
sudo nano /etc/apt/apt.conf.d/20auto-upgrades
```
2. Don't wait for network on boot and disable auto sleep.
```
systemctl mask systemd-networkd-wait-online.service
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
sudo reboot now
```
3. Update the OS before continuing.
```
sudo apt update
sudo apt upgrade
```

### Install ROS 2 Humble Base
1. Follow these instructions, but install the `base` ros package, not `desktop`. https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html 
2. Test the ROS 2 installation
```
echo source /opt/ros/humble/setup.bash >> ~/.bashrc
source ~/.bashrc
ros2 topic list
```

### Install Turtlebot Dependencies
```
sudo apt install python3-argcomplete python3-colcon-common-extensions libboost-system-dev build-essential
sudo apt install ros-humble-hls-lfcd-lds-driver
sudo apt install ros-humble-dynamixel-sdk ros-humble-xacro libudev-dev
sudo apt install ros-humble-turtlebot3-bringup ros-humble-teleop-twist-keyboard ros-humble-turtlebot3-msgs
```

## Configure USB Settings for OpenCR
```
sudo cp `ros2 pkg prefix turtlebot3_bringup`/share/turtlebot3_bringup/script/99-turtlebot3-cdc.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Final System Configuration
1. Set up the OpenCR board
```
sudo dpkg --add-architecture armhf  
sudo apt-get update  
sudo apt-get install libc6:armhf
```
2. Set environment variables for convenience.
```
echo export LDS_MODEL=LDS-01 >> ~/.bashrc
echo export OPENCR_PORT=/dev/ttyACM0 >> ~/.bashrc  
echo export OPENCR_MODEL=burger >> ~/.bashrc
echo export TURTLEBOT3_MODEL=burger >> ~/.bashrc
source ~/.bashrc
```
3. Remove old update and download new. Install.
```
rm -rf ./opencr_update.tar.bz2
wget https://github.com/ROBOTIS-GIT/OpenCR-Binaries/raw/master/turtlebot3/ROS2/latest/opencr_update.tar.bz2   
tar -xvf opencr_update.tar.bz2
cd ./opencr_update  
./update.sh $OPENCR_PORT $OPENCR_MODEL.opencr
```

Run Teleop
ros2 launch turtlebot3_bringup robot.launch.py
