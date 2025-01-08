#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "FluidSynth::fluidsynth" for configuration "RelWithDebInfo"
set_property(TARGET FluidSynth::fluidsynth APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(FluidSynth::fluidsynth PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/fluidsynth"
  )

list(APPEND _cmake_import_check_targets FluidSynth::fluidsynth )
list(APPEND _cmake_import_check_files_for_FluidSynth::fluidsynth "${_IMPORT_PREFIX}/bin/fluidsynth" )

# Import target "FluidSynth::libfluidsynth" for configuration "RelWithDebInfo"
set_property(TARGET FluidSynth::libfluidsynth APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(FluidSynth::libfluidsynth PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "/Users/anustuv/UTM_dir/Shared_drive/musiclab-engine/musiclab/fluidsynth/libfluidsynth/Library/Frameworks/FluidSynth.framework/Versions/3/FluidSynth"
  IMPORTED_SONAME_RELWITHDEBINFO "FluidSynth.framework/Versions/3/FluidSynth"
  )

list(APPEND _cmake_import_check_targets FluidSynth::libfluidsynth )
list(APPEND _cmake_import_check_files_for_FluidSynth::libfluidsynth "/Users/anustuv/UTM_dir/Shared_drive/musiclab-engine/musiclab/fluidsynth/libfluidsynth/Library/Frameworks/FluidSynth.framework/Versions/3/FluidSynth" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
