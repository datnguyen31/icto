cmake_minimum_required(VERSION 3.5.0)
project(module_marry)

# Set output directories
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/modules/marry/lib)

include_directories(${PLATFORM_SERVICE_PATH}
                    ${CMAKE_CURRENT_SOURCE_DIR}/mission
                    ${CMAKE_CURRENT_SOURCE_DIR}/platform
                    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Add source files
set(marry_src
    src/marry_module.cpp
)

# Add library target
add_library(module_marry SHARED ${marry_src})

# Link the necessary libraries
target_link_libraries(module_marry service_pms service_pts)