%define upstream_name dbus-python
%define source_subtree %{upstream_name}-%{version}
%define python_version python3

Name:		dbus-%{python_version}
Version:	1.2.0
Release:	1
Summary:	D-Bus Python bindings (for Python 3)

Group:		System Environment/Libraries
License:	MIT
URL:		http://dbus.freedesktop.org/releases/dbus-python/
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	%{python_version}-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
Requires:	%{python_version}-base

%description
%{summary}.

%package devel
Summary:        D-Bus Python bindings (for Python 3, development headers)
Requires:       %{name} = %{version}

%description devel
%{summary}.

%prep
%setup -q

%build
cd %{source_subtree}
# Make sure it builds against the right Python version
%configure PYTHON=%{python_version}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
cd %{upstream_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

# Remove .la files
find $RPM_BUILD_ROOT -name '*.la' -exec rm {} +

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/%{python_version}.*/site-packages/_dbus_bindings.so
%{_libdir}/%{python_version}.*/site-packages/_dbus_glib_bindings.so
%{_libdir}/%{python_version}.*/site-packages/dbus
%{_datadir}/doc/%{upstream_name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/dbus-1.0/dbus/%{upstream_name}.h
%{_libdir}/pkgconfig/%{upstream_name}.pc
