cmake_minimum_required(VERSION 3.5.0)
project(mission_jose)

add_definitions(-DMISSION=${MISSION})

set(PLATFORM_SERVICE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../ps/inc)
set(DRIVER_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../driver)

# Set the POSITION_INDEPENDENT_CODE property globally
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Disable optimizations and prevent inlining
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -fno-inline -fvisibility=default")

# Set the installation prefix to the binary directory
set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR})

# Include the component list which defines TARGET_DRIVER_LIST and PLATFORM_SERVICE_LIST
include(component_list.cmake)

# Initialize a variable to store all target names
set(ALL_TARGETS "")

# Loop through each target driver defined in TARGET_DRIVER_LIST
foreach(DRIVER ${TARGET_DRIVER_LIST})
    # Add the subdirectory for each driver and specify the binary directory for the build
    add_subdirectory(../driver/${DRIVER} ${CMAKE_BINARY_DIR}/driver/${DRIVER})
    # Append the driver target name to the ALL_TARGETS list
    list(APPEND ALL_TARGETS driver_${DRIVER})
endforeach()

# Loop through each platform service defined in PLATFORM_SERVICE_LIST
foreach(SERVICE ${PLATFORM_SERVICE_LIST})
    # Add the subdirectory for each service and specify the binary directory for the build
    add_subdirectory(../ps/${SERVICE} ${CMAKE_BINARY_DIR}/service/${SERVICE})
    # Append the service target name to the ALL_TARGETS list
    list(APPEND ALL_TARGETS service_${SERVICE})
endforeach()

# Loop through each module defined in MODULE_LIST
foreach(MODULE ${MODULE_LIST})
    # Add the subdirectory for each module and specify the binary directory for the build
    add_subdirectory(../modules/${MODULE}/obsw ${CMAKE_BINARY_DIR}/modules/${MODULE})
    # Append the module target name to the ALL_TARGETS list
    list(APPEND ALL_TARGETS module_${MODULE})
endforeach()

# Initialize a variable to store all archive file paths
set(ALL_ARCHIVES "")

# Collect all archive files from the driver targets
foreach(DRIVER ${TARGET_DRIVER_LIST})
    # Append the path to each driver archive to the ALL_ARCHIVES list
    list(APPEND ALL_ARCHIVES ${CMAKE_BINARY_DIR}/driver/${DRIVER}/lib/libdriver_${DRIVER}.a)
endforeach()

# Collect all archive files from the service targets
foreach(SERVICE ${PLATFORM_SERVICE_LIST})
    # Append the path to each service archive to the ALL_ARCHIVES list
    list(APPEND ALL_ARCHIVES ${CMAKE_BINARY_DIR}/service/${SERVICE}/lib/libservice_${SERVICE}.a)
endforeach()

# Create a custom target to merge all archives into a single archive
add_custom_target(merge_archives ALL
    # Create the directory for the combined archive
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/combined/lib
    # Run the extract_archives.cmake script to extract object files from all archives
    COMMAND ${CMAKE_COMMAND} 
        -DALL_ARCHIVES="${ALL_ARCHIVES}"
        -DCMAKE_AR=${CMAKE_AR}
        -DCMAKE_BINARY_DIR=${CMAKE_BINARY_DIR}
        -P ${CMAKE_CURRENT_SOURCE_DIR}/extract_archives.cmake
    # Create a new combined archive from the extracted object files
    COMMAND ${CMAKE_AR} rcs ${CMAKE_BINARY_DIR}/combined/lib/libcombined.a ${CMAKE_BINARY_DIR}/combined/*.o
    # Generate an index for the combined archive
    COMMAND ${CMAKE_RANLIB} ${CMAKE_BINARY_DIR}/combined/lib/libcombined.a
    # Specify that this target depends on all individual targets
    DEPENDS ${ALL_TARGETS}
    # Add a comment to be displayed during the build process
    COMMENT "Merging all archives into libcombined.a"
)

# Install the combined archive to the specified destination
install(FILES ${CMAKE_BINARY_DIR}/combined/lib/libcombined.a DESTINATION lib)

# Add the jose.cpp source file
add_executable(mission_jose mission_jose.cpp)

# Link the executable with libcombined.a and pthread, and prevent garbage collection of sections
target_link_libraries(mission_jose 
    -Wl,--whole-archive ${CMAKE_BINARY_DIR}/combined/lib/libcombined.a -Wl,--no-whole-archive 
    -Wl,--no-gc-sections
    -Wl,--export-dynamic
    pthread dl g
)

set(MODULE_SO_FILES "")

# Append .so files to the list
foreach(MODULE ${MODULE_LIST})
    list(APPEND MODULE_SO_FILES ${CMAKE_BINARY_DIR}/modules/${MODULE}/libmodule_${MODULE}.so)
endforeach()

# Create a custom target to copy all necessary files to ./build/exe
add_custom_target(copy_files_to_exe ALL
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/exe
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/exe/nonvol
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/mission_modules.txt ${CMAKE_BINARY_DIR}/exe/
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:mission_jose> ${CMAKE_BINARY_DIR}/exe/
    COMMAND ${CMAKE_COMMAND} -E copy ${MODULE_SO_FILES} ${CMAKE_BINARY_DIR}/exe/nonvol
    DEPENDS mission_jose merge_archives ${MODULE_SO_FILES}
    COMMENT "Copying .so files, executable, and mission_modules.txt to ./build/exe"
)