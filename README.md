# rcv
raspberry pi computer vision

## install on rasberry PI device

As user pi

```
    cd /home/pi
    git clone https://github.com/nes56/rcv.git
    cd rcv
    ./install.sh
```

## runing the service

```
    sudo systemctl start rcv.service
```

## checking health of service

```
    sudo systemctl status rcv.service
```
logs of rcv service are located under /opt/logs


## how to test distance logic

first cd to rcv subdirectory
Than run the below command.

Please note to use the right path seperator when running these cmmands on Linux 

```
python measure_distance_on_mouse_click.py --image=images_height_38.5_y_angle_28\img_1_320x240_2019_02_07_20_53_24.png --camera-height=38.5 --y_leaning_angle=28 --x_turning_angle=1.9
```
## how to test line detection
```
python find_line.py --image="images_height_43.3\img2_d200_c-20_d134.jpg" --show=True
```

##how to test combine modules

on image
```
python rcv\combine_modules.py --image=rcv\images_height_23.3\img5_d150_c0_d0.jpg --show=True
```

on video
```
python rcv\combine_modules.py --video=rcv\practice_videos\video_2_320_240.avi
```
