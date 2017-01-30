#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Tool for interacting with the PIV applet on a YubiKey NEO
Name:		yubico-piv-tool
Version:	1.4.2
Release:	1
License:	GPL v3+
Group:		Applications
Source0:	https://developers.yubico.com/yubico-piv-tool/Releases/%{name}-%{version}.tar.gz
# Source0-md5:	b03dc5adef8504f822a7586e65f5b33c
URL:		https://developers.yubico.com/yubico-piv-tool/
BuildRequires:	openssl-devel
BuildRequires:	pcsc-lite-devel
Requires:	pcsc-driver-ccid
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Yubico PIV tool is used for interacting with the Privilege and
Identification Card (PIV) applet on a YubiKey NEO.

With it you may generate keys on the device, importing keys and
certificates, and create certificate requests, and other operations. A
shared library and a command-line tool is included.

%package devel
Summary:	Tool for interacting with the PIV applet on a YubiKey NEO
Requires:	%{name} = %{version}-%{release}

%description devel
The Yubico PIV tool is used for interacting with the Privilege and
Identification Card (PIV) applet on a YubiKey NEO. This package
includes development files.

%prep
%setup -q

%build
%configure \
	--with-backend="pcsc" \
	--disable-silent-rules

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libykpiv.{la,a}
rm $RPM_BUILD_ROOT%{_libdir}/libykcs11.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/yubico-piv-tool
%attr(755,root,root) %ghost %{_libdir}/libykpiv.so.1
%attr(755,root,root) %{_libdir}/libykpiv.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libykcs11.so.1
%attr(755,root,root) %{_libdir}/libykcs11.so.*.*
%{_mandir}/man1/yubico-piv-tool.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libykpiv.so
%attr(755,root,root) %{_libdir}/libykcs11.so
%{_pkgconfigdir}/ykpiv.pc
%{_pkgconfigdir}/ykcs11.pc
%{_includedir}/ykpiv
