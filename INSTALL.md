# Installation on Raspberry Pi

Edit with "pi" user right the file 

```
/home/pi/.config/lxsession/LXDE-pi/autostart
```

adding the follow scripting line

```bash
@/usr/bin/python <location_to_script>/raspbian_wellcome_gui.py
```

and reboot rpi.

### Additional info on installation

After installation no keyboard is mandatory to use this application but the mouse (or a device that emulate it) yes. I am using this application with a gamepad controlled that emulate mouse.
