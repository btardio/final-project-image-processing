### Image Processing

Image processing was completed for ECEA 5307. The results show success building deploying and transforming an image to black and white for a small size png image.

To reproduce the solution:

```

# First clone this repository

# On arch/arm64 build the server and push to dockerhub, you will need to replace dockerhub with your own after setting up a repository.

sudo docker build -t btardio/ecea5307btardio:latest . && sudo docker push btardio/ecea5307btardio:latest

# This step creates a docker image that will be used on the raspberry.

# After success go to the raspberry pi machine or include the init.d scripts to automate this step.

# Start the server:

docker container stop server || true && docker system prune -a -f && docker container run -it -d --network host --name server --privileged -v /sys/:/sys/ btardio/ecea5307btardio

# Finally from a client machine run the image.

# Using a machine with docker installed:

docker build -f ./Dockerfile_client -t thriftclient . && docker container run -it thriftc lient | python3 rgba_to_image.py

# The python script copies an untitled.png file and the result is stored in output_image.png

```


### Sample images:

Sample images can be found in the processed_images directory.


### Results

I am uncertain as to why the algorithm did not perform successfully for larger images. I rule out the blame being the chip and it is probably 
a programming error that I introduced but did solve. My rationale is that if the chip is faulty it wouldn't start up and run at all. 





#### TODO

this is a hello-world example that drove cpu usage:

cat /proc/loadavg
2.93 2.21 1.31 3/146 17214

work in progress
