UNAME:=$(shell uname -s)
OSXFUSE:=
ifeq ($(UNAME),Darwin)
	OSXFUSE=4x
endif

LDLIBS += -lfuse$(OSXFUSE)
CFLAGS += -D_FILE_OFFSET_BITS=64

all: hello

.PHONY: clean

clean:
	rm -f hello *.o
