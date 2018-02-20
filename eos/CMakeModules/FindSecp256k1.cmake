# This module defines:
#  SECP256K1_FOUND             - system has Secp256k1 lib
#  SECP256K1_INCLUDE_DIR       - the Secp256k1 include directory
#  SECP256K1_LIBRARIES_DIR     - directory where the Secp256k1 libraries are located
#  SECP256K1_LIBRARIES         - Link these to use Secp256k1

include(FindPackageHandleStandardArgs)

if(SECP256K1_INCLUDE_DIR)
  set(Secp256k1_in_cache TRUE)
else()
  set(Secp256k1_in_cache FALSE)
endif()
if(NOT SECP256K1_LIBRARIES)
  set(Secp256k1_in_cache FALSE)
endif()

# Is it already configured?
if (Secp256k1_in_cache)
  set(SECP256K1_FOUND TRUE)
else()
  find_path(SECP256K1_INCLUDE_DIR
    NAMES secp256k1.h
    HINTS ENV SECP256k1_INC_DIR
          ENV SECP256k1_DIR
          ENV Secp256k1_ROOT_DIR
    PATH_SUFFIXES include
    DOC "The directory containing the Secp256k1 header files"    
  )

  find_library(SECP256K1_LIBRARIES NAMES libsecp256k1.a secp256k1.lib secp256k1

    HINTS ENV Secp256k1_LIB_DIR
          ENV SECP256k1_DIR
          ENV Secp256k1_ROOT_DIR
    PATH_SUFFIXES lib
    DOC "Path to the  Secp256k1Config library"
  )

  if ( SECP256K1_LIBRARIES )
    get_filename_component(SECP256K1_LIBRARIES_DIR ${SECP256K1_LIBRARIES} PATH CACHE )
  endif()

  find_package_handle_standard_args(Secp256k1 "DEFAULT_MSG" 
    SECP256K1_LIBRARIES SECP256K1_INCLUDE_DIR)

endif()
