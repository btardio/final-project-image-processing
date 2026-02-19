from PIL import Image
import numpy as np
import sys
import io

    
def read_rgba_from_stdin():

	
	total_bytes_read = 0
	
	source = sys.stdin.buffer
	bytesout = bytearray(b'')
	while True:

		chunk = source.read(4096)
		if not chunk:
			break
        # Append the chunk to the bytearray
		bytesout.extend(chunk)
        
	
	#for data_chunk in read_stdin_chunks():

	#	pass
		#bytesout.append(data_chunk)
		#for chunkchar in data_chunk:
			#bytesout.extend(bytes([chunkchar]))
			#bytewrite = int(chunkchar)
			#if bytewrite > 255:
			#	bytewrite = 254
			#if bytewrite < 1:
			#	bytewrite = 1
			#bytesout.extend(bytes([bytewrite]))

	width_bytes = bytesout[0:4]
	height_bytes = bytesout[4:8]
	bytesout = bytesout[8:]

	integer_value_width = int.from_bytes(width_bytes, byteorder='big', signed=False)
	
	integer_value_height = int.from_bytes(height_bytes, byteorder='big', signed=False)

	width = integer_value_width
	height = integer_value_height
	
	img = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
	
	chunk_size = 4

	pixels = []

	for i in range(0, len(bytesout), chunk_size):
		try:
			chunk = bytesout[i:i + chunk_size]
			#print(f"Processing chunk: {chunk}")
			
			r = int(chunk[0])
			g = int(chunk[1])
			b = int(chunk[2])
			a = int(chunk[3])
		
		
			pixels.append((r,g,b,a))
		except Exception as e:
			print("some sizing error")
		
	for x in range(width):
		for y in range(height):
			
			index = (width * y) + x
			
			img.putpixel((x,y), pixels[index])
	
	img.save("output_image.png")

	print(bytesout)

if __name__ == "__main__":
	read_rgba_from_stdin()
