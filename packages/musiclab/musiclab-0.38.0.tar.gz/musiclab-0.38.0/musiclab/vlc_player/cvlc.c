#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <dlfcn.h>
#include <unistd.h>
#include "cvlc.h"

#define PATH_MAX    (1024)

/* libVLC declarations */
typedef int       (*libvlc_media_open_cb) (void *opaque, void **datap, uint64_t *sizep);
typedef ptrdiff_t (*libvlc_media_read_cb) (void *opaque, unsigned char *buf, size_t len);
typedef int       (*libvlc_media_seek_cb) (void *opaque, uint64_t offset);
typedef void      (*libvlc_media_close_cb)(void *opaque);

libvlc_instance_t*     ( *plibvlc_new ) ( int argc , const char *const *argv );
void                   ( *plibvlc_release ) ( libvlc_instance_t *p_instance );

libvlc_media_player_t* ( *plibvlc_media_player_new ) ( libvlc_instance_t *p_libvlc_instance );
void                   ( *plibvlc_media_player_release) ( libvlc_media_player_t *p_mi );
void                   ( *plibvlc_media_player_set_media ) ( libvlc_media_player_t *p_mi, libvlc_media_t *p_md );
int                    ( *plibvlc_media_player_is_playing ) ( libvlc_media_player_t *p_mi );
int                    ( *plibvlc_media_player_play ) ( libvlc_media_player_t *p_mi );
void                   ( *plibvlc_media_player_pause ) ( libvlc_media_player_t *p_mi );
void                   ( *plibvlc_media_player_stop ) ( libvlc_media_player_t *p_mi );
int                    ( *plibvlc_audio_get_volume ) ( libvlc_media_player_t *p_mi );
int                    ( *plibvlc_audio_set_volume ) ( libvlc_media_player_t *p_mi, int i_volume );

libvlc_media_t*        ( *plibvlc_media_new_path ) (
                            libvlc_instance_t *p_instance,
                            const char *path );
libvlc_media_t*        ( *plibvlc_media_new_callbacks )(
                            libvlc_instance_t *instance,
                            libvlc_media_open_cb open_cb,
                            libvlc_media_read_cb read_cb,
                            libvlc_media_seek_cb seek_cb,
                            libvlc_media_close_cb close_cb,
                            void *opaque );
void                   ( *plibvlc_media_release )( libvlc_media_t *p_md );
libvlc_media_t*        ( *plibvlc_media_new_path )( libvlc_instance_t *p_instance, const char *path );
libvlc_media_t*        ( *plibvlc_media_new_location )( libvlc_instance_t *p_instance, const char * psz_mrl );

void *dl_vlccore, *dl_vlc;

static int dlopen_vlc(const char* vlclibdir)
{
    char libvlccore[PATH_MAX], libvlc[PATH_MAX];
#if defined __APPLE__
    snprintf(libvlccore, PATH_MAX, "%s/libvlccore.dylib", vlclibdir);
    snprintf(libvlc, PATH_MAX, "%s/libvlc.dylib", vlclibdir);
#elif defined(__linux__)
    snprintf(libvlccore, PATH_MAX, "%s/libvlccore.so", vlclibdir);
    snprintf(libvlc, PATH_MAX, "%s/libvlc.so", vlclibdir);
#endif

    dl_vlccore = dlopen(libvlccore, RTLD_NOW | RTLD_GLOBAL);
    if (!dl_vlccore) {
        goto fn_fail;
    }
    dl_vlc = dlopen(libvlc, RTLD_NOW | RTLD_GLOBAL);
    if (!dl_vlc) {
        goto fn_fail;
    }

    plibvlc_new = dlsym(dl_vlc, "libvlc_new");
    if (dlerror() != NULL) {
        goto fn_fail;
    }

    plibvlc_release = dlsym(dl_vlc, "libvlc_release");

    plibvlc_media_player_new = dlsym(dl_vlc, "libvlc_media_player_new");
    if (dlerror() != NULL) {
        goto fn_fail;
    }

    plibvlc_media_player_new = dlsym(dl_vlc, "libvlc_media_player_new");

    plibvlc_media_player_release = dlsym(dl_vlc, "libvlc_media_player_release");

    plibvlc_media_player_set_media = dlsym(dl_vlc, "libvlc_media_player_set_media");

    plibvlc_media_player_is_playing = dlsym(dl_vlc, "libvlc_media_player_is_playing");

    plibvlc_media_player_play = dlsym(dl_vlc, "libvlc_media_player_play");

    plibvlc_media_player_pause = dlsym(dl_vlc, "libvlc_media_player_pause");

    plibvlc_media_player_stop = dlsym(dl_vlc, "libvlc_media_player_stop");

    plibvlc_media_new_path = dlsym(dl_vlc, "libvlc_media_new_path");

    plibvlc_media_new_callbacks = dlsym(dl_vlc, "libvlc_media_new_callbacks");

    plibvlc_media_release = dlsym(dl_vlc, "libvlc_media_release");

    plibvlc_media_new_path = dlsym(dl_vlc, "libvlc_media_new_path");

    plibvlc_media_new_location = dlsym(dl_vlc, "libvlc_media_new_location");

    plibvlc_audio_get_volume = dlsym(dl_vlc, "libvlc_audio_get_volume");

    plibvlc_audio_set_volume = dlsym(dl_vlc, "libvlc_audio_set_volume");

    return NO_ERR;
fn_fail:
    return ERR;
}

