# Findkaldi_native_io
# -------------------
#
# Finds the kaldi_native_io library
#
# This will define the following variables:
#
#   KALDI_NATIVE_IO_FOUND        -- True if the system has the kaldi_native_io library
#   KALDI_NATIVE_IO_INCLUDE_DIRS -- The include directories for kaldi_native_io
#   KALDI_NATIVE_IO_LIBRARIES    -- Libraries to link against
#   KALDI_NATIVE_IO_CXX_FLAGS    -- Additional (required) compiler flags
#   KALDI_NATIVE_IO_VERSION      -- The version of kaldi_native_io
#
# and the following imported targets:
#
#   kaldi_native_io_core

# This file is modified from pytorch/cmake/TorchConfig.cmake.in

set(KALDI_NATIVE_IO_CXX_FLAGS "")
set(KALDI_NATIVE_IO_VERSION 1.22.1)

if(DEFINED ENV{KALDI_NATIVE_IO_INSTALL_PREFIX})
  set(KALDI_NATIVE_IO_INSTALL_PREFIX $ENV{KALDI_NATIVE_IO_INSTALL_PREFIX})
else()
  # Assume we are in <install-prefix>/share/cmake/kaldi_native_io/kaldi_native_ioConfig.cmake
  get_filename_component(CMAKE_CURRENT_LIST_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
  get_filename_component(KALDI_NATIVE_IO_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)
endif()

set(KALDI_NATIVE_IO_INCLUDE_DIRS ${KALDI_NATIVE_IO_INSTALL_PREFIX}/include)

set(KALDI_NATIVE_IO_LIBRARIES kaldi_native_io_core)

foreach(lib IN LISTS KALDI_NATIVE_IO_LIBRARIES)
  find_library(location_${lib} ${lib}
    PATHS
    "${KALDI_NATIVE_IO_INSTALL_PREFIX}/lib"
    "${KALDI_NATIVE_IO_INSTALL_PREFIX}/lib64"
  )

  if(NOT MSVC)
    add_library(${lib} SHARED IMPORTED)
  else()
    add_library(${lib} STATIC IMPORTED)
  endif()

  set_target_properties(${lib} PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${KALDI_NATIVE_IO_INCLUDE_DIRS}"
      IMPORTED_LOCATION "${location_${lib}}"
      CXX_STANDARD 14
  )

  set_property(TARGET ${lib} PROPERTY INTERFACE_COMPILE_OPTIONS )
endforeach()

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(kaldi_native_io DEFAULT_MSG
  location_kaldi_native_io_core
)
