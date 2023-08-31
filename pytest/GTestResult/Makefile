exe: gt
	./gt

VPATH = .:../..

gt: $(GTEST_FILE) mainMockMock.o
	g++ -o $@ $? -lgtest_main -lgtest -lgmock

%.o:%.cpp
	g++ -Wall -pedantic -I../.. -I../../TestData -c $<

clean:
	rm -f gt *.o

purge: clean
	rm -f *~
