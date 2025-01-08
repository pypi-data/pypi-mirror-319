#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <unistd.h>
#include "cfsynth.h"

#define PATH_MAX    (1024)

/* fluidsynth.h declarations */
#define FLUID_FAILED    (-1)
typedef void *fluid_synth_t;

static void                ( *pfluid_version ) ( int *major, int *minor, int *micro );

typedef struct _fluid_sfont_t my_fluid_sfont_t;
typedef struct _fluid_preset_t my_fluid_preset_t;

typedef int                ( *fluid_sfont_free_t )            ( my_fluid_sfont_t *sfont );
typedef const char        *( *fluid_sfont_get_name_t )        ( my_fluid_sfont_t *sfont );
typedef void               ( *fluid_sfont_iteration_start_t ) ( my_fluid_sfont_t *sfont );
typedef my_fluid_preset_t *( *fluid_sfont_get_preset_t )      ( my_fluid_sfont_t *sfont, int bank, int prenum );
typedef my_fluid_preset_t *( *fluid_sfont_iteration_next_t )  ( my_fluid_sfont_t *sfont );
typedef void               ( *fluid_preset_free_t )           ( my_fluid_preset_t *preset );
typedef const char        *( *fluid_preset_get_name_t )       ( my_fluid_preset_t *preset );
typedef int                ( *fluid_preset_get_banknum_t )    ( my_fluid_preset_t *preset );
typedef int                ( *fluid_preset_get_num_t )        ( my_fluid_preset_t *preset );
typedef int                ( *fluid_preset_noteon_t )         ( my_fluid_preset_t *preset,
                                                                fluid_synth_t *synth,
                                                                int chan, int key, int vel
                                                              );

typedef void              *fluid_settings_t;
static fluid_settings_t   *( *pnew_fluid_settings )           ( void );
static fluid_synth_t      *( *pnew_fluid_synth )              ( fluid_settings_t *settings );
static int                 ( *pfluid_synth_sfload )	          ( fluid_synth_t *synth, const char *filename, int reset_presets );
static my_fluid_sfont_t   *( *pfluid_synth_get_sfont_by_id )  ( fluid_synth_t *synth, int sf_id);

static int                 ( *pfluid_synth_sfcount )          ( fluid_synth_t *synth );
static int                 ( *pfluid_synth_sfunload )         ( fluid_synth_t *synth, unsigned int id, int reset_presets );
static int                 ( *pdelete_fluid_synth )           ( fluid_synth_t *synth );
static void                ( *pdelete_fluid_settings )        ( fluid_settings_t *settings );

struct _fluid_sfont_t
{
    void *data;
    int id;
    int refcount;
    int bankofs;
    fluid_sfont_free_t free;
    fluid_sfont_get_name_t get_name;
    fluid_sfont_get_preset_t get_preset;
    fluid_sfont_iteration_start_t iteration_start;
    fluid_sfont_iteration_next_t iteration_next;
};

struct _fluid_preset_t
{
    void *data;
    my_fluid_sfont_t *sfont;
    fluid_preset_free_t free;
    fluid_preset_get_name_t get_name;
    fluid_preset_get_banknum_t get_banknum;
    fluid_preset_get_num_t get_num;
    fluid_preset_noteon_t noteon;
    int (*notify)(my_fluid_preset_t *preset, int reason, int chan);
};

typedef void                *fluid_audio_driver_t;
static fluid_audio_driver_t *( *pnew_fluid_audio_driver ) ( fluid_settings_t *settings, fluid_synth_t *synth );
static void                 *( *pdelete_fluid_audio_driver ) ( fluid_audio_driver_t *driver );

typedef void                *fluid_midi_event_t;
typedef int                  ( *handle_midi_event_func_t ) ( void *data, fluid_midi_event_t *event );
static int                   ( *pfluid_synth_handle_midi_event ) ( void *data, fluid_midi_event_t *event );
static int                   ( *pfluid_midi_router_handle_midi_event ) ( void *data, fluid_midi_event_t *event );

typedef void                *fluid_midi_driver_t;
static fluid_midi_driver_t  *( *pnew_fluid_midi_driver )   ( fluid_settings_t *settings, handle_midi_event_func_t handler, void *event_handler_data );
static void                 *( *pdelete_fluid_midi_driver ) ( fluid_midi_driver_t *driver );

