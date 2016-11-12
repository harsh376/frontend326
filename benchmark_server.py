# File designed to replicate the server being run at maximum capacity at a steady state
# Long enough to capture our readings

import os

for i in range(10):
	print os.system("ab -k -n 1350 -c 1350 http://52.5.94.6:8080/?keywords=hello+hi")

