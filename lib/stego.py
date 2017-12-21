from PIL import Image

SIZE_OF_BYTE = 8


class StegoEncoder:

	def __init__(self, imgFile):
		self.imgFile = imgFile
		self.stegoImage = None


	# Save the new stego image to disk at the given filename
	def write(self, outputFilename):
		if self.stegoImage is None:
			self.encode()

		self.stegoImage.save(outputFilename)


	# creates the output image bytes so that we can write the image later
	def encode(self, message = ""):
		self.stegoImage = Image.open(self.imgFile)
		pixels = self.stegoImage.load()

		# encode into ascii byte string
		messageBytes = bytes(message + "\0", "ASCII")

		# if len(imgBytes) * len(imgBytes[0]) < len(messageBytes) * SIZE_OF_BYTE:
		# 	raise Exception("Image is not large enough to encode the message.")

		pixel_x, pixel_y = 0, 0

		for byte in messageBytes:
			for bit in StegoEncoder.byteToBitArray(byte):
				# set the last bit of the image byte to the bit to encode
				oldPixel = pixels[pixel_x, pixel_y]
				pixels[pixel_x, pixel_y] = ((oldPixel[0] & 0xFE) | bit, oldPixel[1], oldPixel[2])
				
				pixel_x += 1

				if pixel_x >= self.stegoImage.width:
					pixel_x = 0
					pixel_y += 1


	def decode(self):
		message = ""

		img = Image.open(self.imgFile)
		pixels = img.load()

		bits = []

		for y in range(img.height):
			for x in range(img.width):
				pixel = pixels[x, y]

				bits.append(pixel[0] & 0x01)

				if len(bits) == SIZE_OF_BYTE:
					
					byte = StegoEncoder.bitArrayToByte(bits)

					char = chr(byte)
					if char == "\0":
						return message
					else:
						message += char


	# Converts a given byte into its equivalent bit array
	@staticmethod
	def byteToBitArray(byte):
		bitArray = []
		for bitPos in range(SIZE_OF_BYTE)[::-1]:
			bitArray.append((byte >> bitPos) & 0x01)

		return bitArray


	@staticmethod
	def bitArrayToByte(arr):
		"""Returns the byte represented by the bit array.
		Also clears the bit array in the process."""

		byte = 0x00
		for _ in range(SIZE_OF_BYTE):
			byte = (byte << 1) | arr.pop(0)

		return byte