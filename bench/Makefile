CXXFLAGS += -I/usr/local/include/snappy \
			-I/usr/local/include/lzo \
			-std=c++11
LDFLAGS += -L/usr/local/lib/ \
			-lsnappy \
			-llzo2 \
			-lz

all: compress

.PHONY: clean

clean:
	@rm -f compress *.o
