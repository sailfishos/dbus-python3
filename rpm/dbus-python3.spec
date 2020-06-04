Name:		dbus-python3
Version:	1.2.16
Release:	1
Summary:	D-Bus Python bindings (for Python 3)
License:	MIT
URL:		http://www.freedesktop.org/wiki/Software/DBusBindings/
Source0:	%{name}-%{version}.tar.gz

# Apply patches to dbus-python/ and then in ./dbus-python use:
#  git format-patch --base=<upstream-tag> <upstream-tag>..<sfos/tag> -o ../rpm/
# this set is:
#  git format-patch --base=dbus-python-1.2.16 dbus-python-1.2.16..jolla/dbus-python-1.2.16 -o ../rpm/
# borrow centos7 patch to use sitearch properly
Patch0: 0001-Move-python-modules-to-architecture-specific-directo.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1788491
Patch1: 0002-Python3.9-changes-from-Redhat.patch

BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-base

# for %%check
BuildRequires:  python3-gobject
# autoreconf and friends
BuildRequires:  autoconf-archive automake libtool

%description
D-Bus python bindings for use with python programs.

%package -n python3-dbus
Summary: D-Bus bindings for python3
Provides: dbus-python3
%{?python_provide:%python_provide python3-dbus}

%description -n python3-dbus
%{summary}.


%package devel
Summary: Libraries and headers for dbus-python
%description devel
Headers and static libraries for hooking up custom mainloops to the dbus python
bindings.

%prep
%autosetup -p1 -n %{name}-%{version}/dbus-python
autoreconf -vif

%build
%py3_build
%configure PYTHON="%{__python3}"
%make_build

%install
%py3_install
%make_install


# unpackaged files
rm -fv  $RPM_BUILD_ROOT%{python3_sitearch}/*.la
rm -rfv $RPM_BUILD_ROOT%{_datadir}/doc/dbus-python/

%check
make check -k || (cat test-suite.log && false)

%files -n python3-dbus
%doc NEWS
%license COPYING
%{python3_sitearch}/*.so
%{python3_sitearch}/dbus/
%{python3_sitearch}/dbus_python*egg-info

%files devel
%doc README ChangeLog doc/API_CHANGES.txt doc/tutorial.txt
%{_includedir}/dbus-1.0/dbus/dbus-python.h
%{_libdir}/pkgconfig/dbus-python.pc