static int                   ( *pfluid_settings_setstr ) ( fluid_settings_t *settings, const char *name, const char *str );
static int                   ( *pfluid_settings_setint ) ( fluid_settings_t *settings, const char *name, int val );
static int                   ( *pfluid_settings_setnum ) ( fluid_settings_t *settings, const char *name, double val );

typedef void                *fluid_midi_router_t;
static fluid_midi_router_t  *( *pnew_fluid_midi_router ) ( fluid_settings_t *settings, handle_midi_event_func_t handler, void *event_handler_data );
static void                  ( *pdelete_fluid_midi_router ) ( fluid_midi_router_t *handler );

static int                   ( *pfluid_settings_get_type ) ( fluid_settings_t *settings, const char *name );
static int                   ( *pfluid_settings_copystr ) ( fluid_settings_t *settings, const char *name, char *value, int num_chars );
static int                   ( *pfluid_settings_getnum ) ( fluid_settings_t *settings, const char *name, double *val );
static int                   ( *pfluid_settings_getint ) ( fluid_settings_t *settings, const char *name, int *val );

typedef void                 ( *fluid_settings_foreach_option_t) (void *data, const char *name, const char *option);
static int                   ( *pfluid_settings_option_count ) ( fluid_settings_t *settings, const char *name );
static void                  ( *pfluid_settings_foreach_option ) ( fluid_settings_t *settings,
                                                                   const char *name, void *data,
                                                                   fluid_settings_foreach_option_t func );

typedef void                *fluid_cmd_handler_t;
typedef void                *fluid_player_t;
typedef int                  fluid_ostream_t;
static fluid_cmd_handler_t   ( *pnew_fluid_cmd_handler2 ) (fluid_settings_t *settings, fluid_synth_t *synth, fluid_midi_router_t *router, fluid_player_t *player);
static void                  ( *pdelete_fluid_cmd_handler ) ( fluid_cmd_handler_t *handler );
static int                   ( *pfluid_command ) ( fluid_cmd_handler_t *handler, const char *cmd, fluid_ostream_t out );
static int                   ( *pfluid_source ) ( fluid_cmd_handler_t *handler, const char *filename );

/* ----------------- */
void *dl_fluidsynth;

