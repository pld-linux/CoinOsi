# TODO: Cplex, Mosek, Xpress, Gurobi solvers (commercial)
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_with	soplex		# Soplex solver support (academic use or commercial)
#
Summary:	COIN-OR Osi - Open Solver Interface library
Summary(pl.UTF-8):	COIN-OR Osi (Open Solver Interface) - interfejs do rozwiązywania problemów matematycznych
Name:		CoinOsi
Version:	0.106.10
Release:	1
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://www.coin-or.org/download/source/Osi/Osi-%{version}.tgz
# Source0-md5:	1a3d67fe4c9948286269e92a85c63b79
Patch0:		Osi-glpk.patch
Patch1:		Osi-destdir.patch
Patch2:		Osi-link.patch
URL:		https://projects.coin-or.org/Osi
BuildRequires:	CoinUtils-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	glpk-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
%{?with_soplex:BuildRequires:	soplex-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The COIN-OR Open Solver Interface library is a collection of solver
interfaces (SIs) that provide a common interface - the OSI API - for
all the supported solvers.

%description -l pl.UTF-8
Biblioteka COIN-OR Open Solver Interface to zbiór interfejsów do
bibliotek rozwiązujących problemy matematyczne (Solver Interface)
udostępniających wspólny interfejs (API OSI) dla wszystkich
obsługiwanych bibliotek.

%package devel
Summary:	Header files for COIN-OR Osi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki COIN-OR Osi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	CoinUtils-devel

%description devel
Header files for COIN-OR Osi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki COIN-OR Osi.

%package static
Summary:	Static COIN-OR Osi library
Summary(pl.UTF-8):	Statyczna biblioteka COIN-OR Osi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static COIN-OR Osi library.

%description static -l pl.UTF-8
Statyczna biblioteka COIN-OR Osi.

%package apidocs
Summary:	COIN-OR Osi API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki COIN-OR Osi
Group:		Documentation

%description apidocs
API documentation for COIN-OR Osi library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki COIN-OR Osi.

%package glpk
Summary:	COIN-OR Open Solver Interface for GLPK
Summary(pl.UTF-8):	Biblioteka COIN-OR Open Solver Interface dla GLPK
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description glpk
COIN-OR Open Solver Interface for GLPK solver.

%description glpk -l pl.UTF-8
Biblioteka COIN-OR Open Solver Interface dla biblioteki rozwiązującej
GLPK.

%package glpk-devel
Summary:	Development files for COIN-OR OsiGlpk library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki COIN-OR OsiGlpk
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-glpk = %{version}-%{release}
Requires:	glpk-devel

%description glpk-devel
Development files for COIN-OR OsiGlpk library.

%description glpk-devel -l pl.UTF-8
Pliki programistyczne biblioteki COIN-OR OsiGlpk.

%package glpk-static
Summary:	Static COIN-OR OsiGlpk library
Summary(pl.UTF-8):	Statyczna biblioteka COIN-OR OsiGlpk
Group:		Development/Libraries
Requires:	%{name}-glpk-devel = %{version}-%{release}

%description glpk-static
Static COIN-OR OsiGlpk library.

%description glpk-static -l pl.UTF-8
Statyczna biblioteka COIN-OR OsiGlpk.

%package soplex
Summary:	COIN-OR Open Solver Interface for Soplex
Summary(pl.UTF-8):	Biblioteka COIN-OR Open Solver Interface dla biblioteki Soplex
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description soplex
COIN-OR Open Solver Interface for Soplex solver.

%description soplex -l pl.UTF-8
Biblioteka COIN-OR Open Solver Interface dla biblioteki rozwiązującej
Soplex.

%package soplex-devel
Summary:	Development files for COIN-OR OsiSpx library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki COIN-OR OsiSpx
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-soplex = %{version}-%{release}
Requires:	soplex-devel

%description soplex-devel
Development files for COIN-OR OsiSpx library.

%description soplex-devel -l pl.UTF-8
Pliki programistyczne biblioteki COIN-OR OsiSpx.

%package soplex-static
Summary:	Static COIN-OR OsiSpx library
Summary(pl.UTF-8):	Statyczna biblioteka COIN-OR OsiSpx
Group:		Development/Libraries
Requires:	%{name}-soplex-devel = %{version}-%{release}

%description soplex-static
Static COIN-OR OsiGlpk library.

%description soplex-static -l pl.UTF-8
Statyczna biblioteka COIN-OR OsiGlpk.

%prep
%setup -q -n Osi-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

ln -s ../BuildTools Osi/BuildTools

%build
cd Osi
%{__libtoolize}
%{__aclocal} -I BuildTools
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%configure \
	--enable-dependency-linking \
	%{?with_static_libs:--enable-static} \
	--with-coinutils-lib="-lCoinUtils" \
	--with-coinutils-incdir="/usr/include/coin" \
	--with-glpk-lib="-lglpk" \
	--with-netlib-datadir="/usr/share/coin/Data/Netlib" \
	--with-sample-datadir="/usr/share/coin/Data/Sample" \
	%{?with_soplex:--with-soplex-lib="-lsoplex" --with-soplex-incdir="/usr/include/soplex"}

%{__make}

%if %{with apidocs}
%{__make} doxydoc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libOsi*.la
# packages as %doc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/coin/doc/Osi/{AUTHORS,LICENSE,README}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Osi/{AUTHORS,CHANGELOG,LICENSE,README}
%attr(755,root,root) %{_libdir}/libOsi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOsi.so.1
%attr(755,root,root) %{_libdir}/libOsiCommonTests.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOsiCommonTests.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOsi.so
%attr(755,root,root) %{_libdir}/libOsiCommonTests.so
%{_includedir}/coin/OsiConfig.h
%{_includedir}/coin/OsiAuxInfo.hpp
%{_includedir}/coin/OsiBranchingObject.hpp
%{_includedir}/coin/OsiChooseVariable.hpp
%{_includedir}/coin/OsiColCut.hpp
%{_includedir}/coin/OsiCollections.hpp
%{_includedir}/coin/OsiCut.hpp
%{_includedir}/coin/OsiCuts.hpp
%{_includedir}/coin/OsiPresolve.hpp
%{_includedir}/coin/OsiRowCut.hpp
%{_includedir}/coin/OsiRowCutDebugger.hpp
%{_includedir}/coin/OsiSolverBranch.hpp
%{_includedir}/coin/OsiSolverInterface.hpp
%{_includedir}/coin/OsiSolverParameters.hpp
%{_includedir}/coin/OsiUnitTests.hpp
%{_pkgconfigdir}/osi.pc
%{_pkgconfigdir}/osi-unittests.pc
%dir %{_datadir}/coin/doc/Osi
%{_datadir}/coin/doc/Osi/osi_addlibs.txt

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libOsi.a
%{_libdir}/libOsiCommonTests.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxydoc/html/*
%endif

%files glpk
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOsiGlpk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOsiGlpk.so.1

%files glpk-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOsiGlpk.so
%{_includedir}/coin/OsiGlpkSolverInterface.hpp
%{_pkgconfigdir}/osi-glpk.pc

%files glpk-static
%defattr(644,root,root,755)
%{_libdir}/libOsiGlpk.a

%if %{with soplex}
%files soplex
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOsiSpx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOsiSpx.so.1

%files soplex-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOsiSpx.so
%{_includedir}/coin/OsiSpxSolverInterface.hpp
%{_pkgconfigdir}/osi-soplex.pc

%files soplex-static
%defattr(644,root,root,755)
%{_libdir}/libOsiSpx.a
%endif
