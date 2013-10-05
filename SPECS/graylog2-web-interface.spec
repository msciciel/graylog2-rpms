Name:		graylog2-web-interface
Version:	0.20.0
Release:	preview.1
Summary:	A front-end web interface for the Graylog2 syslog receiver

Group:		Monitoring/Logging
License:	GPL 3.0
URL:		http://graylog2.org/
Source0:	https://github.com/Graylog2/%{name}/releases/download/%{version}-%{release}/%{name}-%{version}-%{release}.tgz
Source1:	init.d-graylog2-web-interface
Source2:	sysconfig-graylog2-web-interface
Source3:	logrotate.d-graylog2-server
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarach

Requires:	chkconfig
Requires:       jre >= 1.6.0

%description

A front-end web interface for the Graylog2 syslog receiver. This package relies on the configured
REST interfaces of the graylog2-server package and requires almost no other configuration options. 

%prep
%setup -q


%build
true

%install
rm -rf %{buildroot}

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
%{__mkdir} -p %{buildroot}/opt/%{name}/conf
%{__mkdir} -p %{buildroot}/opt/%{name}/lib
%{__mkdir} -p %{buildroot}/opt/%{name}/share
%{__install} -p -m 644 conf/* %{buildroot}/opt/%{name}/conf
%{__install} -p -m 644 lib/*.jar %{buildroot}/opt/%{name}/lib
%{__install} -p -m 644 share/* %{buildroot}/opt/%{name}/share


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
%defattr(-,root,root,-)
%dir %{_sysconfdir}/rc.d/init.d
%dir %{_sysconfdir}/sysconfig
%{_sysconfdir}/rc.d/init.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_localstatedir}/log/%{name}
%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir /opt/%{name}
%dir /opt/%{name}/lib
%dir /opt/%{name}/share
%config(noreplace) /opt/%{name}/conf/*
/opt/%{name}/lib/*
/opt/%{name}/share/*


%changelog
* Sat Oct 5 2013 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-preview.1
- Initial SPEC file
