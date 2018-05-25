#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# unit tests

Summary:	Tool for interacting with the PIV applet on a YubiKey NEO
Summary(pl.UTF-8):	Narzędzie do komunikacji z apletem PIV na YubiKey NEO
Name:		yubico-piv-tool
Version:	1.5.0
Release:	1
License:	BSD
Group:		Applications
Source0:	https://developers.yubico.com/yubico-piv-tool/Releases/%{name}-%{version}.tar.gz
# Source0-md5:	bcfec9fa2454ba7f7be6cc80632bd41f
URL:		https://developers.yubico.com/yubico-piv-tool/
%{?with_tests:BuildRequires:	check-devel >= 0.9.6}
BuildRequires:	help2man
BuildRequires:	openssl-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pcsc-driver-ccid
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Yubico PIV tool is used for interacting with the Privilege and
Identification Card (PIV) applet on a YubiKey NEO.

With it you may generate keys on the device, importing keys and
certificates, and create certificate requests, and other operations.

%description -l pl.UTF-8
Narzędzie Yubico PIV Tool służy do komunikacji z apletem PIV
(Privilege and Identification card) na urządzeniach YubiKey NEO.

Przy jego pomocy można generować klucze na urządzeniu, importować
klucze i certyfikaty, tworzyć żądania certyfikatów oraz wykonywać inne
operacje.

%package libs
Summary:	Yubico PIV shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Yubico PIV
Group:		Libraries

%description libs
The Yubico PIV tool is used for interacting with the Privilege and
Identification Card (PIV) applet on a YubiKey NEO. This package
contains shared libraries for the tool.

%description libs -l pl.UTF-8
Narzędzie Yubico PIV Tool służy do komunikacji z apletem PIV
(Privilege and Identification card) na urządzeniach YubiKey NEO. Ten
pakiet zawiera biblioteki współdzielone wykorzystywane przez
narzędzie.

%package devel
Summary:	Header files for Yubico PIV libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Yubico PIV
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	openssl-devel

%description devel
The Yubico PIV tool is used for interacting with the Privilege and
Identification Card (PIV) applet on a YubiKey NEO. This package
includes development files.

%description devel -l pl.UTF-8
Narzędzie Yubico PIV Tool służy do komunikacji z apletem PIV
(Privilege and Identification card) na urządzeniach YubiKey NEO. Ten
pakiet zawiera pliki programistyczne.

%package static
Summary:	Yubico PIV static libraries
Summary(pl.UTF-8):	Biblioteki statyczne Yubico PIV
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
The Yubico PIV tool is used for interacting with the Privilege and
Identification Card (PIV) applet on a YubiKey NEO. This package
includes static libraries.

%description static -l pl.UTF-8
Narzędzie Yubico PIV Tool służy do komunikacji z apletem PIV
(Privilege and Identification card) na urządzeniach YubiKey NEO. Ten
pakiet zawiera biblioteki statyczne.

%prep
%setup -q

%build
%configure \
	--with-backend="pcsc" \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{ykcs11,ykpiv}.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog NEWS README doc/*.adoc
%attr(755,root,root) %{_bindir}/yubico-piv-tool
%{_mandir}/man1/yubico-piv-tool.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libykpiv.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libykpiv.so.1
%attr(755,root,root) %{_libdir}/libykcs11.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libykcs11.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libykpiv.so
%attr(755,root,root) %{_libdir}/libykcs11.so
%{_pkgconfigdir}/ykpiv.pc
%{_pkgconfigdir}/ykcs11.pc
%{_includedir}/ykpiv

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libykpiv.a
%{_libdir}/libykcs11.a
%endif
