from lib.stego import FileFormat, StegoWriter


stegoWriter = StegoWriter(imgFile = "InputImages/fate.jpeg", fileFormat = FileFormat.JPEG, message = "hello, world")

# Can prepare the output ahead of time
stegoWriter.prepare()

stegoWriter.write("OutputImages/fateOut.jpeg")
