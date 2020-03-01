Name:		libva
Version:	2.6.1
Release:	1%{?dist}
Summary:	Video Acceleration (VA) API for Linux
License:	MIT
URL:		https://github.com/intel/libva
Source0:	%{url}/archive/%{version}%{?pre_release}/%{name}-%{version}%{?pre_release}.tar.gz

BuildRequires:	libtool

BuildRequires:	libudev-devel
BuildRequires:	libdrm-devel
BuildRequires:  libpciaccess-devel
BuildRequires:	mesa-llvmpipe-libGLESv1-devel
BuildRequires:  mesa-llvmpipe-libGLESv2-devel
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client) >= 1
BuildRequires:  pkgconfig(wayland-scanner) >= 1

# owns the %%{_libdir}/dri directory
#Requires:	mesa-dri-filesystem

%description
Libva is a library providing the VA API video acceleration API.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n %{name}-%{version}%{?pre_release}/%{name}
autoreconf -vif

%build
%configure --disable-static \
	   --enable-wayland

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install INSTALL="install -p"
find %{buildroot} -regex ".*\.la$" | xargs rm -f --


%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig


%files
%doc NEWS
%license COPYING
%ghost %{_sysconfdir}/libva.conf
%{_libdir}/libva*.so.*

%files devel
%{_includedir}/va
%{_libdir}/libva*.so
%{_libdir}/pkgconfig/libva*.pc


