gt: gtest.o mainMockMock.o
	g++ -o $@ $? -lgtest_main -lgtest -lgmock

%.o:%.cpp
	g++ -Wall -pedantic -I../.. -c $<

clean:
	rm -f gt *.o

purge: clean
	rm -f *~
