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

More work can be done, including trying another transport. The original idea was to include the OpenCL to do image processing using the 4 chips on
the raspberry, this was not successful. The OpenCL showed CPU loads of nearly 3.0. The next tasks after completing black and white image transfer
would be to do an edge detection.


### Work Completed:

The cpp files modified are buried in the tutorial for Thrift, I have included them below for reference.

Client:

```
/* 
 * ECEA 5307
 * Brandon Tardio
 * https://github.com/btardio/final-project-btardio
 * 
 * This file is a thrift client that runs in docker
 * it is compiled using the following command in docker:
 * 
 * docker build -f ./Dockerfile_client -t thriftclient . && docker container run  -it thriftclient | python3 rgba_to_image.py
 * 
 * If the RPI server is running at address 192.168.1.100 it will produce 
 * \x00 char output.
 * 
 * The container run command uses the python script and the untitled.png
 * 
 * The file is read from stdin.
 */


#include <iostream>
#include <iomanip>
#include <vector>
#include <fstream>

#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TTransportUtils.h>

#include <arpa/inet.h>

#include "../gen-cpp/Calculator.h"

#include "../gen-cpp/rgbatransform.h"

using namespace std;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

using namespace tutorial;
using namespace shared;

std::string filename_create(){
	// 1. Seed the random number generator once per program run
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    // 2. Generate a random number.
    long long randomNum = rand(); // May be small

    // 3. Convert to a string with leading zeros using stringstream
    std::stringstream ss;
    ss << std::setw(10) << std::setfill('0') << randomNum;
    std::string randomStr = ss.str();

    // 4. Ensure the string is exactly length 10 (handle potential overflow if number is > 10 digits)
    if (randomStr.length() > 10) {
        randomStr = randomStr.substr(randomStr.length() - 10);
    }
    return randomStr;
}


std::vector<rgbastruct> readAndPrint4Bytes(std::istream& inputFile) {//const std::string& filename) {

    std::vector<rgbastruct> out;

    // Buffer to hold 4 bytes
    unsigned char buffer[4];
    uint32_t value; // Use uint32_t to ensure a consistent 4-byte size across platforms

    // Read 4 bytes at a time until the end of the file
    while (inputFile.read(reinterpret_cast<char*>(buffer), sizeof(buffer))) {
        // Use static_cast<unsigned int>(static_cast<unsigned char>()) for each byte
        // and combine using bitwise shifts. This approach explicitly handles endianness if you define an order.
        // The following combines bytes in little-endian order (LSB first), common on x86 platforms.
        
        value = static_cast<uint32_t>(static_cast<unsigned int>(buffer[0])) |
                static_cast<uint32_t>(static_cast<unsigned int>(buffer[1])) << 8 |
                static_cast<uint32_t>(static_cast<unsigned int>(buffer[2])) << 16 |
                static_cast<uint32_t>(static_cast<unsigned int>(buffer[3])) << 24;

        // Print the value to the terminal (in hexadecimal for clarity)
        std::cout << "Read value (hex): 0x" << std::hex << std::setw(8) << std::setfill('0') << value << std::dec << std::endl;
        
		rgbastruct transformed_pixel_rgbastruct;

		transformed_pixel_rgbastruct.r = (char)static_cast<uint32_t>(static_cast<unsigned int>(buffer[0]));
		transformed_pixel_rgbastruct.g = (char)static_cast<uint32_t>(static_cast<unsigned int>(buffer[1]));
		transformed_pixel_rgbastruct.b = (char)static_cast<uint32_t>(static_cast<unsigned int>(buffer[2]));
		transformed_pixel_rgbastruct.a = (char)static_cast<uint32_t>(static_cast<unsigned int>(buffer[3]));
		

		out.push_back(transformed_pixel_rgbastruct);
		
        
    }

    // Check if the loop terminated due to an error other than reaching the end of the file
    if (!inputFile.eof()) {
        std::cerr << "Error reading file!" << std::endl;
    }

    //inputFile.close();
    return out;
}


// Write an 8x8x8x8 RGBA file
void writeRGBA(const std::string& filename, uint32_t width, uint32_t height, const std::vector<rgbastruct>& pixels) {
    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Error opening file for writing!" << std::endl;
        return;
    }
    uint32_t big_endian_value_width = htonl(width);
    uint32_t big_endian_value_height = htonl(height);
    file.write(
        reinterpret_cast<const char*>(&big_endian_value_width), 
        sizeof(width)
        
    ); //

	file.write(
        reinterpret_cast<const char*>(&big_endian_value_height), 
        sizeof(height)
    ); //

	for (std::vector<rgbastruct>::const_iterator it = pixels.begin(); it != pixels.end(); ++it) {
		unsigned char r,g,b,a;
		
		r = static_cast<unsigned char>(it->r);
		g = static_cast<unsigned char>(it->g);
		b = static_cast<unsigned char>(it->b);
		a = static_cast<unsigned char>(it->a);
		
		file.write(
			reinterpret_cast<const char*>(&r), 
			sizeof(r)
		);
		file.write(
			reinterpret_cast<const char*>(&g), 
			sizeof(g)
		);
		file.write(
			reinterpret_cast<const char*>(&b), 
			sizeof(b)
		);
		file.write(
			reinterpret_cast<const char*>(&a), 
			sizeof(a)
		);

	}
    
    
    file.close();
    
}


// Function to read a 32-bit Big Endian integer
uint32_t readBigEndian32() {
    uint8_t bytes[4];
    // Read 4 bytes from stdin
    std::cin.read(reinterpret_cast<char*>(bytes), 4);
    
    // Combine bytes: MSB first (index 0)
    return (static_cast<uint32_t>(bytes[0]) << 24) |
           (static_cast<uint32_t>(bytes[1]) << 16) |
           (static_cast<uint32_t>(bytes[2]) << 8)  |
           (static_cast<uint32_t>(bytes[3]));
}

int main() { // int argc, char* argv[]) {
	int argc;
	char* argv[3];
	
	if (!std::cin) {
		std::cout << "stdin error\n";
		return -1;
	}
		
    uint32_t a_width = readBigEndian32();
    uint32_t a_height = readBigEndian32();
    


    std::cout << "Width: " << a_width << ", Height: " << a_height << std::endl;

    std::shared_ptr<TTransport> socket(new TSocket("192.168.1.100", 9090));
    std::shared_ptr<TTransport> transport(new TBufferedTransport(socket));
    std::shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));

    rgbatransformClient rgbaclient(protocol);

    try {
		transport->open();
		std::vector<long int> my_vector = {1000000000L, 2000000000L, 3000000000L};
		cout << "ping rgba" << '\n';
	
		rgbaclient.ehlo();
    
		std::vector<rgbastruct> outvector;
		
		
		
		int width = 8, height = 8;
		
		

		
		std::vector<rgbastruct> image(width * height); //(width * height, {0xFF, 0x00, 0x00, 0xFF}); // Red opaque pixels


		for (int i = 0; i < width * height; ++i) {
			image[i].r = (char)0xFF;
			image[i].g = (char)0x00;
			image[i].b = (char)0x00;
			image[i].a = (char)0xFF;
		}
		

		std::vector<rgbastruct> a_loadedImage = readAndPrint4Bytes(std::cin);

		
		for (std::vector<rgbastruct>::const_iterator it = a_loadedImage.begin(); it != a_loadedImage.end(); ++it) {
			// Access members, e.g., it->r
			cout << "item: " << std::hex << std::setfill('0') << std::setw(2) << static_cast<unsigned int>(static_cast<unsigned char>(it->r)) << ",";
			cout << "item: " << std::hex << std::setfill('0') << std::setw(2) << static_cast<unsigned int>(static_cast<unsigned char>(it->g)) << ",";
			cout << "item: " << std::hex << std::setfill('0') << std::setw(2) << static_cast<unsigned int>(static_cast<unsigned char>(it->b)) << ",";
			cout << "item: " << std::hex << std::setfill('0') << std::setw(2) << static_cast<unsigned int>(static_cast<unsigned char>(it->a)) << std::endl;
		}

		
		cout << a_width << "a_width\n";
		cout << a_height << "a_heigth\n";

		rgbaclient.doMosulA(outvector, a_loadedImage, a_width, a_height);
		
		for (std::vector<rgbastruct>::const_iterator it = outvector.begin(); it != outvector.end(); ++it) {
			// Access members, e.g., it->r
			cout << "item: " << std::hex << std::setfill('0') << std::setw(2) << static_cast<unsigned int>(static_cast<unsigned char>(it->r)) << ",";
			cout << "item: " << std::hex << std::setfill('0') << std::setw(2) << static_cast<unsigned int>(static_cast<unsigned char>(it->g)) << ",";
			cout << "item: " << std::hex << std::setfill('0') << std::setw(2) << static_cast<unsigned int>(static_cast<unsigned char>(it->b)) << ",";
			cout << "item: " << std::hex << std::setfill('0') << std::setw(2) << static_cast<unsigned int>(static_cast<unsigned char>(it->a)) << std::endl;
		}
		
		
		writeRGBA("/out_transformed_image.rgba", a_width, a_height, outvector);
		

		try {
		  cout << "Whoa? We can divide by zero!" << '\n';
		} catch (InvalidOperation& io) {
		  cout << "InvalidOperation: " << io.why << '\n';

		}

		transport->close();
    } catch (TException& tx) {
      cout << "ERROR: " << tx.what() << '\n';
    }
}

```

