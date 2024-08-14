set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR})

# Define the list of target drivers
include(component_list.cmake)

# Lists to store target names
set(ALL_TARGETS "")

# Loop through each target driver and set up build targets
foreach(DRIVER ${TARGET_DRIVER_LIST})
    add_subdirectory(../driver/${DRIVER} ${CMAKE_BINARY_DIR}/driver/${DRIVER})
    list(APPEND ALL_TARGETS driver_${DRIVER})
endforeach()

# Loop through each platform service and set up build targets
foreach(SERVICE ${PLATFORM_SERVICE_LIST})
    add_subdirectory(../ps/${SERVICE} ${CMAKE_BINARY_DIR}/service/${SERVICE})
    list(APPEND ALL_TARGETS service_${SERVICE})
endforeach()

# Create a list to store all archive files
set(ALL_ARCHIVES "")

# Collect all archive files
foreach(DRIVER ${TARGET_DRIVER_LIST})
    list(APPEND ALL_ARCHIVES ${CMAKE_BINARY_DIR}/driver/${DRIVER}/lib/libdriver_${DRIVER}.a)
endforeach()

foreach(SERVICE ${PLATFORM_SERVICE_LIST})
    list(APPEND ALL_ARCHIVES ${CMAKE_BINARY_DIR}/service/${SERVICE}/lib/libservice_${SERVICE}.a)
endforeach()

# Create a custom target to merge all archives
add_custom_target(merge_archives ALL
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/combined/lib
    COMMAND ${CMAKE_COMMAND} 
        -DALL_ARCHIVES="${ALL_ARCHIVES}"
        -DCMAKE_AR=${CMAKE_AR}
        -DCMAKE_BINARY_DIR=${CMAKE_BINARY_DIR}
        -P ${CMAKE_CURRENT_SOURCE_DIR}/extract_archives.cmake
    COMMAND ${CMAKE_AR} rcs ${CMAKE_BINARY_DIR}/combined/lib/libcombined.a ${CMAKE_BINARY_DIR}/combined/*.o
    COMMAND ${CMAKE_RANLIB} ${CMAKE_BINARY_DIR}/combined/lib/libcombined.a
    DEPENDS ${ALL_TARGETS}
    COMMENT "Merging all archives into libcombined.a"
)

# Install the combined archive
install(FILES ${CMAKE_BINARY_DIR}/combined/lib/libcombined.a DESTINATION lib)

