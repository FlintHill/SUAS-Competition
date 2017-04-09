cmake_minimum_required(VERSION 2.8)
project( cropper )

find_package(OpenCV REQUIRED )

include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable(cropper camera_cropper_testing.cpp )
target_link_libraries(cropper ${OpenCV_LIBS} )
