%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A LV2 Development SDK
Name:		lv2-c++-tools
Version:	1.0.5
Release:	1
License:	GPLv3+
Group:		Sound
URL:		http://ll-plugins.nongnu.org/hacking.html
Source0:	http://download.savannah.nongnu.org/releases/ll-plugins/%{name}-%{version}.tar.bz2
Patch0:		lv2-c++-tools-boost.patch
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(gtkmm-2.4)

%description
This software package contains libraries and programs that should make it
easier to write LV2 plugins.

%package -n	%{libname}
Summary:	LV2 Development SDK library
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with the %{name} library.

%package -n	%{develname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%prep
%setup -q
%patch0 -p1

# don't invoke ldconfig
perl -pi -e "s|/sbin/ldconfig -n |/bin/true |g" Makefile.template

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" Makefile.template

%build
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir}

%make CFLAGS="%{optflags}" \
    prefix=%{_prefix} \
    libdir=%{_libdir}

%install
%make_install \
    prefix=%{_prefix} \
    libdir=%{_libdir} \
    pkgdocdir=%{_docdir}/%{name}

%files
%doc %{_docdir}/%{name}
%{_bindir}/lv2peg
%{_bindir}/lv2soname

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

