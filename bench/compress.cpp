#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>

#include <cstdio>
#include <cstring>

#include <snappy.h>
#include <lzo1x.h>

using namespace std;

size_t snappy_default(char*, size_t);
size_t lzo_default(char*, size_t);

template <typename F>
void bench(F f, char* buffer, size_t len) {
    using namespace std::chrono;

    time_point<system_clock> start, end;
    start = system_clock::now();
    size_t compressed_len = f(buffer, len);
    end = system_clock::now();

    int elapsed = duration_cast<milliseconds>(end - start).count();
    float throughput = static_cast<float>(len) / elapsed;

    float ratio = static_cast<float>(compressed_len) / len;

    printf("size=%zu B  time=%d ms  throughput=%.2f KB/sec  ratio=%.2f\n",
            len, elapsed, throughput, ratio);
}

int main(int argc, char** argv) {
    const char* input = argc>1 ? argv[1] : "240MB.txt";
    printf("file = %s\n", input);

    ifstream is(input);
    is.seekg(0, is.end);
    size_t len = is.tellg();
    is.seekg(0);

    char* buffer = new char[len+1];
    memset(buffer, 0, sizeof(*buffer) * (len+1));
    is.read(buffer, len);

    // Snappy default
    //bench(snappy_default, buffer, len);

    // LZO default
    bench(lzo_default, buffer, len);

    delete[] buffer;
}

size_t snappy_default(char* buffer, size_t len) {
    string compressed;
    snappy::Compress(buffer, len, &compressed);
    return compressed.size();
}

size_t lzo_default(char* buffer, size_t len) {
    lzo_init();

    lzo_bytep out = (lzo_bytep) malloc(sizeof(*buffer) * (len+1));
    lzo_voidp wrkmem = (lzo_voidp) malloc(LZO1X_1_15_MEM_COMPRESS);

    lzo_uint out_len, new_len;
    lzo1x_1_15_compress((lzo_bytep) buffer, len, out, &out_len, wrkmem);

    return out_len;
}
