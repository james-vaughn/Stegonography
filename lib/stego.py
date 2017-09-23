from enum import Enum

SIZE_OF_BYTE = 8

JPEG_ENCODING_START_POS = 10000

# File formats which can be accepted by the stego writer
class FileFormat(Enum):
	JPEG = 1


class StegoWriter:

	def __init__(self, imgFile, fileFormat, message=""):
		assert(isinstance(fileFormat, FileFormat))

		self.imgFile = imgFile
		self.fileFormat = fileFormat
		self.message = message
		self.stegoImgBytes = None

	# returns the bytes of an input image
	def _getImgBytes(self):
		with open(self.imgFile, "rb") as imageFile:
			f = imageFile.read()
			bytes = bytearray(f)

		return bytes	


	def write(self, outputFilename):
		if self.stegoImgBytes is None:
			self.prepare()

		with open(outputFilename, "wb") as outputFile:
			outputFile.write(bytearray(self.stegoImgBytes))


	# creates the output image bytes so that we can write the image later
	def prepare(self):
		if self.fileFormat == FileFormat.JPEG:
			self._prepareJPEG()


	def _prepareJPEG(self):
		imgBytes = self._getImgBytes()

		# encode into ascii byte string
		messageBytes = self.message.encode("ASCII") 

		if len(imgBytes) - JPEG_ENCODING_START_POS < len(messageBytes) * SIZE_OF_BYTE:
			raise Exception("Image is not large enough to encode the message.")

		stegoImg = imgBytes[0:JPEG_ENCODING_START_POS]
		imgBytes = imgBytes[JPEG_ENCODING_START_POS:]

		for byte in messageBytes:
			for bit in StegoWriter.byteToBitArray(byte):
				# set the last bit of the image byte to the bit to encode
				oldByte = imgBytes.pop(0)
				stegoByte = (oldByte & 0xFE) | bit
				stegoImg.append(stegoByte)
				
				# print("Old byte: {}\tNew Byte: {}\tEncoded bit: {}".format(oldByte, stegoByte, bit))

		# Fill in the rest of the image bytes that don't have a message
		stegoImg += imgBytes[:]

		self.stegoImgBytes = stegoImg


	# Converts a given byte into its equivalent bit array
	@staticmethod
	def byteToBitArray(byte):
		bitArray = []
		for bitPos in range(SIZE_OF_BYTE)[::-1]:
			bitArray.append((byte >> bitPos) & 0x01)

		return bitArray