_Err cmusiclab_fluidsynth_init(const char *fluidsynth_lib)
{
    LOGDBG("libfluidsynth path %s\n", fluidsynth_lib);
    dl_fluidsynth = dlopen(fluidsynth_lib, RTLD_NOW | RTLD_GLOBAL);
    if (!dl_fluidsynth) {
        LOGERR("dlopen error: %s\n", dlerror());
        goto fn_fail;
    }

    pfluid_version                       = dlsym(dl_fluidsynth, "fluid_version");
    pnew_fluid_settings                  = dlsym(dl_fluidsynth, "new_fluid_settings");
    pnew_fluid_synth                     = dlsym(dl_fluidsynth, "new_fluid_synth");
    pfluid_synth_sfload                  = dlsym(dl_fluidsynth, "fluid_synth_sfload");
    pfluid_synth_sfcount                 = dlsym(dl_fluidsynth, "fluid_synth_sfcount");
    pfluid_synth_get_sfont_by_id         = dlsym(dl_fluidsynth, "fluid_synth_get_sfont_by_id");
    pfluid_synth_sfunload                = dlsym(dl_fluidsynth, "fluid_synth_sfunload");
    pdelete_fluid_synth                  = dlsym(dl_fluidsynth, "delete_fluid_synth");
    pdelete_fluid_settings               = dlsym(dl_fluidsynth, "delete_fluid_settings");
    pnew_fluid_audio_driver              = dlsym(dl_fluidsynth, "new_fluid_audio_driver");
    pnew_fluid_midi_driver               = dlsym(dl_fluidsynth, "new_fluid_midi_driver");
    pdelete_fluid_midi_driver            = dlsym(dl_fluidsynth, "delete_fluid_midi_driver");
    pdelete_fluid_audio_driver           = dlsym(dl_fluidsynth, "delete_fluid_audio_driver");
    pfluid_settings_setstr               = dlsym(dl_fluidsynth, "fluid_settings_setstr");
    pfluid_settings_setint               = dlsym(dl_fluidsynth, "fluid_settings_setint");
    pfluid_settings_setnum               = dlsym(dl_fluidsynth, "fluid_settings_setnum");
    pfluid_synth_handle_midi_event       = dlsym(dl_fluidsynth, "fluid_synth_handle_midi_event");
    pnew_fluid_midi_router               = dlsym(dl_fluidsynth, "new_fluid_midi_router");
    pfluid_midi_router_handle_midi_event = dlsym(dl_fluidsynth, "fluid_midi_router_handle_midi_event");
    pdelete_fluid_midi_router            = dlsym(dl_fluidsynth, "delete_fluid_midi_router");
    pfluid_settings_get_type             = dlsym(dl_fluidsynth, "fluid_settings_get_type");
    pfluid_settings_copystr              = dlsym(dl_fluidsynth, "fluid_settings_copystr");
    pfluid_settings_getnum               = dlsym(dl_fluidsynth, "fluid_settings_getnum");
    pfluid_settings_getint               = dlsym(dl_fluidsynth, "fluid_settings_getint");
    pfluid_settings_option_count         = dlsym(dl_fluidsynth, "fluid_settings_option_count");
    pfluid_settings_foreach_option       = dlsym(dl_fluidsynth, "fluid_settings_foreach_option");
    pnew_fluid_cmd_handler2              = dlsym(dl_fluidsynth, "new_fluid_cmd_handler2");
    pdelete_fluid_cmd_handler            = dlsym(dl_fluidsynth, "delete_fluid_cmd_handler");
    pfluid_command                       = dlsym(dl_fluidsynth, "fluid_command");
    pfluid_source                        = dlsym(dl_fluidsynth, "fluid_source");

    if (!pnew_fluid_settings || !pnew_fluid_synth || !pfluid_synth_sfload || !pfluid_synth_get_sfont_by_id ||
       !pfluid_synth_sfunload || !pdelete_fluid_synth || !pdelete_fluid_settings ||
       !pnew_fluid_audio_driver || !pnew_fluid_midi_driver || !pdelete_fluid_midi_driver ||
       !pdelete_fluid_audio_driver || !pfluid_settings_setstr || !pfluid_settings_setint ||
       !pfluid_settings_setnum || !pfluid_synth_handle_midi_event || !pnew_fluid_midi_router ||
       !pdelete_fluid_midi_router || !pfluid_settings_get_type || !pfluid_settings_copystr ||
       !pfluid_settings_getnum || !pfluid_settings_getint || !pfluid_version || !pfluid_synth_sfcount ||
       !pfluid_settings_option_count || !pfluid_settings_foreach_option ||
       !pnew_fluid_cmd_handler2 || !pdelete_fluid_cmd_handler || !pfluid_command || !pfluid_source
       )
    {
        LOGERR("Symbols weren't loaded\n");
        goto fn_fail;
    }
    return NO_ERR;
fn_fail:
    dl_fluidsynth = NULL;
    return ERR;
}

void cmusiclab_fluidsynth_deinit()
{
    pfluid_version                 = NULL;
    pnew_fluid_settings            = NULL;
    pnew_fluid_synth               = NULL;
    pfluid_synth_sfload            = NULL;
    pfluid_synth_sfcount           = NULL;
    pfluid_synth_get_sfont_by_id   = NULL;
    pfluid_synth_sfunload          = NULL;
    pdelete_fluid_synth            = NULL;
    pdelete_fluid_settings         = NULL;
    pnew_fluid_audio_driver        = NULL;
    pnew_fluid_midi_driver         = NULL;
    pdelete_fluid_midi_driver      = NULL;
    pdelete_fluid_audio_driver     = NULL;
    pfluid_settings_setstr         = NULL;
    pfluid_settings_setint         = NULL;
    pfluid_settings_setnum         = NULL;
    pfluid_synth_handle_midi_event = NULL;
    pfluid_settings_get_type       = NULL;
    pfluid_settings_copystr        = NULL;
    pfluid_settings_getnum         = NULL;
    pfluid_settings_getint         = NULL;
    pfluid_settings_option_count   = NULL;
    pfluid_settings_foreach_option = NULL;
    pnew_fluid_cmd_handler2        = NULL;
    pdelete_fluid_cmd_handler      = NULL;
    pfluid_command                 = NULL;
    pfluid_source                  = NULL;
    dlclose(dl_fluidsynth);
    dl_fluidsynth = NULL;
}

void cmusiclab_fluidsynth_version(int *major, int *minor, int *micro)
{
    pfluid_version(major, minor, micro);
}

int cmusiclab_fluidsynth_is_initialized()
{
    if (dl_fluidsynth != NULL) {
        return 1;
    }
    return 0;
}

