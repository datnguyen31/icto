cmake_minimum_required(VERSION 3.5.0)
project(mission_sample)

set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR})

# Define the list of target drivers
include(targets.cmake)

# Loop through each target driver and set up build targets
foreach(DRIVER ${TARGET_DRIVER_LIST})
    add_subdirectory(../driver/${DRIVER} ${CMAKE_BINARY_DIR}/driver/${DRIVER})
endforeach()

message(INFORMATION " - CMAKE_BINARY_DIR: ${CMAKE_BINARY_DIR}")

# Install rules for each driver
foreach(DRIVER ${TARGET_DRIVER_LIST})
    install(DIRECTORY ${CMAKE_BINARY_DIR}/driver/${DRIVER}/lib DESTINATION lib)
endforeach()