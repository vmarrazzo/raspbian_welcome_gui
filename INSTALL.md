# Installation on Raspberry Pi

Edit with "pi" user right the file 

```
/home/pi/.config/lxsession/LXDE-pi/autostart
```

adding the follow scripting line

```bash
@/usr/bin/python <location_to_script>/raspbian_wellcome_gui.py
```

and reboot
