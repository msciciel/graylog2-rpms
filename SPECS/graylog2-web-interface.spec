Name:		graylog2-web-interface
Version:	0.20.0
Release:	preview.8
Summary:	A front-end web interface for the Graylog2 syslog receiver

Group:		Monitoring/Logging
License:	GPL 3.0
URL:		http://graylog2.org/
Source0:	https://github.com/Graylog2/%{name}/releases/download/%{version}-%{release}/%{name}-%{version}-%{release}.tgz
Source1:	init.d-graylog2-web-interface
Source2:	sysconfig-graylog2-web-interface
Source3:	logrotate.d-graylog2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	chkconfig
Requires:       jre >= 1.6.0

%description

A front-end web interface for the Graylog2 syslog receiver. This package relies on the configured
REST interfaces of the graylog2-server package and requires almost no other configuration options. 

%prep
%setup -q -n %{name}-%{version}-%{release}


%build
true

%install
rm -rf %{buildroot}

# Sysconfig and Init
%{__mkdir} -p %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Logs and Run
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/graylog2
%{__mkdir} -p %{buildroot}%{_localstatedir}/run/graylog2
%{__mkdir} -p %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -p %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install Root
%{__mkdir} -p %{buildroot}/opt/%{name}
%{__mkdir} -p %{buildroot}/opt/%{name}/conf
%{__mkdir} -p %{buildroot}/opt/%{name}/lib
%{__mkdir} -p %{buildroot}/opt/%{name}/share

%{__install} -p conf/* %{buildroot}/opt/%{name}/conf
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
%{_sysconfdir}/rc.d/init.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

# Logs and Run
%dir %{_sysconfdir}/logrotate.d
%dir %{_localstatedir}/run/graylog2
%dir %{_localstatedir}/log/graylog2
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

# Install Root
%dir /opt/%{name}
%dir /opt/%{name}/lib
%dir /opt/%{name}/share
%config(noreplace) /opt/%{name}/conf/*
/opt/%{name}/lib/*
/opt/%{name}/share/*


%changelog
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
