OBJECTS = main.o \
			 testIP.o testPS.o testRP.o testS.o testVI.o \
			 test.PointerII.o test.PointerTypedef.o \
			 test.PointerV.o test.PointerVI.o test.PointerVV.o

OBJ_ELF = $(foreach obj,$(OBJECTS),$(subst .o,.c.obj,$(obj)))
EXEC = test
EXEC_ELF = $(EXEC).elf

CFLAGS = -c -Wall -pedantic

ALL: $(EXEC) $(EXEC_ELF)

tt:
	echo $(OBJ_ELF)

%.o:%.c
	gcc $(CFLAGS) -o $@ -ggdb3 $<

$(EXEC_ELF):$(OBJ_ELF)
	gcc -o $(EXEC_ELF) $(OBJ_ELF)

%.c.obj:%.c
	gcc $(CFLAGS) -o $@ -ggdb3 $<

$(EXEC):$(OBJECTS)
	gcc -o $(EXEC) $(OBJECTS)

clean:
	rm -f $(EXEC) $(EXEC_ELF) *.o *.obj *~
