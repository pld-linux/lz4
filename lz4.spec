# NOTE:
# - probably version could be set 1.0.7 for r107, see lz4cli.c and
#   https://code.google.com/p/lz4/issues/detail?id=88#c4
%define		rel	1
%define		svnrev	107
Summary:	Hash-based Predictive Lempel-Ziv compressor
Summary(pl.UTF-8):	Kompresor wykorzystujący metodę Lempel-Ziv z predykcją opartą na haszach
Name:		lz4
Version:	0.0
Release:	0.svn%{svnrev}.%{rel}
License:	BSD (library), GPL v2+ (CLI utility)
Group:		Libraries
Source0:	https://dl.dropboxusercontent.com/u/59565338/LZ4/%{name}-r%{svnrev}.tar.gz
# Source0-md5:	626947ce4c67f87fdce8922ae0f4cc00
URL:		http://fastcompression.blogspot.com/p/lz4.html
BuildRequires:	cmake >= 2.6
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
%setup -qn %{name}-r%{svnrev}

%{__sed} -i -e 's/-Os -march=native/%{rpmcflags}/' cmake/CMakeLists.txt

%build
cd cmake
%cmake . \
	-DBUILD_SHARED_LIBS=TRUE

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# all available build systems suck in some way:
# 1) make-based installed creates only man and exe (no library, no headers)
#
# 2) cmake based build system creates lib and exe (no man pages), and names
# executable based on arch (!), installs headers, but the SONAME is filled
# incorrectly: liblz4.so.0.0

# so forget all that and just install from spec
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_mandir}/man1,%{_includedir}}

# shared lib
install -p cmake/liblz4.so.0.* $RPM_BUILD_ROOT%{_libdir}/liblz4.so.0.0.%{svnrev}
ln -s $(basename $RPM_BUILD_ROOT%{_libdir}/liblz4.so.0.*) $RPM_BUILD_ROOT%{_libdir}/liblz4.so
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

# static lib
cp -p cmake/liblz4.a $RPM_BUILD_ROOT%{_libdir}

# headers
cp -a {lz4,lz4hc}.h $RPM_BUILD_ROOT%{_includedir}

# binary
install -p cmake/lz4c* $RPM_BUILD_ROOT%{_bindir}/lz4

# man page
cp -p lz4.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS
%attr(755,root,root) %{_bindir}/lz4
%{_mandir}/man1/lz4.1*
%attr(755,root,root) %{_libdir}/liblz4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblz4.so.0.0

%files devel
%defattr(644,root,root,755)
%doc LZ4_Streaming_Format.odt lz4_format_description.txt
%attr(755,root,root) %{_libdir}/liblz4.so
%{_includedir}/lz4.h
%{_includedir}/lz4hc.h

%files static
%defattr(644,root,root,755)
%{_libdir}/liblz4.a
