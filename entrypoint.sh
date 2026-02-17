#!/bin/bash
cat /untitled.png | python3 /image_to_rgba.py | /TutorialClient > /dev/null

# for i in {1..100}; /TutorialClient > /dev/null; done

cat /out_transformed_image.rgba
