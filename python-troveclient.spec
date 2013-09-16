Name:           python-troveclient
Version:        0.1.4
Release:        2%{?dist}
Summary:        Client library for OpenStack DBaaS API

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 0.5.20
BuildRequires:  python-sphinx
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

# strip /usr/bin/env from script
sed -i '1d' troveclient/cli.py
sed -i '1d' troveclient/mcli.py

# generate html docs 
sphinx-build docs/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# currently disabling tests
# see buildrequires
#%check
#%{__python2} setup.py test


%files
%doc html README.rst LICENSE
%{python2_sitelib}/python_troveclient-%{version}-py?.?.egg-info
%{python2_sitelib}/troveclient
%{_bindir}/trove-cli
%{_bindir}/trove-mgmt-cli

%changelog
* Thu Sep 12 2013 Matthias Runge <mrunge@redhat.com> - 0.1.4-2
- change {__python} to {__python2}

* Thu Sep 12 2013 Matthias Runge <mrunge@redhat.com> - 0.1.4-1
- Initial package.
