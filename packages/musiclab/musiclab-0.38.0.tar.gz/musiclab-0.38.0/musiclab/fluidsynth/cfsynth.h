#ifndef __CFSYNTH_H__
#define __CFSYNTH_H__
#include "utils.h"

typedef struct fluidsynth_s fluidsynth_t;

_Err           cmusiclab_fluidsynth_init(const char *fluidsynth_lib_path);
void           cmusiclab_fluidsynth_deinit(void);
int            cmusiclab_fluidsynth_is_initialized(void);

void           cmusiclab_fluidsynth_version(int *major, int *minor, int *micro);
fluidsynth_t  *cmusiclab_fluidsynth_create_instance(void);
void           cmusiclab_fluidsynth_destroy_instance(fluidsynth_t **pfs);
_Err           cmusiclab_fluidsynth_new_settings(fluidsynth_t *fs);
void           cmusiclab_fluidsynth_delete_settings(fluidsynth_t *fs);
_Err           cmusiclab_fluidsynth_new_synth(fluidsynth_t *fs);
void           cmusiclab_fluidsynth_delete_synth(fluidsynth_t *fs);
int            cmusiclab_fluidsynth_load_soundfont(fluidsynth_t *fs, const char *soundfont_file);
_Err           cmusiclab_fluidsynth_settings_int(fluidsynth_t *fs, const char *setting_name, int value);
_Err           cmusiclab_fluidsynth_settings_float(fluidsynth_t *fs, const char *setting_name, double value);
_Err           cmusiclab_fluidsynth_settings_str(fluidsynth_t *fs, const char *setting_name, const char *value);
_Err           cmusiclab_fluidsynth_new_audio_driver(fluidsynth_t *fs);
void           cmusiclab_fluidsynth_delete_audio_driver(fluidsynth_t *fs);
_Err           cmusiclab_fluidsynth_new_midi_driver(fluidsynth_t *fs);
void           cmusiclab_fluidsynth_delete_midi_driver(fluidsynth_t *fs);

int            cmusiclab_fluidsynth_settings_gettype(fluidsynth_t *fs, const char *setting_name);
_Err           cmusiclab_fluidsynth_settings_getint(fluidsynth_t *fs, const char *setting_name, int *value);
_Err           cmusiclab_fluidsynth_settings_getfloat(fluidsynth_t *fs, const char *setting_name, double *value);
void           cmusiclab_fluidsynth_settings_getstr(fluidsynth_t *fs, const char *setting_name, char *value, int num_chars);

int            cmusiclab_fluidsynth_sfload(fluidsynth_t *fs, const char *filename);
int            cmusiclab_fluidsynth_sfcount(fluidsynth_t *fs);
_Err           cmusiclab_fluidsynth_sfunload(fluidsynth_t *fs, int sfont_id);
char          *cmusiclab_fluidsynth_get_sf_info(const char *soundfont_file);
char          *cmusiclab_fluidsynth_get_audio_devices(void);

_Err           cmusiclab_fluidsynth_new_cmd_handler(fluidsynth_t *fs);
void           cmusiclab_fluidsynth_delete_cmd_handler(fluidsynth_t *fs);
_Err           cmusiclab_fluidsynth_shell_command(fluidsynth_t *fs, const char *cmd, char *result, int num_chars);

#endif  // __CFSYNTH_H__
