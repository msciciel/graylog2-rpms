Name:		graylog2-server
Version:	0.20.5
Release:	0.3.BETA
Summary:	A syslog receiver and processing system

Group:		Monitoring/Logging
License:	GPL 3.0
URL:		http://graylog2.org/
Source0:	https://github.com/Graylog2/%{name}/releases/download/%{version}/%{name}-%{version}.tgz
Source1:	init.d-%{name}
Source2:	sysconfig-%{name}
Source3:	log4j-%{name}.xml
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	chkconfig
Requires:	libxml2
Requires:	jre >= 1.7.0

%description

A syslog processing system that stores received messages in an Elasticsearch database. When coupled with 
the graylog2-web-interface, which provides a front-end web interface, will allow for powerful message
analytics for a server network. 

Other information, including but not limited to user credentials, stream configurations, etc, are stored
in MongoDB


%prep
%setup -q -n %{name}-%{version}


%build
true

%install
rm -rf %{buildroot}

# Config
%{__mkdir} -p %{buildroot}%{_sysconfdir}/graylog2/server
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p graylog2.conf.example %{buildroot}%{_sysconfdir}/graylog2/server/server.conf
%{__install} -p %{SOURCE3} %{buildroot}%{_sysconfdir}/graylog2/server/log4j.xml
%{__install} -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# INIT scripts
%{__mkdir} -p %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -p -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}

# Logs and Run
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/graylog2
%{__mkdir} -p %{buildroot}%{_localstatedir}/run/graylog2

# Install Root
%{__mkdir} -p %{buildroot}/opt/%{name}
%{__mkdir} -p %{buildroot}/opt/%{name}/plugin
%{__install} -p -m 644 graylog2-server.jar %{buildroot}/opt/%{name}/
cp -pR plugin/* %{buildroot}/opt/%{name}/plugin


%post
/sbin/chkconfig --add graylog2-server


%preun
if [ $1 -eq 0 ]; then
  /sbin/service graylog2-server stop >/dev/null 2>&1
  /sbin/chkconfig --del graylog2-server
fi

%clean
rm -rf %{buildroot}


%files
%defattr(0644,root,root,0644)

# Configurations
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/graylog2/server/*

# INIT scripts
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/%{name}

# Logs and Run
%dir %{_localstatedir}/run/graylog2
%dir %{_localstatedir}/log/graylog2

# Install root
/opt/%{name}/*


%changelog
* Tue Jul 15 2014 Krzysztof Pawlowski <msciciel@msciciel.eu> 0.20.5
- Version bump to 0.20.5
- Change config file path to /etc/graylog2/server/server.conf

* Sat Mar 29 2014 Corey Hammerton <corey.hammerton@gmail.com> 0.20.1-2
- Waiting for clean shutdown in init script stop function before continuing
- See https://github.com/Graylog2/graylog2-server/commits/020 for full changelog

* Sat Feb 15 2014 Corey Hammerton <corey.hammeton@gmail.com> 0.20.0-rc.3
- See https://github.com/Graylog2/graylog2-server/commits/020 for full changelog

* Sat Jan 18 2014 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-rc.1
- New Release Candidate version

* Mon Dec 16 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.8
- New preview version

* Sat Nov 30 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.7
- New preview version
- Moving the graylog2.conf location from /etc/ to /etc/graylog2/

* Sat Nov 23 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.5
- New preview version
- Removing management of graylog2 group and passwd entries

* Fri Nov 1 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.5
- New upstream version

* Sat Oct 25 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.4
- New upstream version
- Creating group and passwd entries for graylog2
- Creating the log directory and install root owned by the new graylog2 user and group

* Wed Oct 16 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.3
- New upstream version

* Wed Oct 9 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.2
- Updating to version 0.20.0-preview.2

* Sat Oct 5 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.1
- Initial SPEC file
