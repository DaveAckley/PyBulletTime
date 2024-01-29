all:	build run

build:	FORCE
	./scripts/makeTestRobot.pl > genRobot.urdf

run:	FORCE
	python3 ./src/WorldRunner.py notes/sm1.toml

.PHONY:	FORCE
