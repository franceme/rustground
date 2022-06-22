exe=/usr/bin/python3
pkg=package_name

MAKEFLAGS += --silent
start=${pkg}/main.py

default::compile

ex:
	@echo Executing the program
	@chmod 777 -R ${pkg}
	@./${start}

install:
	@echo Installing the dependencies
	@${exe} -m pip install --user --upgrade setuptools wheel
freeze:
	@echo Freezing the code
	@pyinstaller --onefile ${start}
dist:
	@echo Creating the Distribution
	@chmod 777 -R setup.py
	@${exe} setup.py sdist bdist_wheel

clean:
	@echo Clean
	@-rm -r dist/
	@-rm -r build/
	@-rm -r *.egg-info/
	@-rm *.spec
