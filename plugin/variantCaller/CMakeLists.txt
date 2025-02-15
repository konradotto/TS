# Copyright (C) 2010 Ion Torrent Systems, Inc. All Rights Reserved
cmake_minimum_required (VERSION 2.6)

# derive the plugin name from the folder name
get_filename_component(PLUGIN_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)
PROJECT(${PLUGIN_NAME})

# this method will search the plugin script for it's version number and insert that into the debian package
include(../cmake/CMakeLists.PluginGetVersion.txt)

# set the standard package attributes
include(../cmake/CMakeLists.PluginSetAttributes.txt)

# these are the package specific attributues which cannot be automated
SET(CPACK_PACKAGE_DESCRIPTION "This plugin assembles reads into long sequences (contigs) and allows for basic level analysis, with metrics such as number of contigs, N50, and other analysis metrics.")
SET(CPACK_DEBIAN_PACKAGE_DEPENDS "python, ion-pipeline")
SET(CPACK_DEBIAN_PACKAGE_MAINTAINER "Brian Bourke-Martin")

INSTALL(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        DESTINATION "${CPACK_PACKAGE_INSTALL_DIRECTORY}"
        USE_SOURCE_PERMISSIONS
        REGEX "^${CMAKE_CURRENT_SOURCE_DIR}/build" EXCLUDE
        REGEX "^${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.txt" EXCLUDE
        REGEX "^${CMAKE_CURRENT_SOURCE_DIR}/debian" EXCLUDE
        PATTERN "parameter_sets.json" EXCLUDE
       )

add_custom_target(parameter_sets ALL
                   COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/pluginMedia/parameter_sets/build_parameter_sets.py" "${CMAKE_CURRENT_BINARY_DIR}/parameter_sets.json"
                   WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/pluginMedia/parameter_sets/"
                   COMMENT "Combining individual parameter sets into a single parameter_sets.json")

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/parameter_sets.json" DESTINATION "${CPACK_PACKAGE_INSTALL_DIRECTORY}/variantCaller/pluginMedia/parameter_sets")

message(STATUS "${CMAKE_CURRENT_BINARY_DIR}")

SET(ANALYSIS_BUILD_DIR)
if(EXISTS "${CMAKE_CURRENT_BINARY_DIR}/../../Analysis")
  SET(ANALYSIS_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/../../Analysis")
endif()

# when build variantCaller only
if(EXISTS "${CMAKE_CURRENT_BINARY_DIR}/../../../build/Analysis")
  SET(ANALYSIS_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/../../../build/Analysis")
endif()

if(DEFINED ANALYSIS_BUILD_DIR)
    SET(CPACK_PACKAGE_VERSION "${VERSION}-${LSB_RELEASE_CODENAME}")
    SET(CPACK_PACKAGE_FILE_NAME "ion-plugin-${DEB_PLUGIN_NAME}-${CPACK_PACKAGE_VERSION}")
    message(STATUS "Adding Ubuntu codename to the version: ${CPACK_PACKAGE_VERSION}")
    message(STATUS "Adding tmap from Analysis build")
    install(PROGRAMS "${ANALYSIS_BUILD_DIR}/TMAP/tmap" DESTINATION "${CPACK_PACKAGE_INSTALL_DIRECTORY}/variantCaller/bin/")
    message(STATUS "Adding tvc from Analysis build")
    install(PROGRAMS "${ANALYSIS_BUILD_DIR}/tvc" DESTINATION "${CPACK_PACKAGE_INSTALL_DIRECTORY}/variantCaller/bin/")
    message(STATUS "Adding tvcutils from Analysis build")
    install(PROGRAMS "${ANALYSIS_BUILD_DIR}/tvcutils" DESTINATION "${CPACK_PACKAGE_INSTALL_DIRECTORY}/variantCaller/bin/")
endif()

INCLUDE(CPack)
