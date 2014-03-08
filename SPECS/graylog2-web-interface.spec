Name:		graylog2-web-interface
Version:	0.20.1
Release:	1
Summary:	A front-end web interface for the Graylog2 syslog receiver

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
Requires:       jre >= 1.6.0

%description

A front-end web interface for the Graylog2 syslog receiver. This package relies on the configured
REST interfaces of the graylog2-server package and requires almost no other configuration options. 

%prep
%setup -q -n %{name}-%{version}


%build
true

%install
rm -rf %{buildroot}

# Sysconfig and Init
%{__mkdir} -p %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Configurations
%{__mkdir} -p %{buildroot}%{_sysconfdir}/graylog2/web-interface
%{__install} -p %{SOURCE3} %{buildroot}%{_sysconfdir}/graylog2/web-interface/log4j.xml
%{__install} -p conf/* %{buildroot}%{_sysconfdir}/graylog2/web-interface

# Logs and Run
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/graylog2
%{__mkdir} -p %{buildroot}%{_localstatedir}/run/graylog2

# Install Root
%{__mkdir} -p %{buildroot}/opt/%{name}
%{__mkdir} -p %{buildroot}/opt/%{name}/conf
%{__mkdir} -p %{buildroot}/opt/%{name}/lib
%{__mkdir} -p %{buildroot}/opt/%{name}/share

%{__install} -p lib/*.jar %{buildroot}/opt/%{name}/lib

cp -pR share/ %{buildroot}/opt/%{name}/


%post
/sbin/chkconfig --add graylog2-web-interface


%preun
if [ $1 -eq 0 ]; then
  /sbin/service graylog2-web-interface stop >/dev/null 2>&1
  /sbin/chkconfig --del graylog2-web-interface
fi


%clean
rm -rf %{buildroot}


%files
%defattr(0644,root,root,0644)

# Sysconfig and Init
%dir %{_sysconfdir}/rc.d/init.d
%dir %{_sysconfdir}/sysconfig
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

# Configurations
%config(noreplace) %{_sysconfdir}/graylog2/web-interface/*

# Logs and Run
%dir %{_localstatedir}/run/graylog2
%dir %{_localstatedir}/log/graylog2

# Install Root
/opt/%{name}/*


%changelog
* Sat Feb 15 2014 Corey Hammerton <corey.hammeton@gmail.com> 0.20.0-rc.3
- See https://github.com/Graylog2/graylog2-web-interface/commits/play for full changelog

* Sat Jan 18 2014 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-rc.1
- New Release Candidate version

* Mon Dec 16 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.8
- New preview version

* Sat Nov 30 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.7
- New preview version

* Sat Nov 23 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.6
- New preview version
- Removing management of the graylog2 group and passwd entries

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
