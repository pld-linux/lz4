# NOTE:
# - probably version could be set 1.0.7 for r107, see lz4cli.c and
#   https://code.google.com/p/lz4/issues/detail?id=88#c4
%define		rel	2
%define		subver	r121
Summary:	Hash-based Predictive Lempel-Ziv compressor
Summary(pl.UTF-8):	Kompresor wykorzystujący metodę Lempel-Ziv z predykcją opartą na haszach
Name:		lz4
Version:	0.0
Release:	1.%{subver}.%{rel}
License:	BSD (library), GPL v2+ (CLI utility)
Group:		Libraries
Source0:	https://github.com/Cyan4973/lz4/archive/%{subver}/%{name}-%{subver}.tar.gz
# Source0-md5:	2de6fe3c2f8d52d9532a913b0e3b6465
URL:		http://fastcompression.blogspot.com/p/lz4.html
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LZ4 is a very fast compressor, based on well-known LZ77 (Lempel-Ziv)
algorithm. It is a LZP2 fork and provides better compression ratio for
text files.

%description -l pl.UTF-8
LZ4 to bardzo szybki kompresor, oparty na dobrze znanym algorytmie
LZ77 (Lempel-Ziv). Jest to odgałęzienie LZP2, zapewniające lepszy
współczynnik kompresji dla plików tekstowych.

%package devel
Summary:	Development files for the LZ4 compressor
Summary(pl.UTF-8):	Pliki programistyczne kompresora LZ4
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
LZ4 is a very fast compressor, based on well-known LZ77 (Lempel-Ziv)
algorithm. It is a LZP2 fork and provides better compression ratio for
text files.

This subpackage contains the header files for developing applications
that want to make use of liblz4.

%description devel -l pl.UTF-8
LZ4 to bardzo szybki kompresor, oparty na dobrze znanym algorytmie
LZ77 (Lempel-Ziv). Jest to odgałęzienie LZP2, zapewniające lepszy
współczynnik kompresji dla plików tekstowych.

Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących liblz4.

%package static
Summary:	Static LZ4 compressor library
Summary(pl.UTF-8):	Statyczna biblioteka kompresora LZ4
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LZ4 compressor library.

%description static -l pl.UTF-8
Statyczna biblioteka kompresora LZ4.

%prep
%setup -qn %{name}-%{subver}

mv cmake{_unofficial,}
%{__sed} -i -e 's/-Os -march=native/%{rpmcflags}/' cmake/CMakeLists.txt

%build
CFLAGS="%{rpmcflags}"
%{__make} \
	CC="%{__cc}" \
	CPPFLAGS="%{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	LIBDIR=%{_libdir} \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT \

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md NEWS LICENSE
%attr(755,root,root) %{_bindir}/lz4
%attr(755,root,root) %{_bindir}/lz4c
%attr(755,root,root) %{_bindir}/lz4cat
%{_mandir}/man1/lz4.1*
%{_mandir}/man1/lz4c.1*
%{_mandir}/man1/lz4cat.1*
%attr(755,root,root) %{_libdir}/liblz4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblz4.so.1

%files devel
%defattr(644,root,root,755)
%doc LZ4_Streaming_Format.odt lz4_format_description.txt
%attr(755,root,root) %{_libdir}/liblz4.so
%{_includedir}/lz4.h
%{_includedir}/lz4hc.h
%{_pkgconfigdir}/liblz4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblz4.a
