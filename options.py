import platform
OS = platform.system()

print("Running on '%s' platform." % OS)

if OS.lower() == 'windows':
	# debug configuration (dev)
	DEBUG = True
	RUN_LOCALLY = True
	JAVA_PATH = "java"

elif OS.lower() == 'linux':
	# deploy configuration (test & production)
	DEBUG = False
	RUN_LOCALLY = False
	JAVA_PATH = "/opt/jdk-14/bin/java"

else:
	# raise RuntimeError("Unknown platform: %s, check your 'options.py'." % OS)
	DEBUG = False
	RUN_LOCALLY = True
	JAVA_PATH = "java"

