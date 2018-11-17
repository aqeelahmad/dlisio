#ifndef DLISIO_PYTHON_TYPECONV_HPP
#define DLISIO_PYTHON_TYPECONV_HPP

#include <complex>
#include <tuple>
#include <utility>
#include <vector>

namespace dl {

struct datetime {
    int Y, TZ, M, D, H, MN, S, MS;
};

int sshort( const char*& xs ) noexcept;
int snorm( const char*& xs ) noexcept;
long slong( const char*& xs ) noexcept;

int ushort( const char*& xs ) noexcept;
int unorm( const char*& xs ) noexcept;
long ulong( const char*& xs ) noexcept;

float fshort( const char*& xs ) noexcept;
float fsingl(  const char*& xs ) noexcept;
double fdoubl( const char*& xs ) noexcept;

float isingl(  const char*& xs ) noexcept;
float vsingl(  const char*& xs ) noexcept;

std::pair< float, float > fsing1( const char*& xs ) noexcept;
std::tuple< float, float, float > fsing2( const char*& xs ) noexcept;
std::complex< float > csingl( const char*& xs ) noexcept;

std::pair< double, double > fdoub1( const char*& xs ) noexcept;
std::tuple< double, double, double > fdoub2( const char*& xs ) noexcept;
std::complex< double > cdoubl( const char*& xs ) noexcept;

long uvari( const char*& xs ) noexcept;

std::string ident( const char*& xs );
std::string ascii( const char*& xs );

datetime dtime( const char*& xs ) noexcept;

long origin( const char*& xs ) noexcept;

std::tuple< long, int, std::string > obname( const char*& xs );
std::tuple< std::string, long, int, std::string > objref( const char*& xs );

int status( const char*& xs ) noexcept;

}

#endif //DLISIO_PYTHON_TYPECONV_HPP
