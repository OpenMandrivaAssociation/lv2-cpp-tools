%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A LV2 Development SDK
Name:		lv2-c++-tools
Version:	1.0.2
Release:	%mkrel 3
License:	GPLv3+
Group:		Sound
URL:		http://ll-plugins.nongnu.org/hacking.html
Source0:	http://download.savannah.nongnu.org/releases/ll-plugins/%{name}-%{version}.tar.bz2
BuildRequires:	boost-devel
BuildRequires:	gtkmm2.4-devel >= 2.6.0
BuildRequires:	pkgconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Summary:	Development headers and libraries for %{oname}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%prep

%setup -q -n %{name}-%{version}

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
rm -rf %{buildroot}

%makeinstall_std \
    prefix=%{_prefix} \
    libdir=%{_libdir} \
    pkgdocdir=%{_docdir}/%{name}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}
%{_bindir}/lv2peg
%{_bindir}/lv2soname

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
