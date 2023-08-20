CPPOBJ = depMock.o gtest.o

ALL: gt

gt: m

gt: $(CPPOBJ)
	g++ -o gt foo.o $(CPPOBJ) -lgtest_main -lgtest -lgmock

%.o:%.cpp
	g++ -c $<

m: foo.o
	gcc -o m foo.o main.c dep.c 

foo.o:foo.c
	gcc -c foo.c

clean:
	rm -f gt m *.o
