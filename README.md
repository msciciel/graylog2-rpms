graylog2-rpms
=============

h2. An easy way to install the graylog2-server and graylog2-web-interface packages on Fedora/RHEL based systems

These RPM SPEC files were built to provide an easy way to install the graylog2-server and graylog2-web-interface
packages in a systemic way.

h2. These packages are made for version 0.20.0-preview.1 and higher of both packages, these SPEC files WILL NOT WORK with previous versions

h2. These package have been by ONLY me, use at your own risk.

To build the rpm for your system of choice:

* Check out this repo
* Create your rpmbuild directory
<pre>rpmdev-setuptree</pre>
* Sym link all the sources and spec files into your build tree
<pre>
 cd rpmbuild
 ln -s ${repo}/SPECS/* SPECS/
 ln -s ${repo}/SOURCES/* SOURCES/
</pre>
* Download all the source files
<pre>spectool -g SPECS/graylog2-server.spec </pre>
<pre>spectool -g SPECS/graylog2-web-interface.spec </pre>
* Build the src rpm
<pre>rpmbuild -ba SPECS/graylog2-server.spec </pre>
<pre>rpmbuild -ba SPECS/graylog2-web-interface.spec </pre>
** If you are building for an older system such as el5 you will need to use the old method of hashing
<pre>rpmbuild-md5 -ba SPECS/graylog2-server.spec </pre>
<pre>rpmbuild-md5 -ba SPECS/graylog2-web-interface.spec </pre>
* Install into your repo!
