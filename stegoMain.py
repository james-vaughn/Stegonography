from lib.stego import StegoEncoder


stegoWriter = StegoEncoder(imgFile = "InputImages/fate_png.png")

# Can prepare the output ahead of time
stegoWriter.encode(message = "hello, world")

stegoWriter.write("OutputImages/fate_png_out.png")

stegoReader = StegoEncoder(imgFile = "OutputImages/fate_png_out.png")
print(stegoReader.decode())