#!/usr/bin/python3
import os,sys

try:
	from src.information import REQ
	import src.PACKAGE_NAME as entry
except:
	pass
try:
	from information import REQ
	import PACKAGE_NAME as entry
except:
	pass


hollow_run = lambda: entry.hollow_main()

if __name__ == '__main__':
	map(lambda x: os.system(f"{sys.executable} -m pip install {x}"), REQ)
	hollow_run()
