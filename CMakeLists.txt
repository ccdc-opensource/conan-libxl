cmake_minimum_required(VERSION 3.17.0)
project(cmake_wrapper)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

file(GLOB HEADERS source_subfolder/*.h source_subfolder/officeart/*.h source_subfolder/biff/*.h source_subfolder/biffblocks/*.h source_subfolder/struct/*.h source_subfolder/ooxml/*.h source_subfolder/ZipArchive/*.h source_subfolder/ZipArchive/bzip2/*.h source_subfolder/ZipArchive/zlib/*.h source_subfolder/lmx/*.h)
file(GLOB SOURCES source_subfolder/biff/*.cpp source_subfolder/biffblocks/*.cpp *.cpp source_subfolder/officeart/*.cpp source_subfolder/struct/*.cpp source_subfolder/ooxml/*.cpp source_subfolder/ZipArchive/*.cpp source_subfolder/ZipArchive/bzip2/*.c source_subfolder/ZipArchive/zlib/*.c source_subfolder/lmx/*.cpp)
file(GLOB RESOURCES source_subfolder/*.rc)
file(GLOB PUBLIC_C_HEADERS source_subfolder/include_c/*.h)
file(GLOB PUBLIC_CPP_HEADERS source_subfolder/include_cpp/*.h)

set(SOURCE_FILES ${HEADERS} ${SOURCES} ${RESOURCES} ${DEF} ${PUBLIC_C_HEADERS} ${PUBLIC_CPP_HEADERS})

set(IDIR source_subfolder/include_cpp source_subfolder/include_c source_subfolder/biff source_subfolder/biffblocks source_subfolder/struct source_subfolder/ZipArchive source_subfolder/lmx)

if(LIBXL_SHARED)
    message("Building shared library")
    add_library(libxl SHARED ${SOURCE_FILES})
else()
  add_library(libxl STATIC ${SOURCE_FILES})
  target_compile_definitions(libxl PUBLIC "LIBXL_STATIC")
endif()
MESSAGE("++ Operating system: ${CMAKE_SYSTEM_NAME}")

install(TARGETS libxl
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

# Only install the C++ headers
install(FILES ${PUBLIC_CPP_HEADERS} DESTINATION include)

if(WIN32)
  if(MSVC)
    target_compile_definitions(
        libxl PRIVATE
        _CRT_SECURE_NO_WARNINGS _SCL_SECURE_NO_WARNINGS _UNICODE UNICODE
        "$<$<CONFIG:Debug>:_DEBUG>"
        "$<$<CONFIG:Release>:NDEBUG>"
        )
    target_compile_options(
        libxl PRIVATE 
        /Zc:wchar_t /wd4267 /wd4244 /MP /bigobj
        "$<$<CONFIG:Debug>:/Od;/Ob0;/Zi;/RTC1>"
        "$<$<CONFIG:Release>:/O2;/Ob2>"
    )
  endif(MSVC)

  if(MINGW)

    target_include_directories(libxl PRIVATE ${IDIR} source_subfolder/mingw)

  else(MINGW)

  target_include_directories(libxl PRIVATE ${IDIR} source_subfolder/windows)

  endif(MINGW)

elseif(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    target_compile_definitions(
        libxl PRIVATE
        -U_FORTIFY_SOURCE -D_ZIP_SYSTEM_LINUX
        "$<$<CONFIG:Debug>:_DEBUG>"
        "$<$<CONFIG:Release>:NDEBUG>"
        )
    target_compile_options(
        libxl PRIVATE 
        -fno-stack-protector -fvisibility=hidden -Wno-deprecated-declarations
        "$<$<CONFIG:Release>:-O1>"
    )
    target_include_directories(libxl PRIVATE ${IDIR} source_subfolder/linux)
    set_target_properties(libxl PROPERTIES OUTPUT_NAME "xl")

ELSEIF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    target_compile_definitions(
        libxl PRIVATE
        -D_ZIP_SYSTEM_LINUX
        "$<$<CONFIG:Release>:NDEBUG>"
        )
    target_compile_options(
        libxl PRIVATE 
        -fvisibility=hidden
        "$<$<CONFIG:Release>:-O2>"
    )
    target_include_directories(libxl PRIVATE ${IDIR} source_subfolder/mac)
    set_target_properties(libxl PROPERTIES OUTPUT_NAME "xl")
    target_link_libraries(libxl "-framework CoreFoundation" "-framework CoreServices")
endif()

include(TestBigEndian)

TEST_BIG_ENDIAN(BIGENDIAN)
if(BIGENDIAN)
    target_compile_definitions(
        libxl PRIVATE
        _ZIP_BIG_ENDIAN _LIBXL_BIG_ENDIAN
    )
  message("++ Big endian platform detected")
endif()
# add_subdirectory(source_subfolder/clientapp)
