OBJECTS = testdata.o main.o test.Pointer.o
EXEC = test

%.o:%.c
	gcc -c -ggdb3 $<

$(EXEC):$(OBJECTS)
	gcc -o $(EXEC) $(OBJECTS)
