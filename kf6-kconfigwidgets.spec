#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.5
%define		qtver		5.15.2
%define		kfname		kconfigwidgets

Summary:	Widgets for configuration dialogs
Name:		kf6-%{kfname}
Version:	6.5.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	3da8c7755a7207ce332775f7bea879a9
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kauth-devel >= %{version}
BuildRequires:	kf6-kcodecs-devel >= %{version}
BuildRequires:	kf6-kcolorscheme-devel >= %{version}
BuildRequires:	kf6-kconfig-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-kdoctools-devel >= %{version}
BuildRequires:	kf6-kguiaddons-devel >= %{version}
BuildRequires:	kf6-ki18n-devel >= %{version}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-kauth >= %{version}
Requires:	kf6-kcodecs >= %{version}
Requires:	kf6-kcolorscheme >= %{version}
Requires:	kf6-kconfig >= %{version}
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-kguiaddons >= %{version}
Requires:	kf6-ki18n >= %{version}
Requires:	kf6-kwidgetsaddons >= %{version}
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KConfigWidgets provides easy-to-use classes to create configuration
dialogs, as well as a set of widgets which uses KConfig to store their
settings.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cmake >= 3.16
Requires:	kf6-kauth-devel >= %{version}
Requires:	kf6-kcodecs-devel >= %{version}
Requires:	kf6-kcolorscheme-devel >= %{version}
Requires:	kf6-kconfig-devel >= %{version}
Requires:	kf6-kwidgetsaddons-devel >= %{version}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6ConfigWidgets.so.6
%attr(755,root,root) %{_libdir}/libKF6ConfigWidgets.so.*.*
%{_datadir}/qlogging-categories6/kconfigwidgets.categories
%attr(755,root,root) %{qt6dir}/plugins/designer/kconfigwidgets6widgets.so
%{_datadir}/qlogging-categories6/kconfigwidgets.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KConfigWidgets
%{_libdir}/cmake/KF6ConfigWidgets
%{_libdir}/libKF6ConfigWidgets.so