Server:

```

/* 
 * ECEA 5307
 * Brandon Tardio
 * https://github.com/btardio/final-project-btardio
 * 
 * This file is a thrift server that runs on the RPI
 * it is compiled using the following command in docker:
 * 
 * git pull && git submodule foreach 'git pull' && sudo docker build -t btardio/ecea5307btardio:latest . && sudo docker push btardio/ecea5307btardio:latest
 * 
 * This command is on AWS EC-2 Arm architecture machine.
 * 
 * This produces a dockerhub image that the RPI pulls and runs.
 * 
 * docker container stop server || true && docker system prune -a -f && docker container run -it --network host --name server --privileged -v /sys/:/sys/ btardio/ecea5307btardio
 * 
 * This demonstrates STL and thrift.
 */


#include <CL/cl.h>
#define VECTOR_SIZE 1024

#include <thrift/concurrency/ThreadManager.h>
#include <thrift/concurrency/ThreadFactory.h>
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/server/TThreadPoolServer.h>
#include <thrift/server/TThreadedServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TTransportUtils.h>
#include <thrift/TToString.h>

#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <sstream>

#include "../gen-cpp/rgbatransform.h"

using namespace std;
using namespace apache::thrift;
using namespace apache::thrift::concurrency;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;
using namespace apache::thrift::server;

using namespace tutorial;
using namespace shared;

class RgbaHandler : public rgbatransformIf {
public:
  RgbaHandler();
  
  void ehlo() override { cout << "pong()" << '\n'; }
    
  void doMosul(std::vector<long int>&, const std::vector<long int>&) override;
  
  void doMosulA(std::vector<rgbastruct>&, const std::vector<rgbastruct>&, const int width, const int height) override;
  
};

RgbaHandler::RgbaHandler() {

}


void RgbaHandler::doMosulA(std::vector<rgbastruct>& transformedImage, const std::vector<rgbastruct>& loadedImage, const int width, const int height) {

	for (size_t i = 0; i < loadedImage.size(); ++i) {
		
		rgbastruct transformed_pixel_rgbastruct;
		
		float luminance = 0.299f * (float)loadedImage[i].r + 0.587f * (float)loadedImage[i].g + 0.114f * (float)loadedImage[i].b;        
		transformed_pixel_rgbastruct.r = (unsigned char)(luminance * 255.0f); //loadedImage[i].r;
		transformed_pixel_rgbastruct.g = (unsigned char)(luminance * 255.0f); //loadedImage[i].g;
		transformed_pixel_rgbastruct.b = (unsigned char)(luminance * 255.0f); //loadedImage[i].b;
		transformed_pixel_rgbastruct.a = 0xFF;
		transformedImage.push_back(transformed_pixel_rgbastruct);
	}
}

void RgbaHandler::doMosul(std::vector<long int>& a, const std::vector<long int>& b) {
	
	
}



int main() {

  // This server only allows one connection at a time, but spawns no threads
  TSimpleServer server(
    std::make_shared<rgbatransformProcessor>(std::make_shared<RgbaHandler>()),
    std::make_shared<TServerSocket>(9090),
    std::make_shared<TBufferedTransportFactory>(),
    std::make_shared<TBinaryProtocolFactory>());


  cout << "Starting the server..." << '\n';
  server.serve();
  cout << "Done." << '\n';
  return 0;
}


```


