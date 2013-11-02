Name:		graylog2-server
Version:	0.20.0
Release:	preview.5
Summary:	A syslog receiver and processing system

Group:		Monitoring/Logging
License:	GPL 3.0
URL:		http://graylog2.org/
Source0:	https://github.com/Graylog2/%{name}/releases/download/%{version}-%{release}/%{name}-%{version}-%{release}.tgz
Source1:	init.d-graylog2-server
Source2:	sysconfig-graylog2-server
Source3:	logrotate.d-graylog2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	chkconfig
Requires:	jre >= 1.6.0

%description

A syslog processing system that stores received messages in an Elasticsearch database. When coupled with 
the graylog2-web-interface, which provides a front-end web interface, will allow for powerful message
analytics for a server network. 

Other information, including but not limited to user credentials, stream configurations, etc, are stored
in MongoDB


%prep
%setup -q -n %{name}-%{version}-%{release}


%build
true

%install
rm -rf %{buildroot}

# Config
%{__mkdir} -p %{buildroot}%{_sysconfdir}/
%{__install} -p -m 644 graylog2.conf.example %{buildroot}%{_sysconfdir}/graylog2.conf

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
%{__mkdir} -p %{buildroot}/opt/%{name}/plugin

%{__install} -p -m 644 graylog2-server.jar %{buildroot}/opt/%{name}/
cp -pR plugin/* %{buildroot}/opt/%{name}/plugin


%pre
# Create graylog2 group
if ! getent group graylog2 > /dev/null 
then
	groupadd -r graylog2
fi

# Create graylog2 user
if ! getent passwd graylog2 > /dev/null
then
	useradd -r -g graylog2 -s /sbin/nologin graylog2
fi


%post
/sbin/chkconfig --add graylog2-server


%preun
if [ $1 -eq 0 ]; then
  /sbin/service graylog2-server stop >/dev/null 2>&1
  /sbin/chkconfig --del graylog2-server
fi

# Remove graylog2 user
if getent passwd graylog2 > /dev/null
then
	userdel graylog2
fi

# Remove graylog2 group
if getent group graylog2 > /dev/null
then
	groupdel graylog2
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/
%config(noreplace) %{_sysconfdir}/graylog2.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_localstatedir}/run
%dir %{_sysconfdir}/logrotate.d
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/rc.d/init.d/%{name}
%defattr(-,graylog2,graylog2,-)
%dir %{_localstatedir}/log/graylog2
%dir /opt/%{name}
%dir /opt/%{name}/plugin
/opt/%{name}/graylog2-server.jar
/opt/%{name}/plugin/*


%changelog
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
