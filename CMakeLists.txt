CMAKE_MINIMUM_REQUIRED(VERSION 3.1)

# name of the project is VISION
PROJECT(helen)
set (CMAKE_CXX_FLAGS "-fPIC -O3")
set (CMAKE_C_FLAGS "-fPIC -O3")

SET(CMAKE_CXX_STANDARD 11)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)

FIND_PACKAGE(PythonInterp 3 REQUIRED)
FIND_PACKAGE(PythonLibs 3 REQUIRED)

if (PYTHONINTERP_FOUND)
    message("Python found")
else()
    message("Python not found")
endif()

# enable installing dependencies
option(INSTALL_DEPENDENCIES
        "Install project dependencies"
        ON)

INCLUDE(modules/pybind11.cmake)

# pybind11 to interface
pybind11_add_module(HELEN ${CMAKE_CURRENT_SOURCE_DIR}/modules/src/pybind_api.cpp)

