#!/bin/bash
cat /untitled.png | python3 /image_to_rgba.py | /TutorialClient > /dev/null

cat /out_transformed_image.rgba
