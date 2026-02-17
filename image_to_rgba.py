from PIL import Image
import numpy as np
import sys
import io


def read_image_from_stdin():
	# Read all binary data from stdin
	# In Python 3, use sys.stdin.buffer to read binary data
	img_bytes = sys.stdin.buffer.read()

	if not img_bytes:
		print("Error: No image data received from stdin.")
		sys.exit(1)

	try:
        
		image_stream = io.BytesIO(img_bytes)
        
		img = Image.open(image_stream)
        
		#print(f"Image format: {img.format}")
		#print(f"Image size: {img.size}")
        
		byte_representation_width = img.size[0].to_bytes(4, byteorder='big', signed=False)
		byte_representation_height = img.size[1].to_bytes(4, byteorder='big', signed=False)

		sys.stdout.buffer.write(byte_representation_width)
		sys.stdout.buffer.write(byte_representation_height)
        
		imgrgba = img.convert('RGBA')
		
		image_bytes = imgrgba.tobytes()
		sys.stdout.buffer.write(image_bytes)
		
		return None
		
		x = np.array(imgrgba)
		r, g, b, a = np.rollaxis(x, axis = -1)
		#r[a == 0] = 255
		#g[a == 0] = 255
		#b[a == 0] = 255
		rgbaarray = np.dstack([r, g, b, a])
		
		charbuff = []
		
		for item in rgbaarray:
			#print(item)
			#print('aaa')
			#print("!!!")
			for (r, g, b, a) in item:
				#for  in imagerow:
				#print(hex(r))
				
				charbuff.append(chr(r))
				charbuff.append(chr(g))
				charbuff.append(chr(b))
				charbuff.append(chr(a))
				sys.stdout.write(chr(r))
				sys.stdout.write(chr(g))
				sys.stdout.write(chr(b))
				sys.stdout.write(chr(a))
				
				#sys.stdout.buffer.write(chr(r))
				
				#print(r)
				#print(g)
				#print(b)
				#print(a)
				#break
			
			
			
			#print('aaa')
			
			
			#for (r, g, b, a) in item:
				#for  in imagerow:
				#print(hex(r))
				#charbuff.append(chr(r))
				#charbuff.append(chr(g))
				#charbuff.append(chr(b))
				#charbuff.append(chr(a))
				#sys.stdout.write(chr(r))
				#sys.stdout.write(chr(g))
				#sys.stdout.write(chr(b))
				#sys.stdout.write(chr(a))
				
				#sys.stdout.buffer.write(chr(r))
				
				#print(r)
				#print(g)
				#print(b)
				#print(a)
				#break
			#break

			#print(repr(rgbaarray[0].tobytes()))
			#sys.stdout.buffer.write(rgbaarray[0].tobytes())
			#print(item[0], item[1], i)
			#print(r.bytes()) #, g, b, a
		#print(chr(0), end="")
		#print(chr(0), end="")
		#print(chr(0), end="")
		#print(chr(0), end="")
		#print(chr(0), end="")
		#img = Image.fromarray(x, 'RGBA')
        

	except Exception as e:
		print(f"Error opening image: {e}")
		sys.exit(1)



if __name__ == "__main__":
    read_image_from_stdin()
