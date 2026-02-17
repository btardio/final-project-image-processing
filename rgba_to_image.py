from PIL import Image
import numpy as np
import sys
import io



def read_stdin_chunks(chunk_size=1024):
    """Reads stdin in chunks and yields bytes objects."""
    while True:
        # Read a chunk of data (at most chunk_size bytes)
        chunk = sys.stdin.buffer.read(chunk_size)
        if not chunk:
            # End of file (EOF) reached
            break
        yield chunk
        
def read_rgba_from_stdin():
	# Read all binary data from stdin
	# In Python 3, use sys.stdin.buffer to read binary data
	#img_bytes = sys.stdin.buffer.read()

	#if not img_bytes:
	#	print("Error: No image data received from stdin.")
	#	sys.exit(1)
	bytesout = bytearray(b'')
	total_bytes_read = 0
	for data_chunk in read_stdin_chunks():
		# Process each data_chunk (which is a bytes object)
		#total_bytes_read += len(data_chunk)
		#print(data_chunk)
		for chunkchar in data_chunk:
			#print(">")
			#print(bytes([chunkchar]))
			bytesout.extend(bytes([chunkchar]))
	#print(f"Total bytes read: {total_bytes_read}")

	width_bytes = bytesout[0:4]
	height_bytes = bytesout[4:8]
	bytesout = bytesout[8:]

	integer_value_width = int.from_bytes(width_bytes, byteorder='big', signed=False)
	
	integer_value_height = int.from_bytes(height_bytes, byteorder='big', signed=False)

	#print( integer_value_height )
	#print( integer_value_width )
	
	#return None
	#print(img_bytes)
#	try:
#		print ("~")
#		for byte in img_bytes:
#			print ("~")
#			print(repr(byte))
        
	#except Exception as e:
	#	pass
	
	width = integer_value_width
	height = integer_value_height
	
	img = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
	
	chunk_size = 4

	pixels = []

	for i in range(0, len(bytesout), chunk_size):
		chunk = bytesout[i:i + chunk_size]
		print(f"Processing chunk: {chunk}")
		
		r = chunk[0]
		g = chunk[1]
		b = chunk[2]
		a = chunk[3]
		
		
		pixels.append((r,g,b,a))
		
	for x in range(width):
		for y in range(height):
			
			index = (width * x) + y
			#print(index)
			img.putpixel((x,y), pixels[index])
	
	img.save("output_image.png")

	print(bytesout)

if __name__ == "__main__":
	read_rgba_from_stdin()
