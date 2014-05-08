Name:           python-troveclient
Version:        1.0.3
Release:        2%{?dist}
Summary:        Client library for OpenStack DBaaS API

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Patch0:         python-troveclient-remove-pbr-dep.patch
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 0.5.20
%if 0%{?rhel} == 6
BuildRequires:  python-sphinx10
%else 
BuildRequires: python-sphinx
%endif

BuildRequires:  python-setuptools

# required for tests
# tests currently disabled due missing deps
#BuildRequires:  python-pep8
#BuildRequires:  pyflakes
# currently under review
# https://bugzilla.redhat.com/show_bug.cgi?id=839056
# BuildRequires:  python-flake8

# Currently under review
# https://bugzilla.redhat.com/show_bug.cgi?id=958007
# BuildRequires:  python-hacking
#BuildRequires: python-mock
#BuildRequires: python-testtools
#BuildRequires: python-testrepository

%description
This is a client for the Trove API. There's a Python API (the
troveclient module), and a command-line script (trove). Each
implements 100% (or less ;) ) of the Trove API.

%prep
%setup -q -n %{name}-%{version}
# Remove bundled egg-info
rm -rf %{name}.egg-info

# remove pbr runtime dependency
%patch0 
sed -i s/RPMVERSION/%{version}/ troveclient/__init__.py

# generate html docs 
%if 0%{?rhel} == 6
sphinx-1.0-build docs/source html
%else
sphinx-build docs/source html
%endif

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%if 0%{?rhel} == 6
%{__python} setup.py build
%else
%{__python2} setup.py build
%endif


%install
%if 0%{?rhel} == 6
%{__python} setup.py install --skip-build --root %{buildroot}
%else
%{__python2} setup.py install --skip-build --root %{buildroot}
%endif

# currently disabling tests
# see buildrequires
#%check
#%{__python2} setup.py test


%files
%doc html README.rst LICENSE
%if 0%{?rhel} == 6
%{python_sitelib}/python_troveclient-%{version}-py?.?.egg-info
%{python_sitelib}/troveclient
%else
%{python2_sitelib}/python_troveclient-%{version}-py?.?.egg-info
%{python2_sitelib}/troveclient
%endif
%{_bindir}/trove

%changelog
* Thu May 08 2014 Matthias Runge <mrunge@redhat.com> - 1.0.3-2
- remove runtime dep to pbr

* Fri Dec 06 2013 Matthias Runge <mrunge@redhat.com> - 1.0.3-1
- upgrade to 1.0.3

* Tue Sep 17 2013 Matthias Runge <mrunge@redhat.com> - 0.1.4-3
- also build on EPEL6

* Thu Sep 12 2013 Matthias Runge <mrunge@redhat.com> - 0.1.4-2
- change {__python} to {__python2}

* Thu Sep 12 2013 Matthias Runge <mrunge@redhat.com> - 0.1.4-1
- Initial package.
