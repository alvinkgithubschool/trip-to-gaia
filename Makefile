CXX ?= clang++
CXXFLAGS = -std=c++11 -Wall -Wextra
ifeq ($(shell uname),Darwin)
LDLIBS = -framework OpenGL -framework GLUT
else
LDLIBS = -lGL -lglut
endif
gaia: main.cpp
	$(CXX) $(CXXFLAGS) main.cpp -o gaia $(LDLIBS)
clean:
	rm -f gaia
.PHONY: clean
