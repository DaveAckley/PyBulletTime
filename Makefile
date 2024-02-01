TOML_FILE:=notes/sm2.toml

all:	build run

build:	FORCE
	./scripts/makeTestRobot.pl > genRobot.urdf

run:	FORCE
	python3 ./src/WorldRunner.py $(TOML_FILE)

.PHONY:	FORCE
