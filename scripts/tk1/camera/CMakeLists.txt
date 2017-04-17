cmake_minimum_required(VERSION 2.8)
project( cropper )

find_package(OpenCV REQUIRED )

SET(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR})

INCLUDE(FindPackageHandleStandardArgs)
INCLUDE(HandleLibraryTypes)

SET(FlyCapture_IncludeSearchPaths
  /usr/include/flycapture/
  ${CMAKE_SOURCE_DIR}/include/
)

SET(FlyCapture_LibrarySearchPaths
  /usr/lib/
)

FIND_PATH(FLYCAPTURE2_INCLUDE_DIR FlyCapture2.h
  PATHS ${FlyCapture_IncludeSearchPaths}
)
FIND_LIBRARY(FLYCAPTURE2_LIBRARY_OPTIMIZED
  NAMES flycapture
  PATHS ${FlyCapture_LibrarySearchPaths}
)

# Handle the REQUIRED argument and set the <UPPERCASED_NAME>_FOUND variable
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FlyCapture2 "Could NOT find Flycapture2. Only required for testing purposes. Please continue."
  FLYCAPTURE2_LIBRARY_OPTIMIZED
  FLYCAPTURE2_INCLUDE_DIR
)

IF(FLYCAPTURE2_FOUND)
 FIND_PACKAGE_MESSAGE(FLYCAPTURE2_FOUND "Found Fly Capture SDK  ${FLYCAPTURE2_LIBRARY_OPTIMIZED}" "[${FLYCAPTURE2_LIBRARY_OPTIMIZED}][${FLYCAPTURE2_INCLUDE_DIR}]")
ENDIF(FLYCAPTURE2_FOUND)

# Collect optimized and debug libraries
HANDLE_LIBRARY_TYPES(FLYCAPTURE2)

MARK_AS_ADVANCED(
  FLYCAPTURE2_INCLUDE_DIR
  FLYCAPTURE2_LIBRARY_OPTIMIZED
)

include_directories( ${OpenCV_INCLUDE_DIRS} )
include_directories( ${FLYCAPTURE2_INCLUDE_DIR} )
add_executable(cropper cropper.cpp )
target_link_libraries(cropper ${OpenCV_LIBS} )
target_link_libraries(cropper  ${FLYCAPTURE2_LIBRARY_OPTIMIZED})
