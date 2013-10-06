%define		rel	1
%define		svnrev	106
Summary:	Hash-based Predictive Lempel-Ziv compressor
Name:		lz4
Version:	0.0
Release:	0.svn%{svnrev}.%{rel}
License:	GPL-2.0+ and BSD-2-Clause
Group:		Libraries
Source0:	https://dl.dropboxusercontent.com/u/59565338/LZ4/%{name}-r%{svnrev}.tar.gz
# Source0-md5:	4d071aaecd42dd383dd58c5a7577663b
URL:		http://fastcompression.blogspot.com/p/lz4.html
BuildRequires:	cmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LZ4 is a very fast compressor, based on well-known LZ77 (Lempel-Ziv)
algorithm. It is a LZP2 fork and provides better compression ratio for
text files.

%package devel
Summary:	Development files for the LZ4 compressor
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
LZ4 is a very fast compressor, based on well-known LZ77 (Lempel-Ziv)
algorithm. It is a LZP2 fork and provides better compression ratio for
text files.

This subpackage contains libraries and header files for developing
applications that want to make use of liblz4.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -qn %{name}-r%{svnrev}

%build
cd cmake
%cmake \
	-DBUILD_SHARED_LIBS=TRUE \
	.

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
%attr(755,root,root) %{_bindir}/lz4
%{_mandir}/man1/lz4.1*
%attr(755,root,root) %{_libdir}/liblz4.so.*.*.*
%ghost %{_libdir}/liblz4.so.0.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/lz4.h
%{_includedir}/lz4hc.h
%{_libdir}/liblz4.so

%files static
%defattr(644,root,root,755)
%{_libdir}/liblz4.a
