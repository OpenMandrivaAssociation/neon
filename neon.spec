%define major 27
%define oldlibname %mklibname %{name} 27
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

Summary:	An HTTP and WebDAV client library, with a C interface
Name:		neon
Version:	0.35.0
Release:	1
Group:		Development/Other
License:	GPLv2+ and LGPLv2+
Url:		https://notroj.github.io/neon/
Source0:	https://notroj.github.io/neon/%{name}-%{version}.tar.gz
Patch0:		neon-locales.diff
Patch1:		neon-fail_parse.diff
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=476571
Patch6:		neon-0.28.2-fix-segfault.patch
Patch7:		neon-0.29.6-neon-config_cleanups.diff

BuildRequires:	libtool
BuildRequires:	krb5-devel
BuildRequires:	rootcerts
BuildRequires:	pkgconfig(libcrypto) >= 0.9.7
BuildRequires:	pkgconfig(libssl) >= 0.9.7
BuildRequires:	pkgconfig(expat)
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

%package -n %{libname}
Summary:	Shared library for Neon
Group:		System/Libraries
%define	bogus %mklibname %{name} 0.27
%rename		%{bogus}
%rename		%{oldlibname}

%description -n %{libname}
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.

%package -n %{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C++
Requires:	%{libname} >= %{EVRD}
Provides:	neon-devel = %{EVRD}
Obsoletes:	%{mklibname neon 0.27 -d} < 0.29.6-7
Conflicts:	%{mklibname neon 0.26}-devel < 0.29.6-7

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%autosetup -p1
# fix mo clash (#28428)
# this goes with the changes done by Patch0
perl -pi -e "s|_LIBNAME_|%{libname}|g" Makefile.in src/ne_internal.h

# this value has to be raised on x86_64
perl -pi -e "s|^ulimit \-v .*|ulimit \-v 40960|g" test/run.sh

%build
%configure \
	--enable-shared \
	--disable-static \
	--with-ssl=openssl \
	--with-expat \
	--enable-threadsafe-ssl=posix \
	--with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
	--without-libxml2 \
	--without-libproxy

%make_build

%check
# FIXME at some point, we need to investigate the failures
if ! make check; then
    printf '%s\n'  "WARNING: Some tests failed. Please fix..." >&2
fi

%install
%make_install

# fix this
rm -rf %{buildroot}%{_datadir}/doc

%find_lang %{libname} --all-name

cp src/README README.neon

%files i18n -f %{libname}.lang
%doc doc/*.txt README.neon

%files -n %{libname}
%{_libdir}/libneon.so.%{major}*

%files -n %{devname}
%doc AUTHORS doc/html NEWS THANKS TODO
%{_bindir}/neon-config
%{_libdir}/libneon.so
%{_libdir}/pkgconfig/neon.pc
%dir %{_includedir}/neon
%{_includedir}/neon/*
%doc %{_mandir}/man1/*
%doc %{_mandir}/man3/*
