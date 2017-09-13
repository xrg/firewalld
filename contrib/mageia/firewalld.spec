%define git_repo firewalld
%define git_head HEAD

%if (0%{?fedora} >= 13 || 0%{?rhel} > 7)
%global with_python3 1
%if (0%{?fedora} >= 23 || 0%{?rhel} >= 8)
%global use_python3 1
%endif
%else
%if (0%{?mageia} > 5 )
%global with_python3 1
%endif
%endif


%{?!make_build: %global make_build make -O %_smp_mflags }
%{?!make_install: %global make_install make install }
%{?!python2_sitelib: %global python2_sitelib %{python_sitelib} }


Summary:	A firewall daemon with D-Bus interface providing a dynamic firewall
Name:		firewalld
Version:	%git_get_ver
Release:	%mkrel %git_get_rel2
URL:		http://www.firewalld.org
Group:          System/Servers
License:	GPLv2+
Source:		%git_bs_source %{name}-%{version}.tar.gz
Source1:	%{name}-gitrpm.version
Source2:	%{name}-changelog.gitrpm.txt
BuildArch:	noarch
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
BuildRequires:	systemd-units
BuildRequires:	docbook-style-xsl
BuildRequires:  python-devel
BuildRequires: xsltproc
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif #0%{?with_python3}
BuildRequires:	iptables 
BuildRequires:	ipset 
BuildRequires:	ebtables

Requires:	iptables
Requires:	ipset
Requires:	ebtables
Requires:	firewalld-filesystem = %{version}-%{release}
%if 0%{?use_python3}
Requires:	python3-firewall = %{version}-%{release}
%else #0%{?use_python3}
Requires: python-firewall  = %{version}-%{release}
%endif #0%{?use_python3}


%description
Firewalld provides a dynamically managed firewall with support for
network/firewall zones that define the trust level of network
connections or interfaces. It has support for IPv4, IPv6 firewall
settings, ethernet bridges and IP sets. There is a separation of
runtime and permanent configuration options. It also provides an
interface for services or applications to add firewall rules directly.


%package -n python-firewall
Summary: Python2 bindings for firewalld
Provides: python2-firewall
Obsoletes: python2-firewall
Requires: dbus-python
Requires: python-slip-dbus
Requires: python-decorator
Requires: python-gobject

%description -n python-firewall
Python2 bindings for firewalld.

%if 0%{?with_python3}
%package -n python3-firewall
Summary:	Python3 bindings for firewalld
Group:		Development/Python
Requires:	python3-dbus
Requires:	python3-slip-dbus
Requires:	python3-decorator
Requires:	python3-gobject3

%description -n python3-firewall
Python3 bindings for firewalld.
%endif #0%{?with_python3}

%package -n firewalld-filesystem
Summary:	Firewalld directory layout and rpm macros
Group:          System/Servers

%description -n firewalld-filesystem
This package provides directories and rpm macros which are required by
other packages that add firewalld configuration files.

%package -n firewall-applet
Summary:	Firewall panel applet
Group:          System/Servers
Requires:	%{name} = %{version}-%{release}
Requires:	firewall-config = %{version}-%{release}
%if 0%{?use_python3}
Requires: python3-qt5
Requires: python3-gobject
Requires:       python3-qt5-core
Requires:       python3-qt5-gui 
Requires:       python3-qt5-widgets
%else
Requires: python-qt5
Requires: python-gobject
%endif
Requires:	libnotify
Requires:	dbus-x11

%description -n firewall-applet
The firewall panel applet provides a status information of firewalld as
well as the settings of the firewall.

%package -n firewall-config
Summary:	Firewall configuration application
Group:          System/Servers
Requires:	%{name} = %{version}-%{release}
%if 0%{?use_python3}
Requires:	python3-gobject3
%else
Requires: python-gobject
%endif
Requires:	dbus-x11

%description -n firewall-config
The firewall configuration application provides a configuration interface
for firewalld.

%prep
%git_get_source
%setup -q

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}

%if 0%{?use_python3}
sed -i -e 's|/usr/bin/python -Es|%{__python3} -Es|' %{py3dir}/fix_python_shebang.sh
sed -i 's|/usr/bin/python|%{__python3}|' %{py3dir}/config/lockdown-whitelist.xml
%endif #0%{?use_python3}
%endif #0%{?with_python3}


%build
./autogen.sh
%configure2_5x --enable-sysconfig --enable-rpmmacros
# Enable the make line if there are patches affecting man pages to
# regenerate them
%make_build

%if 0%{?with_python3}
pushd %{py3dir}
./autogen.sh
%configure2_5x --enable-sysconfig --enable-rpmmacros PYTHON=%{__python3}
%make_build
popd
%endif #0%{?with_python3}

