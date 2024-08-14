# Convert the space-separated list of archives to a CMake list
string(REPLACE " " ";" ALL_ARCHIVES "${ALL_ARCHIVES}")

# Loop through each archive in the list
foreach(ARCHIVE ${ALL_ARCHIVES})
    # Check if the archive file exists
    if(EXISTS "${ARCHIVE}")
        # Print a status message indicating the archive being extracted
        message(STATUS "Extracting: ${ARCHIVE}")
        # Execute the command to extract object files from the archive
        execute_process(
            COMMAND ${CMAKE_AR} x ${ARCHIVE}
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/combined
            RESULT_VARIABLE EXTRACT_RESULT
        )
        # Check if the extraction was successful
        if(NOT EXTRACT_RESULT EQUAL 0)
            # Print a warning message if the extraction failed
            message(WARNING "Failed to extract ${ARCHIVE}")
        endif()
    else()
        # Print a warning message if the archive file does not exist
        message(WARNING "Archive not found: ${ARCHIVE}")
    endif()
endforeach()

# Check if any object files were extracted
file(GLOB OBJECT_FILES "${CMAKE_BINARY_DIR}/combined/*.o")
list(LENGTH OBJECT_FILES OBJECT_FILE_COUNT)
if(OBJECT_FILE_COUNT EQUAL 0)
    # Print a fatal error message if no object files were found
    message(FATAL_ERROR "No object files found after extracting archives")
else()
    # Print a status message indicating the number of object files extracted
    message(STATUS "Extracted ${OBJECT_FILE_COUNT} object files")
endif()