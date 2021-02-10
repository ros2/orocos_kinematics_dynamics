cmake_minimum_required(VERSION 3.5)
project(python_orocos_kdl)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(orocos_kdl)
include_directories(${orocos_kdl_INCLUDE_DIRS})
link_directories(${orocos_kdl_LIBRARY_DIRS})

find_package(python_cmake_module REQUIRED)
find_package(PythonExtra REQUIRED)
set(_PYTHON_EXECUTABLE "${PYTHON_EXECUTABLE}")
if(WIN32 AND CMAKE_BUILD_TYPE STREQUAL "Debug")
  set(PYTHON_EXECUTABLE "${PYTHON_EXECUTABLE_DEBUG}")
endif()

execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True, prefix=''))" OUTPUT_VARIABLE PYTHON_SITE_PACKAGES OUTPUT_STRIP_TRAILING_WHITESPACE)
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
find_package(SIP REQUIRED)
include(SIPMacros)

include_directories(${SIP_INCLUDE_DIR} ${PYTHON_INCLUDE_DIRS})

file(GLOB SIP_FILES "${CMAKE_CURRENT_SOURCE_DIR}/*.sip")
set(SIP_INCLUDES ${SIP_FILES})
set(SIP_EXTRA_OPTIONS "-o")
set(PYTHON_SITE_PACKAGES_INSTALL_DIR ${CMAKE_INSTALL_PREFIX}/${PYTHON_SITE_PACKAGES})
add_sip_python_module(PyKDL PyKDL/PyKDL.sip ${orocos_kdl_LIBRARIES})

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(frames_test tests/framestest.py PYTHON_EXECUTABLE "${PYTHON_EXECUTABLE}" APPEND_ENV PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR} TIMEOUT 60)
endif()

set(PYTHON_EXECUTABLE "${_PYTHON_EXECUTABLE}")


install(FILES package.xml DESTINATION share/python_orocos_kdl)

find_package(ament_cmake QUIET)
if(ament_cmake_FOUND)
  ament_environment_hooks(env-hooks/python_orocos_kdl_site_packages.bash.in)
  ament_environment_hooks(env-hooks/python_orocos_kdl_site_packages.tcsh.in)
  ament_environment_hooks(env-hooks/python_orocos_kdl_site_packages.sh.in)
  ament_environment_hooks(env-hooks/python_orocos_kdl_site_packages.zsh.in)
  ament_environment_hooks(env-hooks/python_orocos_kdl_site_packages.dsv.in)
  ament_package()
endif()