%install
%if 0%{?use_python3}
make -C src install-nobase_dist_pythonDATA PYTHON=%{__python2} DESTDIR=%{buildroot}
%else
%make_install PYTHON=%{__python2} DESTDIR=%{buildroot}
%endif #0%{?use_python3}

%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?use_python3}
%make_install PYTHON=%{__python3}
%else
make -C src install-nobase_dist_pythonDATA PYTHON=%{__python3} DESTDIR=%{buildroot}
%endif #0%{?use_python3}
popd
%endif #0%{?with_python3}

desktop-file-install --delete-original \
  --dir %{buildroot}%{_sysconfdir}/xdg/autostart \
  %{buildroot}%{_sysconfdir}/xdg/autostart/firewall-applet.desktop
desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/firewall-config.desktop

%find_lang %{name} --all-name

%files -f %{name}.lang
%doc COPYING README
%{_sbindir}/firewalld
%{_bindir}/firewall-cmd
%{_bindir}/firewallctl
%{_bindir}/firewall-offline-cmd
%{_datadir}/bash-completion/completions/firewall-cmd
%{_prefix}/lib/firewalld/helpers/*.xml
%{_prefix}/lib/firewalld/icmptypes/*.xml
%{_prefix}/lib/firewalld/ipsets/README
%{_prefix}/lib/firewalld/services/*.xml
%{_prefix}/lib/firewalld/zones/*.xml
%{_prefix}/lib/firewalld/xmlschema/check.sh
%{_prefix}/lib/firewalld/xmlschema/*.xsd
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld
%config(noreplace) %{_sysconfdir}/firewalld/firewalld.conf
%config(noreplace) %{_sysconfdir}/firewalld/lockdown-whitelist.xml
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld/icmptypes
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld/services
%attr(0750,root,root) %dir %{_sysconfdir}/firewalld/zones
%config(noreplace) %{_sysconfdir}/sysconfig/firewalld
%{_unitdir}/firewalld.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/FirewallD.conf
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.desktop.policy
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.server.policy
%{_datadir}/polkit-1/actions/org.fedoraproject.FirewallD1.policy
# {_mandir}/man1/firewall*cmd*.1*
# {_mandir}/man1/firewalld*.1*
%{_mandir}/man1/firewall*.1.*
%{_mandir}/man5/firewall*.5*

%files -n python-firewall
%attr(0755,root,root) %dir %{python2_sitelib}/firewall
%attr(0755,root,root) %dir %{python2_sitelib}/firewall/config
%attr(0755,root,root) %dir %{python2_sitelib}/firewall/core
%attr(0755,root,root) %dir %{python2_sitelib}/firewall/core/io
%attr(0755,root,root) %dir %{python2_sitelib}/firewall/server
%{python2_sitelib}/firewall/*.py*
%{python2_sitelib}/firewall/config/*.py*
%{python2_sitelib}/firewall/core/*.py*
%{python2_sitelib}/firewall/core/io/*.py*
%{python2_sitelib}/firewall/server/*.py*

%if 0%{?with_python3}
%files -n python3-firewall
%attr(0755,root,root) %dir %{python3_sitelib}/firewall
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/config
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core/io
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/server
%{python3_sitelib}/firewall/*.py*
%{python3_sitelib}/firewall/config/*.py*
%{python3_sitelib}/firewall/core/*.py*
%{python3_sitelib}/firewall/core/io/*.py*
%{python3_sitelib}/firewall/server/*.py*
%endif #0%{?with_python3}

%files -n firewalld-filesystem
%dir %{_prefix}/lib/firewalld
%dir %{_prefix}/lib/firewalld/helpers
%dir %{_prefix}/lib/firewalld/icmptypes
%dir %{_prefix}/lib/firewalld/services
%dir %{_prefix}/lib/firewalld/zones
%dir %{_prefix}/lib/firewalld/xmlschema
%{_rpmconfigdir}/macros.d/macros.firewalld

%files -n firewall-applet
%{_bindir}/firewall-applet
%{_sysconfdir}/xdg/autostart/firewall-applet.desktop
%dir %{_sysconfdir}/firewall
%{_sysconfdir}/firewall/applet.conf
%{_datadir}/icons/hicolor/*/apps/firewall-applet*.*
%{_mandir}/man1/firewall-applet*.1*

%files -n firewall-config
%{_bindir}/firewall-config
%{_datadir}/firewalld/firewall-config.glade
%{_datadir}/firewalld/gtk3_chooserbutton.py*
%{_datadir}/firewalld/gtk3_niceexpander.py*
%{_datadir}/firewalld/tests/firewall*
%{_datadir}/applications/firewall-config.desktop
%{_datadir}/appdata/firewall-config.appdata.xml
%{_datadir}/icons/hicolor/*/apps/firewall-config*.*
%{_datadir}/glib-2.0/schemas/org.fedoraproject.FirewallConfig.gschema.xml
%{_mandir}/man1/firewall-config*.1*
