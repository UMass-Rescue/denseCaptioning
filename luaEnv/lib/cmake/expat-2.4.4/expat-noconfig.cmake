#----------------------------------------------------------------
# Generated CMake target import file for configuration "NoConfig".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "expat::expat" for configuration "NoConfig"
set_property(TARGET expat::expat APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(expat::expat PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libexpat.so.1.8.4"
  IMPORTED_SONAME_NOCONFIG "libexpat.so.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS expat::expat )
list(APPEND _IMPORT_CHECK_FILES_FOR_expat::expat "${_IMPORT_PREFIX}/lib/libexpat.so.1.8.4" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
