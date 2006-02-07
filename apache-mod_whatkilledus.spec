%define		mod_name	whatkilledus
%define 	apxs		/usr/sbin/apxs
Summary:	Knows what a thread was handling in case the thread segfaults
Name:		apache-mod_%{mod_name}
Version:	1.0
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://people.apache.org/~trawick/mod_whatkilledus.c
# Source0-md5:	e59c5d56e294a31e5b158ad5e4553001
URL:		http://people.apache.org/~trawick/exception_hook.html
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.43
BuildRequires:	rpm-perlprov
Requires(post,preun):	%{apxs}
Requires:	apache >= 2.0.43
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)

%description
Keeps a little bit of state on each active connection, which allows it
to know what a thread was handling in case the thread segfaults.

%prep
%setup -q -c -T

%build
%{apxs} -c %{SOURCE0}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/httpd/httpd.conf

libtool --mode=install install -D mod_%{mod_name}.la $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so

echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > $RPM_BUILD_ROOT/etc/httpd/httpd.conf/68_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache HTTP daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*.so
%config %{_sysconfdir}/httpd.conf/*.conf
