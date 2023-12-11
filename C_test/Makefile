.DEFAULT_GOAL := hello


.PHONY: test
test: 
	echo "Test target in Makefile"


hello: hello.o main.o
	gcc hello.o main.o -o hello

hello.o: hello.c
	gcc -c hello.c

main.o: main.c 
	gcc -c main.c

.PHONY: clean
clean:
	rm -rf *.o hello

