cmake_minimum_required(VERSION 3.1.0)
project(test_package)

find_package(Boost.SIMD REQUIRED)

# The components from Boost.SIMD (target Boost::SIMD) won't work,
# as it is defined in Boost.SIMD cmake package file, so we
# could not use the Boost.SIMD components in basic find_package(Boost).
find_package(Boost REQUIRED COMPONENTS date_time) #  COMPONENTS SIMD)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} Boost::headers Boost::SIMD)
