exe: gt
	./gt

CXX = /usr/bin/g++
RM = /usr/bin/rm

VPATH = .:../..

gt: $(GTEST_FILE) mainMockMock.o
	$(CXX) -o $@ $? -lgtest_main -lgtest -lgmock

%.o:%.cpp
	$(CXX) -Wall -pedantic -I../.. -I../../TestData -c $<

clean:
	$(RM) -f gt *.o

purge: clean
	$(RM) -f *~
