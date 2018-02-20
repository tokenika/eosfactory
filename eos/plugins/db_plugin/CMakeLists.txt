file(GLOB HEADERS "include/eos/db_plugin/*.hpp")
set( LIB_NAME db_plugin )

add_library( ${LIB_NAME}
  db_plugin.cpp
  ${HEADERS} 
)

###tokenika:
#find_package(libmongoc-1.0 1.8)
###tokenika

if (libmongoc-1.0_FOUND)

    # EOS has no direct dependencies on libmongoc but its shared libraries
    # will need to be present at runtime for the C++ libraries we use:
    # libbsoncxx & libmongocxx (both from github.com/mongodb/mongo-cxx-driver)

    # The *.cmake package files provided by mongo-cxx-driver don't give us the
    # absolute path to the libraries, which is needed whenever they are not
    # installed in system-known locations.  CMake requires the absolute paths
    # in target_link_libraries() since we are builiding an archive and the
    # link step for all executables using this archive must include the
    # mongo-cxx-driver libraries libmongocxx and libbsoncxx.

    find_package(libbsoncxx REQUIRED)
    message(STATUS "Found bsoncxx headers: ${LIBBSONCXX_INCLUDE_DIRS}")
    find_library(EOS_LIBBSONCXX ${LIBBSONCXX_LIBRARIES}
                 PATHS ${LIBBSONCXX_LIBRARY_DIRS} NO_DEFAULT_PATH)
    message(STATUS "Found bsoncxx library: ${EOS_LIBBSONCXX}")

    find_package(libmongocxx REQUIRED)
    message(STATUS "Found mongocxx headers: ${LIBMONGOCXX_INCLUDE_DIRS}")
    find_library(EOS_LIBMONGOCXX ${LIBMONGOCXX_LIBRARIES}
                 PATHS ${LIBMONGOCXX_LIBRARY_DIRS} NO_DEFAULT_PATH)
    message(STATUS "Found mongocxx library: ${EOS_LIBMONGOCXX}")

    add_definitions(-DMONGODB)
else()
    message("Could NOT find MongoDB. db_plugin with MongoDB support will not be included.")
    # sudo apt-get install pkg-config libssl-dev libsasl2-dev
    # wget https://github.com/mongodb/mongo-c-driver/releases/download/1.8.0/mongo-c-driver-1.8.0.tar.gz
    # tar xzf mongo-c-driver-1.8.0.tar.gz
    # cd mongo-c-driver-1.8.0
    # ./configure --disable-automatic-init-and-cleanup --enable-static
    # make
    # sudo make install
    #
    # git clone https://github.com/mongodb/mongo-cxx-driver.git --branch releases/stable --depth 1
    # cd mongo-cxx-driver/build
    # cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local ..
    # sudo make EP_mnmlstc_core
    # make
    # sudo make install
    #
    # sudo apt-get install mongodb
endif()

target_include_directories(${LIB_NAME}
  PRIVATE 
    ${LIBMONGOCXX_INCLUDE_DIRS} 
    ${LIBBSONCXX_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIR}
    ${OPENSSL_INCLUDE_DIR}
    "${CMAKE_SOURCE_DIR}/plugins/database_plugin/include"
    "${CMAKE_SOURCE_DIR}/libraries/native_contract/include"
    "${CMAKE_SOURCE_DIR}/libraries/fc/include"
    "${CMAKE_SOURCE_DIR}/libraries/types/include"
    "${CMAKE_SOURCE_DIR}/libraries/chainbase/include"
    "${CMAKE_SOURCE_DIR}/libraries/utilities/include"
  PUBLIC 
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

target_compile_definitions(${LIB_NAME}
	PRIVATE ${LIBMONGOCXX_DEFINITIONS} ${LIBBSONCXX_DEFINITIONS}
	)

target_link_libraries(${LIB_NAME}
        PUBLIC chain_plugin eos_chain appbase
        ${EOS_LIBMONGOCXX} ${EOS_LIBBSONCXX}
        )

install( TARGETS
   db_plugin

   RUNTIME DESTINATION bin
   LIBRARY DESTINATION lib
   ARCHIVE DESTINATION lib
)
install( FILES ${HEADERS} DESTINATION "include/eos/db_plugin" )
