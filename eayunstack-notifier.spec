Name:            eayunstack-notifier		
Version:         1.0	
Release:         2%{?dist}
Summary:         Eayunstack Notifier	

Group:           Application	
License:         GPL	
URL:             http://gitlab.eayun.com:9000/eayunstack/eayunstack-notifier/
Source0:         eayunstack-notifier-%{version}.tar.gz 	

BuildRequires:  /bin/bash 
BuildRequires:  python
BuildRequires:  python2-devel	
BuildRequires:  python-setuptools	
BuildRequires:  systemd
Requires:       python	
Requires:       python-ceilometer

%description
EayunStack Notifier Tool

%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build


%install
rm -rf %{buildroot}
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/etc/eayunstack-notifier/
install -p -D -m 644 etc/eayunstack-notifier/eayunstack-notifier.conf %{buildroot}%{_sysconfdir}/eayunstack-notifier/eayunstack-notifier.conf
install -p -D -m 644 etc/eayunstack-notifier/event_definitions.yaml %{buildroot}%{_sysconfdir}/eayunstack-notifier/event_definitions.yaml
install -p -D -m 755 etc/eayunstack-notifier/eayunstack-notifier.service %{buildroot}%{_unitdir}/eayunstack-notifier.service
install -p -D -m 644 etc/eayunstack-notifier/eayunstack-notifier %{buildroot}%{_sysconfdir}/logrotate.d/eayunstack-notifier


%files
%doc
%attr(0755,root,root)/etc/eayunstack-notifier
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/eayunstack-notifier/eayunstack-notifier.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/eayunstack-notifier/event_definitions.yaml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/eayunstack-notifier
%{_unitdir}/eayunstack-notifier.service
/usr/bin/eayunstack-notifier
/usr/lib/python2.7/site-packages/


%changelog
* Thu Nov 23 2017 Armstrong Liu <vpbvmw651078@gmail.com> 1.0-2
- commit fb40b5d2971f2498181fba5a66e73829a070986d

* Mon Jul 17 2017 dwong <peng.wang@eayun.com> 1.0-1
- commit 990b457369b7715012f5f1dece79c3fee0c0e40c
