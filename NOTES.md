
Note: this is using

https://portablecl.org/publications.html

There is no GPU

Modifications to the code provided in 


OpenCL Programming by Example
By : Banger, Koushik Bhattacharyya

added CL_MEM_ALLOC_HOST_PTR to the clCreateBuffer

change GPU to CL_DEVICE_TYPE_CPU





arm64 machine on aws:

sudo docker build -t btardio/ecea5307btardio:latest . && sudo docker push btardio/ecea5307btardio:latest


RPI5:

docker system prune -a -f && docker container run -it --privileged -v /sys/:/sys/ btardio/ecea5307btardio
