%define major 0.27
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	An HTTP and WebDAV client library, with a C interface
Name:		neon
Version:	0.29.6
Release:	8
Group:		Development/Other
License: 	GPLv2+ and LGPLv2+
URL:		http://www.webdav.org/neon/
Source0:	http://www.webdav.org/neon/%{name}-%{version}.tar.gz
Source1:	http://www.webdav.org/neon/%{name}-%{version}.tar.gz.asc
Patch0:		neon-locales.diff
Patch1:		neon-fail_parse.diff
Patch2:		neon-borked_addr_reverse.diff
Patch3:		neon-borked_retry_notcompress_and_retry_compress.diff
Patch4:		neon-borked_read_reset.diff
Patch5:		neon-borked_simple_sslv2.diff
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

%package	i18n
Summary:	Language files for Neon
Group:		System/Internationalization 
BuildArch:	noarch

%description	i18n
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.

%package -n	%{libname}
Summary:	Shared library for Neon
Group:		System/Libraries

%description -n %{libname}
neon is an HTTP and WebDAV client library for Unix systems, 
with a C language API. It provides high-level interfaces to 
HTTP/1.1 and WebDAV  methods, and a low-level interface to 
HTTP request/response handling, allowing new methods to be 
easily implemented.

%package -n	%{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C++
Requires:	%{libname} >= %{EVRD}
Provides:	neon-devel = %{EVRD}
Obsoletes:	%{mklibname neon 0.27 -d} < 0.29.6-7
Conflicts:	%{mklibname neon 0.26}-devel < 0.29.6-7

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
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
    --with-libxml2

%make

#%%check
#%make check <- the tests are broken, and/or some of the iurt tar balls and/or some build node, take your pick

%install
rm -rf %{buildroot}
%makeinstall

# fix this
rm -rf %{buildroot}%{_datadir}/doc

%find_lang %{libname} --all-name

cp src/README README.neon

%files i18n -f %{libname}.lang
%doc doc/*.txt README.neon

%files -n %{libname}
%{_libdir}/libneon.so.27*

%files -n %{develname}
%doc AUTHORS BUGS doc/html ChangeLog NEWS README THANKS TODO
%{_bindir}/neon-config
%{_libdir}/libneon.so
%{_libdir}/pkgconfig/neon.pc
%dir %{_includedir}/neon
%{_includedir}/neon/*
%{_mandir}/man1/*
%{_mandir}/man3/*



%changelog
* Fri Mar 23 2012 Bernhard Rosenkraenzer <bero@bero.eu> 0.29.6-6
+ Revision: 786472
- Rebuild with openssl 1.0.1

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - use %%{EVRD} macro

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added comment for fix done after p0

* Wed Nov 30 2011 Oden Eriksson <oeriksson@mandriva.com> 0.29.6-5
+ Revision: 735687
- stupid build system
- disable the tests again
- fix #28428 (again!)
- fix upgrade
- mes5.2 is still around...

  + Matthew Dawkins <mattydaw@mandriva.org>
    - fixed version-version to version-release oops

* Tue Nov 29 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.29.6-3
+ Revision: 735490
- renamed spec file
- renaming package back to its proper name
- renamed name back to source tarball name
- rebuild for major spec clean up
- disabled static build
- removed .la files
- removed clean section
- reenabled check
- cleaned up BRs/requires
- many part of basesystem, others converted to pkgconfig provides
- removed legacy build hacks
- removed legacy conflicts, provides, requires
- split out i18n pkg
- dropped half baked major from devel pkg
- removed mkrel & BuildRoot
- fixed libname summary

* Tue Nov 29 2011 Oden Eriksson <oeriksson@mandriva.com> 0.29.6-2
+ Revision: 735456
- drop the libtool *.la file
- add a cleaner neon-config and neon.pc implementation (looked at fedora a bit)
- various cleanups
- fix deps

* Tue Oct 18 2011 Oden Eriksson <oeriksson@mandriva.com> 0.29.6-1
+ Revision: 705078
- 0.29.6
- disable make check for now
- more multiarch fixes

* Sun May 01 2011 Funda Wang <fwang@mandriva.org> 0.29.5-2
+ Revision: 661169
- update multiarch usage

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Fri Oct 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.29.5-1mdv2011.0
+ Revision: 585759
- 0.29.5

* Mon Oct 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.29.4-1mdv2011.0
+ Revision: 582848
- 0.29.4

* Tue Apr 06 2010 Eugeni Dodonov <eugeni@mandriva.com> 0.29.3-3mdv2010.1
+ Revision: 532356
- Rebuild for new openssl.

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 0.29.3-2mdv2010.1
+ Revision: 511588
- rebuilt against openssl-0.9.8m

* Tue Jan 12 2010 Oden Eriksson <oeriksson@mandriva.com> 0.29.3-1mdv2010.1
+ Revision: 490271
- 0.29.3

* Fri Jan 01 2010 Oden Eriksson <oeriksson@mandriva.com> 0.29.2-1mdv2010.1
+ Revision: 484671
- 0.29.2

* Wed Dec 16 2009 Oden Eriksson <oeriksson@mandriva.com> 0.29.1-1mdv2010.1
+ Revision: 479546
- 0.29.1

* Mon Sep 14 2009 Oden Eriksson <oeriksson@mandriva.com> 0.29.0-1mdv2010.0
+ Revision: 439716
- 0.29.0
- rediffed one patch

* Tue Aug 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.28.6-1mdv2010.0
+ Revision: 417795
- 0.28.6

* Sat Aug 01 2009 Frederik Himpe <fhimpe@mandriva.org> 0.28.5-1mdv2010.0
+ Revision: 407044
- update to new version 0.28.5

  + Oden Eriksson <oeriksson@mandriva.com>
    - 0.28.4

* Tue Dec 16 2008 Oden Eriksson <oeriksson@mandriva.com> 0.28.3-2mdv2009.1
+ Revision: 314883
- rebuild

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - remove truly bogus libxmlrpc-devel buildrequires

* Fri Aug 22 2008 Frederik Himpe <fhimpe@mandriva.org> 0.28.3-1mdv2009.0
+ Revision: 275231
- Update to version 0.28.3 (fixes CVE-2008-3746)

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0.28.2-3mdv2009.0
+ Revision: 264841
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Apr 28 2008 Frederik Himpe <fhimpe@mandriva.org> 0.28.2-2mdv2009.0
+ Revision: 198524
- Add patch fixing segfault
  http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=476571

* Sat Apr 19 2008 Oden Eriksson <oeriksson@mandriva.com> 0.28.2-1mdv2009.0
+ Revision: 195825
- disable two more tests (P4,P5)
- 0.28.2

* Mon Feb 11 2008 Oden Eriksson <oeriksson@mandriva.com> 0.28.0-1mdv2008.1
+ Revision: 165193
- 0.28.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 03 2007 Thierry Vignaud <tv@mandriva.org> 0.27.1-2mdv2008.1
+ Revision: 114532
- move huge HTML doc from main package into devel subpackage

  + Oden Eriksson <oeriksson@mandriva.com>
    - 0.27.1

* Thu Aug 23 2007 Oden Eriksson <oeriksson@mandriva.com> 0.27.0-2mdv2008.0
+ Revision: 69927
- fix deps (whoa!)

* Thu Aug 23 2007 Oden Eriksson <oeriksson@mandriva.com> 0.27.0-1mdv2008.0
+ Revision: 69335
- 0.27.0
- prepare for 0.27

* Tue Jul 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.26.4-1mdv2008.0
+ Revision: 52857
- revert some code to make the tests pass
- 0.26.4
- rediffed P0
- drop upstream implemented P1

