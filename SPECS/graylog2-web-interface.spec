Name:		graylog2-web-interface
Version:	0.20.0
Release:	preview.4
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
%{__install} -p -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Logs and Run
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/graylog2
%{__mkdir} -p %{buildroot}%{_localstatedir}/run
%{__mkdir} -p %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install Root
%{__mkdir} -p %{buildroot}/opt/%{name}
%{__mkdir} -p %{buildroot}/opt/%{name}/conf
%{__mkdir} -p %{buildroot}/opt/%{name}/lib
%{__mkdir} -p %{buildroot}/opt/%{name}/share

%{__install} -p -m 644 conf/* %{buildroot}/opt/%{name}/conf
%{__install} -p -m 644 lib/*.jar %{buildroot}/opt/%{name}/lib

cp -pR share/ %{buildroot}/opt/%{name}/


%pre
# Create the graylog2 group
if ! getent group graylog2 > /dev/null
then
	groupadd -r graylog2
fi

# Create the graylog2 user
if ! getent passwd graylog2 > /dev/null
then
	useradd -r -g graylog2 -s /sbin/nologin graylog2
fi


%post
/sbin/chkconfig --add graylog2-web-interface


%preun
if [ $1 -eq 0 ]; then
  /sbin/service graylog2-web-interface stop >/dev/null 2>&1
  /sbin/chkconfig --del graylog2-web-interface
fi

# Remove the graylog2 user
if getent passwd graylog2 > /dev/null
then
	userdel graylog2
fi

# Remove the graylog2 group
if getent group graylog2 > /dev/null
then
	groupdel graylog2
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/rc.d/init.d
%dir %{_sysconfdir}/sysconfig
%{_sysconfdir}/rc.d/init.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_localstatedir}/run
%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%defattr(-,graylog2,graylog2,-)
%dir %{_localstatedir}/log/graylog2
%dir /opt/%{name}
%dir /opt/%{name}/lib
%dir /opt/%{name}/share
%config(noreplace) /opt/%{name}/conf/*
/opt/%{name}/lib/*
/opt/%{name}/share/*


%changelog
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
