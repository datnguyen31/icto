cmake_minimum_required(VERSION 3.5.0)
project(module_john)

# Set output directories
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/modules/john/lib)

include_directories(${PLATFORM_SERVICE_PATH}
                    ${CMAKE_CURRENT_SOURCE_DIR}/mission
                    ${CMAKE_CURRENT_SOURCE_DIR}/platform
                    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Add source files
set(john_src
    src/john_module.cpp
)

# Add library target
add_library(module_john SHARED ${john_src})

# Link the necessary libraries
target_link_libraries(module_john service_pms service_pts)