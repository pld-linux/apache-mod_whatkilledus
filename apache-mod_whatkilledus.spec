%define		mod_name	whatkilledus
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: knows what a thread was handling in case the thread segfaults
Summary(pl.UTF-8):	Moduł apache wiedzący, co obsługiwał wątek w przypadku naruszenia ochrony pamięci
Name:		apache-mod_%{mod_name}
Version:	1.0
Release:	1.20040323.1
License:	Apache v2.0
Group:		Networking/Daemons
Source0:	http://people.apache.org/~trawick/mod_whatkilledus.c
# Source0-md5:	e59c5d56e294a31e5b158ad5e4553001
Source1:	http://mirrors.ludost.net/gentoo-portage/www-apache/mod_whatkilledus/files/gen_test_char.c
# Source1-md5:	7c4e734d1afc695a5be53581998f3700
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Keeps a little bit of state on each active connection, which allows it
to know what a thread was handling in case the thread segfaults.

%description -l pl.UTF-8
Moduł przechowujący wybrane informacje o stanie każdego aktywnego
połączenia, pozwalające dowiedzieć się, co obsługiwał wątek w
sytuacji, kiedy spowodował naruszenie ochrony pamięci.

%prep
%setup -q -c -T
install %{SOURCE0} .

%build
%{__cc} `%{_bindir}/apr-1-config --includes --cppflags` %{SOURCE1} -o gen_test_char
./gen_test_char > test_char.h
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf,/var/log/httpd}
install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

touch $RPM_BUILD_ROOT/var/log/httpd/whatkilledus_log

cat > $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/68_mod_%{mod_name}.conf << 'EOF'
LoadModule %{mod_name}_module modules/mod_%{mod_name}.so
EnableExceptionHook On
WhatKilledUsLog /var/log/httpd/whatkilledus_log
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart
touch /var/log/httpd/whatkilledus_log && chown root:http /var/log/httpd/whatkilledus_log && chmod 620 /var/log/httpd/whatkilledus_log

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
# append by webserver
%attr(620,root,http) %ghost /var/log/httpd/whatkilledus_log