struct fluidsynth_s {
    fluid_settings_t *settings;
    fluid_synth_t *synth;
    fluid_audio_driver_t *adriver;
    fluid_midi_driver_t *mdriver;
    fluid_midi_router_t *router;
    fluid_cmd_handler_t *cmd_handler;
};


char *cmusiclab_fluidsynth_get_sf_info(const char *soundfont_file)
{
    fluid_settings_t* settings = pnew_fluid_settings();
    fluid_synth_t* synth = pnew_fluid_synth(settings);
    int sfont_id;

    sfont_id = pfluid_synth_sfload(synth, soundfont_file, 1);
    if (sfont_id == FLUID_FAILED) {
        fprintf(stderr, "Failed to load sound font file.\n");
        return NULL;
    }

    my_fluid_sfont_t* sfont = pfluid_synth_get_sfont_by_id(synth, sfont_id);
    if (sfont == NULL) {
        fprintf(stderr, "Failed to load soundfont.\n");
        return NULL;
    }

    my_fluid_preset_t* preset = NULL;

    size_t buffer_size = 256, used_size = 0;
    char* sf_info_str = calloc(buffer_size, sizeof(char));
    if (!sf_info_str) {
        return NULL;
    }

    const char *preset_name;
    int bank_num, preset_num;
    sfont->iteration_start(sfont);

    while (1) {
        preset = sfont->iteration_next(sfont);
        if (preset == NULL) break;

        preset_name = preset->get_name(preset);
        bank_num = preset->get_banknum(preset);
        preset_num = preset->get_num(preset);

        size_t entry_length = snprintf(NULL, 0, "%d-%d: %s\n", bank_num, preset_num, preset_name) + 1;

        if (used_size + entry_length >= buffer_size) {
            buffer_size *= 2;
            char* temp = realloc(sf_info_str, buffer_size);
            if (!temp) {
                free(sf_info_str);
                return NULL;
            }
            sf_info_str = temp;
        }

        snprintf(sf_info_str + used_size, entry_length, "%d-%d: %s\n", bank_num, preset_num, preset_name);
        used_size += entry_length - 1;
    }

    pfluid_synth_sfunload(synth, sfont_id, 1);
    pdelete_fluid_synth(synth);
    pdelete_fluid_settings(settings);

    return sf_info_str;
}

typedef struct {
    int count;
    int cur_idx;
    char *buf;
} IterVar;

static void settings_option_foreach_func(void *data, const char *name __attribute__((unused)), const char *option)
{
    IterVar *iter = data;
    iter->cur_idx++;
    strcat(iter->buf, option);
    strcat(iter->buf, "\n");
}

const char *audio_coreaudio_device = "audio.coreaudio.device";

char *cmusiclab_fluidsynth_get_audio_devices()
{
    fluid_settings_t *settings = pnew_fluid_settings();
    int count = pfluid_settings_option_count(settings, audio_coreaudio_device);
    IterVar iter = {count, 0, NULL};
    size_t buffer_size = 256;
    iter.buf = calloc(buffer_size, sizeof(char));
    pfluid_settings_foreach_option(settings, audio_coreaudio_device, &iter, settings_option_foreach_func);
    pdelete_fluid_settings(settings);
    return iter.buf;
}

fluidsynth_t *cmusiclab_fluidsynth_create_instance()
{
    fluidsynth_t *fs = (fluidsynth_t *) calloc (1, sizeof(fluidsynth_t));
    if (!fs) {
        fprintf(stderr, "Failed to allocate memory for fluidsynth struct.\n");
        return NULL;
    }
    return fs;
}

void cmusiclab_fluidsynth_destroy_instance(fluidsynth_t **pfs)
{
    fluidsynth_t *fs = *pfs;
    if (!fs) return;
    free(fs);
    *pfs = NULL;
}

_Err cmusiclab_fluidsynth_new_settings(fluidsynth_t *fs)
{
    fs->settings = pnew_fluid_settings();
    if (!fs->settings) {
        fprintf(stderr, "Failed to create settings.\n");
        free(fs);
        return ERR;
    }
    return NO_ERR;
}

void cmusiclab_fluidsynth_delete_settings(fluidsynth_t *fs)
{
    if (fs->settings) {
        pdelete_fluid_settings(fs->settings);
        fs->settings = NULL;
    }
}

