%define		rel	0.1
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

%prep
%setup -qn %{name}-r%{svnrev}
%{__sed} -i -e 's,CFLAGS=,CFLAGS=$(OPTFLAGS) ,' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lz4
%{_mandir}/man1/lz4.1*

%if 0
%{_libdir}/liblz4-*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/lz4*.h
%{_libdir}/liblz4.so
%endif
