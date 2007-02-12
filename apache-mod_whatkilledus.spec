%define		mod_name	whatkilledus
%define 	apxs		/usr/sbin/apxs
Summary:	Knows what a thread was handling in case the thread segfaults
Summary(pl.UTF-8):   Moduł wiedzący, co obsługiwał wątek w przypadku naruszenia ochrony pamięci
Name:		apache-mod_%{mod_name}
Version:	1.0
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://people.apache.org/~trawick/mod_whatkilledus.c
# Source0-md5:	e59c5d56e294a31e5b158ad5e4553001
URL:		http://people.apache.org/~trawick/exception_hook.html
BuildRequires:	apache-devel >= 2.0.43
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

%build
%{apxs} -c %{SOURCE0}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

libtool --mode=install install mod_%{mod_name}.la $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so

echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' \
	> $RPM_BUILD_ROOT/etc/httpd/httpd.conf/68_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*mod_*.conf
%attr(755,root,root) %{_pkglibdir}/*.so
