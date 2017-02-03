cmake_minimum_required(VERSION 2.8)
project( cropper )

find_package(OpenCV REQUIRED )

set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR} )

find_package(FlyCapture2 REQUIRED )

include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable(cropper cropper.cpp )
target_link_libraries(cropper ${OpenCV_LIBS} )

install(TARGETS build )
