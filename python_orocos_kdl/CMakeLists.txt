cmake_minimum_required(VERSION 3.5)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

project(python_orocos_kdl)

find_package(ament_cmake REQUIRED)
find_package(orocos_kdl REQUIRED)

include_directories(${orocos_kdl_INCLUDE_DIRS})
link_directories(${orocos_kdl_LIBRARY_DIRS})

set(PYTHON_VERSION 3.5 CACHE STRING "Python Version")
find_package(PythonInterp ${PYTHON_VERSION} REQUIRED)
find_package(PythonLibs ${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR} REQUIRED)
execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True, prefix=''))" OUTPUT_VARIABLE PYTHON_SITE_PACKAGES OUTPUT_STRIP_TRAILING_WHITESPACE)
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
find_package(SIP REQUIRED)
include(SIPMacros)

include_directories(${SIP_INCLUDE_DIR} ${PYTHON_INCLUDE_DIRS})

file(GLOB SIP_FILES "${CMAKE_CURRENT_SOURCE_DIR}/*.sip")
set(SIP_INCLUDES ${SIP_FILES})
set(SIP_EXTRA_OPTIONS "-o")
set(PYTHON_INSTALL_DIR ${PYTHON_SITE_PACKAGES})
add_sip_python_module(PyKDL PyKDL/PyKDL.sip ${orocos_kdl_LIBRARIES})

# Manually trigger adding install directory to $PYTHONPATH - until ament supports SIP packages or a better solution is found
configure_file(
  "cmake/pythonpath_hook.sh.in"
  "cmake/pythonpath_hook.sh"
  @ONLY
)
ament_environment_hooks(
  ${CMAKE_CURRENT_BINARY_DIR}/cmake/pythonpath_hook.sh
)

# python_module_PyKDL is target name created by add_sip_python_module()
install(
  TARGETS python_module_PyKDL
  DESTINATION "${CMAKE_INSTALL_PREFIX}/${PYTHON_INSTALL_DIR}"
)

install(
  FILES package.xml
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)

  ament_add_pytest_test(
    Frames
    tests/framestest.py
    APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}
  )
  ament_add_pytest_test(
    FrameVel
    tests/frameveltest.py
    APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}
  )
  ament_add_pytest_test(
    KinematicFamily
    tests/framestest.py
    APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}
  )
endif()

ament_package()
