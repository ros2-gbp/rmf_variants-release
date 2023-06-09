%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-rmf-dev
Version:        0.0.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS rmf_dev package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-humble-ament-cmake-catch2
Requires:       ros-humble-menge-vendor
Requires:       ros-humble-nlohmann-json-schema-validator-vendor
Requires:       ros-humble-pybind11-json-vendor
Requires:       ros-humble-rmf-api-msgs
Requires:       ros-humble-rmf-battery
Requires:       ros-humble-rmf-building-map-msgs
Requires:       ros-humble-rmf-building-map-tools
Requires:       ros-humble-rmf-building-sim-common
Requires:       ros-humble-rmf-building-sim-gz-classic-plugins
Requires:       ros-humble-rmf-building-sim-gz-plugins
Requires:       ros-humble-rmf-charger-msgs
Requires:       ros-humble-rmf-dispenser-msgs
Requires:       ros-humble-rmf-door-msgs
Requires:       ros-humble-rmf-fleet-adapter
Requires:       ros-humble-rmf-fleet-adapter-python
Requires:       ros-humble-rmf-fleet-msgs
Requires:       ros-humble-rmf-ingestor-msgs
Requires:       ros-humble-rmf-lift-msgs
Requires:       ros-humble-rmf-obstacle-msgs
Requires:       ros-humble-rmf-robot-sim-common
Requires:       ros-humble-rmf-robot-sim-gz-classic-plugins
Requires:       ros-humble-rmf-robot-sim-gz-plugins
Requires:       ros-humble-rmf-scheduler-msgs
Requires:       ros-humble-rmf-site-map-msgs
Requires:       ros-humble-rmf-task
Requires:       ros-humble-rmf-task-msgs
Requires:       ros-humble-rmf-task-ros2
Requires:       ros-humble-rmf-task-sequence
Requires:       ros-humble-rmf-traffic
Requires:       ros-humble-rmf-traffic-editor
Requires:       ros-humble-rmf-traffic-editor-assets
Requires:       ros-humble-rmf-traffic-editor-test-maps
Requires:       ros-humble-rmf-traffic-examples
Requires:       ros-humble-rmf-traffic-msgs
Requires:       ros-humble-rmf-traffic-ros2
Requires:       ros-humble-rmf-utils
Requires:       ros-humble-rmf-visualization
Requires:       ros-humble-rmf-visualization-building-systems
Requires:       ros-humble-rmf-visualization-fleet-states
Requires:       ros-humble-rmf-visualization-floorplans
Requires:       ros-humble-rmf-visualization-msgs
Requires:       ros-humble-rmf-visualization-navgraphs
Requires:       ros-humble-rmf-visualization-obstacles
Requires:       ros-humble-rmf-visualization-rviz2-plugins
Requires:       ros-humble-rmf-visualization-schedule
Requires:       ros-humble-rmf-websocket
Requires:       ros-humble-rmf-workcell-msgs
Requires:       ros-humble-ros-workspace
BuildRequires:  ros-humble-ament-cmake
BuildRequires:  ros-humble-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
A package to aggregate the packages required for a minimal installation of Open-
RMF

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DAMENT_PREFIX_PATH="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Fri Jun 09 2023 Yadunund <yadunund@openrobotics.org> - 0.0.1-1
- Autogenerated by Bloom

