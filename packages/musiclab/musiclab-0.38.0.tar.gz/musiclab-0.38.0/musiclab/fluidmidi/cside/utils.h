#ifndef __CSIDE_UTILS_H__
#define __CSIDE_UTILS_H__

/* Error code interface */
#define NO_ERR       0
#define ERR         -1

typedef int _Err;

/* Endianness function interface */
#ifdef __APPLE__
    #include <libkern/OSByteOrder.h>
    #define be16toh(x) OSSwapBigToHostInt16(x)
    #define be32toh(x) OSSwapBigToHostInt32(x)
    #define htobe16(x) OSSwapHostToBigInt16(x)
    #define htobe32(x) OSSwapHostToBigInt32(x)
#else
    #include <endian.h>
#endif

/* ANSI Color code strings */
#define ANSIRED     "\033[31;1m"
#define ANSIBLUE    "\033[36;1m"
#define ANSIGREEN   "\033[32;1m"
#define ANSIYELLOW  "\033[33;1m"
#define ANSIMAGENTA "\033[35;1m"
#define ANSIEND     "\033[0m"

#ifdef MUSICLAB_CDEBUG
#include <stdio.h>
#define LOGERR(...) do {  \
    fprintf(stderr, "LOGERR: %s, line %d, in %s: ", __FILE__, __LINE__, __func__);  \
    fprintf(stderr, __VA_ARGS__);  \
} while (0);

#define LOGDBG(...) do { \
    fprintf(stderr, ANSIYELLOW "DEBUG: %s, line %d, in %s: ", __FILE__, __LINE__, __func__);  \
    fprintf(stderr, __VA_ARGS__);  \
    fprintf(stderr, ANSIEND);  \
} while (0);
#else
#define LOGERR(...)
#define LOGDBG(...)
#endif

#endif  // __CSIDE_UTILS_H__
