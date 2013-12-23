%define major 27
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	An HTTP and WebDAV client library, with a C interface
Name:		neon
Version:	0.30.0
Release:	1
Group:		Development/Other
License:	GPLv2+ and LGPLv2+
Url:		http://www.webdav.org/neon/
Source0:	http://www.webdav.org/neon/%{name}-%{version}.tar.gz
Source1:	http://www.webdav.org/neon/%{name}-%{version}.tar.gz.asc
Patch0:		neon-locales.diff
Patch1:		neon-fail_parse.diff
Patch2:		neon-borked_addr_reverse.diff
Patch3:		neon-borked_retry_notcompress_and_retry_compress.diff
Patch4:		neon-borked_read_reset.diff
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=476571
Patch6:		neon-0.28.2-fix-segfault.patch
Patch7:		neon-0.29.6-neon-config_cleanups.diff

BuildRequires:	libtool
BuildRequires:	krb5-devel
BuildRequires:	pkgconfig(libcrypto) >= 0.9.7
BuildRequires:	pkgconfig(libssl) >= 0.9.7
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(zlib)

%description
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.

%package i18n
Summary:	Language files for Neon
Group:		System/Internationalization 
BuildArch:	noarch

%description i18n
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.

%package -n	%{libname}
Summary:	Shared library for Neon
Group:		System/Libraries
%define	bogus %mklibname %{name} 0.27
%rename		%{bogus}

%description -n %{libname}
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.

%package -n	%{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C++
Requires:	%{libname} >= %{EVRD}
Provides:	neon-devel = %{EVRD}
Obsoletes:	%{mklibname neon 0.27 -d} < 0.29.6-7
Conflicts:	%{mklibname neon 0.26}-devel < 0.29.6-7

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch6 -p1
%patch7 -p1

# fix mo clash (#28428)
# this goes with the changes done by Patch0
perl -pi -e "s|_LIBNAME_|%{libname}|g" Makefile.in src/ne_internal.h

# this value has to be raised on x86_64
perl -pi -e "s|^ulimit \-v .*|ulimit \-v 40960|g" test/run.sh

%build
%configure2_5x \
	--enable-shared \
	--disable-static \
	--with-ssl=openssl \
	--enable-threadsafe-ssl=posix \
	--with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
	--with-libxml2 \
	--without-libproxy

%make

%check
make check

%install
%makeinstall_std

mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libneon.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libneon.so.%{major}.*.* %{buildroot}%{_libdir}/libneon.so

# fix this
rm -rf %{buildroot}%{_datadir}/doc

%find_lang %{libname} --all-name

cp src/README README.neon

%files i18n -f %{libname}.lang
%doc doc/*.txt README.neon

%files -n %{libname}
/%{_lib}/libneon.so.%{major}*

%files -n %{devname}
%doc AUTHORS BUGS doc/html ChangeLog NEWS README THANKS TODO
%{_bindir}/neon-config
%{_libdir}/libneon.so
%{_libdir}/pkgconfig/neon.pc
%dir %{_includedir}/neon
%{_includedir}/neon/*
%{_mandir}/man1/*
%{_mandir}/man3/*

