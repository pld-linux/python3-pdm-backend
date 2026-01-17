#
# Conditional build:
%bcond_with	doc	# API documentation (not in sdist)
%bcond_without	tests	# unit tests

%define		module	template
Summary:	The build backend used by PDM that supports latest packaging standards
Summary(pl.UTF-8):	Używany przez PDM backend budowania obsługujący najnowsze standardy pakietowania
Name:		python3-pdm-backend
Version:	2.4.6
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pdm-backend/
Source0:	https://files.pythonhosted.org/packages/source/p/pdm-backend/pdm_backend-%{version}.tar.gz
# Source0-md5:	63dd231ba6206cc834b205694208df40
URL:		https://pypi.org/project/pdm-backend/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
%if %{with tests}
%if "%{py3_ver}" == "3.9"
BuildRequires:	python3-importlib_metadata >= 3.6
%endif
BuildRequires:	python3-pytest
# optional?
#BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-gitconfig
#BuildRequires:	python3-pytest-xdist
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-mkdocs >= 1.4.2
BuildRequires:	python3-mkdocs-material >= 8.5.10
BuildRequires:	python3-mkdocs-version-annotations >= 1.0.0
# mkdocstrings[python]
BuildRequires:	python3-mkdocstrings >= 0.19.0
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the backend for PDM projects that is fully-compatible with PEP
517 spec, but you can also use it alone. It reads the metadata of PEP 621
format and converts it to Core metadata
(<https://packaging.python.org/specifications/core-metadata/>).

%description -l pl.UTF-8
Ten moduł jest backendem dla projektów PDM, w pełni zgodnym ze
specyfikacją PEP 517, ale może być używany samodzielnie. Odczytuje
metadane w formacie PEP 621 i konwertuje do formatu Core metadata
(<https://packaging.python.org/specifications/core-metadata/>).

%prep
%setup -q -n pdm_backend-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%dir %{py3_sitescriptdir}/pdm
%{py3_sitescriptdir}/pdm/backend
%{py3_sitescriptdir}/pdm_backend-%{version}.dist-info
