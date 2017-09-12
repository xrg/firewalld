%define git_repo firewalld
%define git_head HEAD
%{?!make_build: %global make_build make -O %_smp_mflags }

Name:		firewalld
Version:	%git_get_ver
Release:	%mkrel %git_get_rel2
Summary:	A firewall daemon with D-Bus interface providing a dynamic firewall
Group:          System/Servers
License:	GPLv2+
URL:		http://www.firewalld.org
Source:		%git_bs_source %{name}-%{version}.tar.gz
Source1:	%{name}-gitrpm.version
Source2:	%{name}-changelog.gitrpm.txt
BuildArch:	noarch
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
BuildRequires:	systemd-units
BuildRequires:	docbook-style-xsl
BuildRequires:	python3-devel
BuildRequires:	iptables 
BuildRequires:	ipset 
BuildRequires:	ebtables

Requires:	iptables
Requires:	ipset
Requires:	ebtables
Requires:	firewalld-filesystem = %{version}-%{release}
Requires:	python3-firewall = %{version}-%{release}

%description
Firewalld provides a dynamically managed firewall with support for
network/firewall zones that define the trust level of network
connections or interfaces. It has support for IPv4, IPv6 firewall
settings, ethernet bridges and IP sets. There is a separation of
runtime and permanent configuration options. It also provides an
interface for services or applications to add firewall rules directly.

%package -n python3-firewall
Summary:	Python3 bindings for firewalld
Group:		Development/Python
Requires:	python3-dbus
Requires:	python3-slip-dbus
Requires:	python3-decorator
Requires:	python3-gobject3

%description -n python3-firewall
Python3 bindings for firewalld.

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
Requires:	python3-gobject3
Requires:	libnotify
Requires:	dbus-x11
Requires:       python3-qt5-core
Requires:       python3-qt5-gui 
Requires:       python3-qt5-widgets

%description -n firewall-applet
The firewall panel applet provides a status information of firewalld as
well as the settings of the firewall.

%package -n firewall-config
Summary:	Firewall configuration application
Group:          System/Servers
Requires:	%{name} = %{version}-%{release}
Requires:	python3-gobject3
Requires:	dbus-x11

%description -n firewall-config
The firewall configuration application provides a configuration interface
for firewalld.

%prep
%git_get_source
%setup -q

cp -a . %{py3dir}

sed -i -e 's|/usr/bin/python -Es|%{__python3} -Es|' %{py3dir}/fix_python_shebang.sh
sed -i 's|/usr/bin/python|%{__python3}|' %{py3dir}/config/lockdown-whitelist.xml

%build
./autogen.sh
%configure2_5x --enable-sysconfig --enable-rpmmacros
# Enable the make line if there are patches affecting man pages to
# regenerate them
%make_build

pushd %{py3dir}
./autogen.sh
%configure2_5x --enable-sysconfig --enable-rpmmacros PYTHON=%{__python3}
%make_build
popd

%install
pushd %{py3dir}
%make_install PYTHON=%{__python3}
popd

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
%{_mandir}/man1/firewall*cmd*.1*
%{_mandir}/man1/firewalld*.1*
%{_mandir}/man1/firewall*.1.*
%{_mandir}/man5/firewall*.5*

%files -n python3-firewall
%attr(0755,root,root) %dir %{python3_sitelib}/firewall
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/__pycache__
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/config
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/config/__pycache__
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core/__pycache__
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core/io
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/core/io/__pycache__
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/server
%attr(0755,root,root) %dir %{python3_sitelib}/firewall/server/__pycache__
%{python3_sitelib}/firewall/__pycache__/*.py*
%{python3_sitelib}/firewall/*.py*
%{python3_sitelib}/firewall/config/*.py*
%{python3_sitelib}/firewall/config/__pycache__/*.py*
%{python3_sitelib}/firewall/core/*.py*
%{python3_sitelib}/firewall/core/__pycache__/*.py*
%{python3_sitelib}/firewall/core/io/*.py*
%{python3_sitelib}/firewall/core/io/__pycache__/*.py*
%{python3_sitelib}/firewall/server/*.py*
%{python3_sitelib}/firewall/server/__pycache__/*.py*

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
