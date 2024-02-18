
CC = cc
CPPFLAGS = -O2
RM = rm -f

all: a.out b.out c.out f.out

a.out: main.c
	$(CC) $(CPPFLAGS) $^ -o $@

b.out: timing.c
	$(CC) $(CPPFLAGS) $^ -o $@

c.out: sends.c
	$(CC) $(CPPFLAGS) $^ -o $@

f.out: confirm_ac97.c
	$(CC) $(CPPFLAGS) $^ -o $@

clean:
	$(RM) a.out b.out c.out f.out
