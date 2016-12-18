Summary:	Hash-based Predictive Lempel-Ziv compressor
Summary(pl.UTF-8):	Kompresor wykorzystujący metodę Lempel-Ziv z predykcją opartą na haszach
Name:		lz4
Version:	1.7.4.2
Release:	1
Epoch:		1
License:	BSD (library), GPL v2+ (CLI utility)
Group:		Applications
#Source0Download: https://github.com/lz4/lz4/releases
Source0:	https://github.com/lz4/lz4/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c8a1e198555fb0650448e498b7614ae5
URL:		http://www.lz4.org/
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LZ4 is a very fast compressor, based on well-known LZ77 (Lempel-Ziv)
algorithm. It is a LZP2 fork and provides better compression ratio for
text files.

%description -l pl.UTF-8
LZ4 to bardzo szybki kompresor, oparty na dobrze znanym algorytmie
LZ77 (Lempel-Ziv). Jest to odgałęzienie LZP2, zapewniające lepszy
współczynnik kompresji dla plików tekstowych.

%package libs
Summary:	LZ4 library
Summary(pl.UTF-8):	Biblioteka LZ4
License:	BSD
Group:		Libraries
Conflicts:	lz4 < 0.0-1.r121.3

%description libs
LZ4 library.

%description libs -l pl.UTF_8
Biblioteka LZ4.

%package devel
Summary:	Development files for the LZ4 compressor
Summary(pl.UTF-8):	Pliki programistyczne kompresora LZ4
License:	BSD
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

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
License:	BSD
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static LZ4 compressor library.

%description static -l pl.UTF-8
Statyczna biblioteka kompresora LZ4.

%prep
%setup -q

%build
%{__make} -j1 \
	MOREFLAGS="%{rpmcflags} %{rpmcppflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	INCLUDEDIR=%{_includedir}/lz4 \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT \

install -d $RPM_BUILD_ROOT/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/liblz4.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/liblz4.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/liblz4.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS README.md
%attr(755,root,root) %{_bindir}/lz4
%attr(755,root,root) %{_bindir}/lz4c
%attr(755,root,root) %{_bindir}/lz4cat
%attr(755,root,root) %{_bindir}/unlz4
%{_mandir}/man1/lz4.1*
%{_mandir}/man1/lz4c.1*
%{_mandir}/man1/lz4cat.1*
%{_mandir}/man1/unlz4.1*

%files libs
%defattr(644,root,root,755)
%doc lib/{LICENSE,README.md}
%attr(755,root,root) /%{_lib}/liblz4.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/liblz4.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblz4.so
%dir %{_includedir}/lz4
%{_includedir}/lz4/lz4.h
%{_includedir}/lz4/lz4hc.h
%{_includedir}/lz4/lz4frame.h
%{_pkgconfigdir}/liblz4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblz4.a
