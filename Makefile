
CC = cc
CPPFLAGS = -O2
RM = rm -f

all: main.c
	$(CC) $(CPPFLAGS) $^

clean:
	$(RM) a.out
