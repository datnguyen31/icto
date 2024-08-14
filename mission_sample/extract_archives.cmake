# Convert the space-separated list to a CMake list
string(REPLACE " " ";" ALL_ARCHIVES "${ALL_ARCHIVES}")

foreach(ARCHIVE ${ALL_ARCHIVES})
    if(EXISTS "${ARCHIVE}")
        message(STATUS "Extracting: ${ARCHIVE}")
        execute_process(
            COMMAND ${CMAKE_AR} x ${ARCHIVE}
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/combined
            RESULT_VARIABLE EXTRACT_RESULT
        )
        if(NOT EXTRACT_RESULT EQUAL 0)
            message(WARNING "Failed to extract ${ARCHIVE}")
        endif()
    else()
        message(WARNING "Archive not found: ${ARCHIVE}")
    endif()
endforeach()

# Check if any .o files were extracted
file(GLOB OBJECT_FILES "${CMAKE_BINARY_DIR}/combined/*.o")
list(LENGTH OBJECT_FILES OBJECT_FILE_COUNT)
if(OBJECT_FILE_COUNT EQUAL 0)
    message(FATAL_ERROR "No object files found after extracting archives")
else()
    message(STATUS "Extracted ${OBJECT_FILE_COUNT} object files")
endif()