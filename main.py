# Libraries
import time
import sys

# Classes
from app import App

# Class Main
class Main:

	# Constructor
	def __init__(self):
		self.run = True

		self.app = App()

		self.loop()

	# Loop
	def loop(self):
		
		while self.run:
			
			self.app.update()

			time.sleep(1)


# Start app
if __name__ == "__main__":
	main = Main()
	sys.exit()
