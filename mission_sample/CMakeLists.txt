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