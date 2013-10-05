Name:		graylog2-server
Version:	0.20.0
Release:	preview.1
Summary:	A syslog receiver and processing system

Group:		Monitoring/Logging
License:	GPL 3.0
URL:		http://graylog2.org/
Source0:	https://github.com/Graylog2/%{name}/releases/download/%{version}-%{release}/%{name}-%{version}-%{release}.tgz
Source1:	init.d-graylog2-server
Source2:	sysconfig-graylog2-server
Source3:	logrotate.d-graylog2-server
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	chkconfig
Requires:	jre >= 1.6.0

%description

A syslog processing system that stores received messages in an Elasticsearch database. When coupled with 
the graylog2-web-interface, which provides a front-end web interface, will allow for powerful message
analytics for a server network. 

Other information, including but not limited to user credentials, stream configurations, etc, are stored
in MongoDB


%prep
%setup -q


%build
true

%install
rm -rf %{buildroot}

# Config
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__install} -p -m 644 graylog2.conf.example %{buildroot}%{_sysconfdir}/%{name}/graylog2.conf

# Sysconfig and Init
%{__mkdir} -p %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install Root
%{__mkdir} -p %{buildroot}/opt/%{name}
%{__mkdir} -p %{buildroot}/opt/%{name}/plugin

%{__install} -p -m 644 graylog2-server.jar %{buildroot}/opt/%{name}/


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
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/graylog2.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_localstatedir}/log/%{name}
%dir %{_sysconfdir}/logrotate.d
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/rc.d/init.d/%{name}
%dir /opt/%{name}
%dir /opt/%{name}/plugin
/opt/%{name}/graylog2-server.jar


%changelog
* Sat Oct 5 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.1-1
- Initial SPEC file
