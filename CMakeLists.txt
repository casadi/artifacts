cmake_minimum_required(VERSION 2.8.6)

project(casadi C CXX)

set(SWIG_EXPORT OFF)

# Workaround for OS X
if(APPLE)
  if(WITH_PYTHON3)
  set(PYTHON_CONFIG_NAME python3-config)
  else()
  set(PYTHON_CONFIG_NAME python-config)
  endif()
  find_program(PYTHON_CONFIG_EXECUTABLE
               NAMES ${PYTHON_CONFIG_NAME} DOC "python-config executable")
  if(PYTHON_CONFIG_EXECUTABLE)
    execute_process(COMMAND ${PYTHON_CONFIG_EXECUTABLE} --prefix
                    OUTPUT_VARIABLE PYTHON_PREFIX_STRING
                    RESULT_VARIABLE PYTHON_PREFIX_FAILED
                    ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)
    if(NOT PYTHON_PREFIX_FAILED)
      file(GLOB LOCAL_PYTHON_NAME RELATIVE ${PYTHON_PREFIX_STRING}/lib "${PYTHON_PREFIX_STRING}/lib/python*.*")
      find_library(PYTHON_LIBRARY NAMES ${LOCAL_PYTHON_NAME}
        PATHS ${PYTHON_PREFIX_STRING}/lib NO_DEFAULT_PATH)
      file(GLOB LOCAL_PYTHON_NAME "${PYTHON_PREFIX_STRING}/include/python*")
      find_path(PYTHON_INCLUDE_DIR
        NAMES Python.h
        PATHS ${LOCAL_PYTHON_NAME} NO_DEFAULT_PATH)
    endif()
    message(STATUS ${PYTHON_INCLUDE_DIR})
  endif()
endif()

function(CasadiGetPythonVersionMajor VERSION_MAJOR_RESULT INCLUDE_PATH)
  set(MATCH_STRING "#define[ \t]+PY_MAJOR_VERSION[ \t]+([0-9]+)")
  file(STRINGS "${INCLUDE_PATH}/patchlevel.h" PY_MAJOR_VERSION REGEX ${MATCH_STRING})
  string(REGEX REPLACE "${MATCH_STRING}" "\\1" PYTHON_VERSION_MAJOR "${PY_MAJOR_VERSION}")
  set(${VERSION_MAJOR_RESULT} ${PYTHON_VERSION_MAJOR} PARENT_SCOPE)
endfunction()

if(SWIG_EXPORT)
  if(WITH_PYTHON3)
    set(PYTHON_VERSION_MAJOR 3)
  else()
    set(PYTHON_VERSION_MAJOR 2)
  endif()
else()
  if(PYTHON_INCLUDE_DIR)
    set(PYTHON_INCLUDE_PATH ${PYTHON_INCLUDE_DIR})
  else()
    # Find packages
    if(WITH_PYTHON3)
    set(MINPYVERSION "3")
    else()
    set(MINPYVERSION "")
    endif()

    # We don't really need the libs, but the headers.
    find_package(PythonLibs ${MINPYVERSION})
    if(NOT PYTHON_INCLUDE_PATH)
      message(SEND_ERROR "Python include headers not found, but required." )
    endif()
  endif()
  
  CasadiGetPythonVersionMajor(PYTHON_VERSION_MAJOR "${PYTHON_INCLUDE_PATH}")
  include_directories(${PYTHON_INCLUDE_PATH})
endif()

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