_Err cmusiclab_fluidsynth_new_synth(fluidsynth_t *fs)
{
    fs->synth = pnew_fluid_synth(fs->settings);
    if (!fs->synth) {
        fprintf(stderr, "Failed to create synth.\n");
        pdelete_fluid_settings(fs->settings);
        free(fs);
        return ERR;
    }
    return NO_ERR;
}

void cmusiclab_fluidsynth_delete_synth(fluidsynth_t *fs)
{
    if (fs->synth) {
        pdelete_fluid_synth(fs->synth);
        fs->synth = NULL;
    }
}

int cmusiclab_fluidsynth_load_soundfont(fluidsynth_t *fs, const char *soundfont_file)
{
    int sfont_id;
    sfont_id = pfluid_synth_sfload(fs->synth, soundfont_file, 1);
    if (sfont_id == FLUID_FAILED) {
        fprintf(stderr, "Failed to load sound font file.\n");
        return ERR;
    }
    return sfont_id;
}

_Err cmusiclab_fluidsynth_settings_int(fluidsynth_t *fs, const char *setting_name, int value)
{
    if (!fs->settings) {
        fprintf(stderr, "Fluidsynth settings not initialized\n");
        return ERR;
    }
    if (pfluid_settings_setint(fs->settings, setting_name, value)) {
        fprintf(stderr, "Failed to set setting '%s' to %d\n", setting_name, value);
        return ERR;
    }
    return NO_ERR;
}

_Err cmusiclab_fluidsynth_settings_float(fluidsynth_t *fs, const char *setting_name, double value)
{
    if (!fs->settings) {
        fprintf(stderr, "Fluidsynth settings not initialized\n");
        return ERR;
    }
    if (pfluid_settings_setnum(fs->settings, setting_name, value)) {
        fprintf(stderr, "Failed to set setting '%s' to %lf\n", setting_name, value);
        return ERR;
    }
    return NO_ERR;
}

_Err cmusiclab_fluidsynth_settings_str(fluidsynth_t *fs, const char *setting_name, const char *value)
{
    if (!fs->settings) {
        fprintf(stderr, "Fluidsynth settings not initialized\n");
        return ERR;
    }
    if (pfluid_settings_setstr(fs->settings, setting_name, value)) {
        fprintf(stderr, "Failed to set setting '%s' to %s\n", setting_name, value);
        return ERR;
    }
    return NO_ERR;
}

int cmusiclab_fluidsynth_settings_gettype(fluidsynth_t *fs, const char *setting_name)
{
    return pfluid_settings_get_type(fs->settings, setting_name);
}

_Err cmusiclab_fluidsynth_settings_getint(fluidsynth_t *fs, const char *setting_name, int *value)
{
    if (!fs->settings) {
        fprintf(stderr, "Fluidsynth settings not initialized\n");
        return ERR;
    }
    if (pfluid_settings_getint(fs->settings, setting_name, value)) {
        fprintf(stderr, "Failed to get setting '%s'\n", setting_name);
        return ERR;
    }
    return NO_ERR;
}

_Err cmusiclab_fluidsynth_settings_getfloat(fluidsynth_t *fs, const char *setting_name, double *value)
{
    if (!fs->settings) {
        fprintf(stderr, "Fluidsynth settings not initialized\n");
        return ERR;
    }
    if (pfluid_settings_getnum(fs->settings, setting_name, value)) {
        fprintf(stderr, "Failed to get setting '%s'\n", setting_name);
        return ERR;
    }
    return NO_ERR;
}

void cmusiclab_fluidsynth_settings_getstr(fluidsynth_t *fs, const char *setting_name, char *value, int num_chars)
{
    if (!fs->settings) {
        fprintf(stderr, "Fluidsynth settings not initialized\n");
    }
    if (pfluid_settings_copystr(fs->settings, setting_name, value, num_chars)) {
        fprintf(stderr, "Failed to get setting '%s'\n", setting_name);
    }
}

void cmusiclab_fluidsynth_delete_audio_driver(fluidsynth_t *fs)
{
    if (fs->adriver) {
        pdelete_fluid_audio_driver(fs->adriver);
        fs->adriver = NULL;
    }
}

_Err cmusiclab_fluidsynth_new_audio_driver(fluidsynth_t *fs)
{
    cmusiclab_fluidsynth_delete_audio_driver(fs);
    fs->adriver = pnew_fluid_audio_driver(fs->settings, fs->synth);
    if (!fs->adriver) {
        fprintf(stderr, "Failed to create audio driver.\n");
        pdelete_fluid_settings(fs->settings);
        free(fs);
        return ERR;
    }
    return NO_ERR;
}