static int vlc_cbytes_open_cb(void *opaque, void **datap, uint64_t *sizep)
{
    cBytes cbytes = (cBytes) opaque;
    *datap = cbytes;
    *sizep = (uint64_t) bytes_size(cbytes);
    return 0;
}

static ptrdiff_t vlc_cbytes_read_cb(void *opaque, unsigned char *buf, size_t len)
{
    _Err err;
    cBytes cbytes = (cBytes) opaque;
    size_t remaining = bytes_size(cbytes) - bytes_tell(cbytes);
    ptrdiff_t toread = (len < remaining) ? len : remaining;
    if (toread > 0) {
        err = bytes_read(cbytes, (int) toread, buf);
        if (err != NO_ERR) {
            return -1;
        }
        return toread;
    }
    return 0;
}

static int vlc_cbytes_seek_cb(void *opaque, uint64_t offset)
{
    cBytes cbytes = (cBytes) opaque;
    _Err err = bytes_seek(cbytes, (long int) offset, SEEK_SET);
    return err;
}

static void vlc_cbytes_close_cb(void *opaque)
{
    cBytes cbytes = (cBytes) opaque;
    bytes_seek(cbytes, 0, SEEK_SET);
}

static libvlc_media_t* vlc_media_new_cbytes(libvlc_instance_t *inst, cBytes obj)
{
    return plibvlc_media_new_callbacks(
        inst,
        vlc_cbytes_open_cb,
        vlc_cbytes_read_cb,
        vlc_cbytes_seek_cb,
        vlc_cbytes_close_cb,
        (void *) obj);
}

libvlc_instance_t* cmusiclab_vlc_instance_new()
{
    int argc = 1;
    char *argv[] = {"--quiet"};
    return plibvlc_new(argc, (const char *const *) argv);
}

void cmusiclab_vlc_instance_release(libvlc_instance_t *inst)
{
    plibvlc_release(inst);
}

_Err cmusiclab_vlc_init(const char *vlc_lib_path, const char *vlc_plugin_path)
{
    setenv("VLC_PLUGIN_PATH", vlc_plugin_path, 1);
    _Err err = dlopen_vlc(vlc_lib_path);
    if (err) return err;
    return NO_ERR;
}

int cmusiclab_vlc_is_initialized()
{
    if (dl_vlccore != NULL && dl_vlc != NULL)
        return 1;
    return 0;
}

void cmusiclab_vlc_deinit()
{
    if (dl_vlc) {
        dlclose(dl_vlc);
        dl_vlc = NULL;
    }
    if (dl_vlccore) {
        dlclose(dl_vlccore);
        dl_vlccore = NULL;
    }
}

libvlc_media_player_t *cmusiclab_vlc_player_new(libvlc_instance_t *inst)
{
    return plibvlc_media_player_new(inst);
}

void cmusiclab_vlc_player_release(libvlc_media_player_t *player)
{
    plibvlc_media_player_release(player);
}

void cmusiclab_vlc_player_cbytes_load(libvlc_instance_t *inst, libvlc_media_player_t *player, cBytes obj)
{
    libvlc_media_t *media = vlc_media_new_cbytes(inst, obj);
    plibvlc_media_player_set_media(player, media);
    plibvlc_media_release(media);
}

_Err cmusiclab_vlc_player_file_load(libvlc_instance_t *inst, libvlc_media_player_t *player, const char *path)
{
    libvlc_media_t *media = plibvlc_media_new_path(inst, path);
    if (media == NULL) {
        return ERR;
    }
    plibvlc_media_player_set_media(player, media);
    plibvlc_media_release(media);
    return NO_ERR;
}

_Err cmusiclab_vlc_player_url_load(libvlc_instance_t *inst, libvlc_media_player_t *player, const char *url)
{
    libvlc_media_t *media = plibvlc_media_new_location(inst, url);
    if (media == NULL) {
        return ERR;
    }
    plibvlc_media_player_set_media(player, media);
    plibvlc_media_release(media);
    return NO_ERR;
}

_Err cmusiclab_vlc_play(libvlc_media_player_t *player)
{
    if (plibvlc_media_player_play(player))
        return ERR;
    return NO_ERR;
}

int cmusiclab_vlc_is_playing(libvlc_media_player_t *player)
{
    return plibvlc_media_player_is_playing(player);
}

_Err cmusiclab_vlc_play_blocking(libvlc_media_player_t *player)
{
    int err = plibvlc_media_player_play(player);
    if (err != 0)
        return ERR;
    do {
        usleep(100000);
    } while(plibvlc_media_player_is_playing(player));
    return NO_ERR;
}

void cmusiclab_vlc_pause(libvlc_media_player_t *player)
{
    plibvlc_media_player_pause(player);
}

void cmusiclab_vlc_stop(libvlc_media_player_t *player)
{
    plibvlc_media_player_stop(player);
}

int cmusiclab_vlc_get_volume(libvlc_media_player_t *player)
{
    return plibvlc_audio_get_volume(player);
}

_Err cmusiclab_vlc_set_volume(libvlc_media_player_t *player, int vol_pct)
{
    return plibvlc_audio_set_volume(player, vol_pct);
}
