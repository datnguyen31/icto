cmake_minimum_required(VERSION 3.5.0)
project(module_sample)

# Set output directories
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/modules/sample/lib)

# Add include directories
include_directories(sample_inc
                    mission/sample_version.hpp
                    platform/sample_msgids.hpp
                    platform/sample_platform.hpp
                    src/sample_module.hpp
)

# Add source files
set(sample_src
    src/sample_module.cpp
)

# Add library target
add_library(module_sample SHARED ${sample_src})