Name:		graylog2-radio
Version:	0.20.5
Release:	0.5.BETA
Summary:	A message receiver front-end to expand on a graylog2 network.

Group:		Monitoring/Logging
License:	GPL 3.0
URL:		http://graylog2.org/
Source0:	https://github.com/Graylog2/graylog2-server/releases/download/%{version}/%{name}-%{version}.tgz
Source1:	init.d-%{name}
Source2:	sysconfig-%{name}
Source3:	log4j-%{name}.xml
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	chkconfig
Requires:	libxml2
Requires:	jre >= 1.7.0

%description

The graylog2-radio package is an expasion package in the Graylog2 family of 
packages. It works by accepting messages from inputs, converting them into 
an internal Graylog2 message format and writes them to a Kafka cluster. 
From there one or more graylog2-server nodes can process the messages, run
all extractors and/or converters and write them to configured output(s).

This package is optional, but can be useful if your environments endure
exteremly high message throughput rates. Having radio nodes may significantly
reduce the load on your graylog2-server node(s)


%prep
%setup -q -n %{name}-%{version}


%build
true

%install
rm -rf %{buildroot}

# Config
%{__mkdir} -p %{buildroot}%{_sysconfdir}/graylog2/radio
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p graylog2-radio.conf.example %{buildroot}%{_sysconfdir}/graylog2/radio/radio.conf
%{__install} -p %{SOURCE3} %{buildroot}%{_sysconfdir}/graylog2/radio/log4j.xml
%{__install} -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# INIT scripts
%{__mkdir} -p %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -p -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}

# Logs and Run
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/graylog2
%{__mkdir} -p %{buildroot}%{_localstatedir}/run/graylog2

# Install Root
%{__mkdir} -p %{buildroot}/opt/%{name}
%{__install} -p -m 644 graylog2-radio.jar %{buildroot}/opt/%{name}/


%post
/sbin/chkconfig --add graylog2-radio


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
%config(noreplace) %{_sysconfdir}/graylog2/radio/*

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

* Sat Mar 29 2014 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-2
- Waiting for clean shutdown in init script stop function before continuing
- See https://github.com/Graylog2/graylog2-server/commits/020 for full changelog

* Sat Jan 18 2014 Corey Hammerton <corey.hammerton@gmail.com> 0.20.0-rc.1
- See https://github.com/Graylog2/graylog2-server/commits/020 for full changelog
- Initial SPEC file