_Err cmusiclab_fluidsynth_new_midi_driver(fluidsynth_t *fs)
{
    fs->router = pnew_fluid_midi_router(fs->settings, pfluid_synth_handle_midi_event, (void *) fs->synth);
    if (!fs->router) {
        fprintf(stderr, "Failed to create MIDI router.\n");
        return ERR;
    }
    fs->mdriver = pnew_fluid_midi_driver(fs->settings, pfluid_midi_router_handle_midi_event, (void *) fs->router);
    if (!fs->mdriver) {
        fprintf(stderr, "Failed to create MIDI driver.\n");
        return ERR;
    }
    return NO_ERR;
}

void cmusiclab_fluidsynth_delete_midi_driver(fluidsynth_t *fs)
{
    if (fs->mdriver) {
        pdelete_fluid_midi_driver(fs->mdriver);
        fs->mdriver = NULL;
    }
    if (fs->router) {
        pdelete_fluid_midi_router(fs->router);
        fs->router = NULL;
    }
}

int cmusiclab_fluidsynth_sfcount(fluidsynth_t *fs)
{
    return pfluid_synth_sfcount(fs->synth);
}

int cmusiclab_fluidsynth_sfload(fluidsynth_t *fs, const char *filename)
{
    int sfont_id;
    printf("SF file: %s\n", filename);
    sfont_id = pfluid_synth_sfload(fs->synth, filename, 1);
    if (sfont_id == FLUID_FAILED) {
        fprintf(stderr, "Failed to load sound font file.\n");
        return FLUID_FAILED;
    }
    return sfont_id;
}

_Err cmusiclab_fluidsynth_sfunload(fluidsynth_t *fs, int sfont_id)
{
    fprintf(stderr, "cmusiclab_fluidsynth_sfunload\n");
    int err = pfluid_synth_sfunload(fs->synth, sfont_id, 0);
    if (err == FLUID_FAILED) {
        fprintf(stderr, "Failed to unload sound font.\n");
        return ERR;
    }
    return NO_ERR;
}

_Err cmusiclab_fluidsynth_new_cmd_handler(fluidsynth_t *fs)
{
    cmusiclab_fluidsynth_delete_cmd_handler(fs);
    fs->cmd_handler = pnew_fluid_cmd_handler2(fs->settings, fs->synth, fs->router, NULL);
    if (!fs->cmd_handler) {
        fprintf(stderr, "Failed to create command handler.\n");
        return ERR;
    }
    return NO_ERR;
}

void cmusiclab_fluidsynth_delete_cmd_handler(fluidsynth_t *fs)
{
    if (fs->cmd_handler) {
        pdelete_fluid_cmd_handler(fs->cmd_handler);
        fs->cmd_handler = NULL;
    }
}

_Err cmusiclab_fluidsynth_shell_command(fluidsynth_t *fs, const char *cmd, char *result, int num_chars)
{
    int pipefd[2];
    int stdout_backup;
    ssize_t bytes_read;

    // Create a pipe
    if (pipe(pipefd) == -1) {
        return ERR;
    }

    // Backup the current stdout
    stdout_backup = dup(STDOUT_FILENO);
    if (stdout_backup == -1) {
        close(pipefd[0]);
        close(pipefd[1]);
        return ERR;
    }

    // Redirect stdout to the write end of the pipe
    if (dup2(pipefd[1], STDOUT_FILENO) == -1) {
        close(pipefd[0]);
        close(pipefd[1]);
        return ERR;
    }

    // Close the write end of the pipe as we don't need it anymore
    close(pipefd[1]);

    // Execute the command
    _Err err = pfluid_command(fs->cmd_handler, cmd, STDOUT_FILENO);

    // Restore stdout
    fflush(stdout); // Ensure all data is flushed before restoring
    dup2(stdout_backup, STDOUT_FILENO);
    close(stdout_backup);

    // Read from the read end of the pipe into the result buffer
    bytes_read = read(pipefd[0], result, num_chars - 1); // Leave space for null terminator
    if (bytes_read < 0) {
        close(pipefd[0]);
        return ERR;
    }

    // Null-terminate the string
    result[bytes_read] = '\0';

    // Close the read end of the pipe
    close(pipefd[0]);

    return err; // Return the status code from pfluid_command
}
