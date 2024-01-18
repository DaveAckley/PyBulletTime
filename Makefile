all:	build run

build:	FORCE
	./makeTestRobot.pl > genRobot.urdf

run:	FORCE
	python3 ./WorldRunner.py notes/sm1.toml

.PHONY:	FORCE
