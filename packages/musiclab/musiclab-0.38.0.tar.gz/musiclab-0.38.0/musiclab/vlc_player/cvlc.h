#ifndef __CVLC_H__
#define __CVLC_H__

#include "cbytearray.h"

typedef void libvlc_instance_t;
typedef void libvlc_media_player_t;
typedef void libvlc_media_t;

_Err                   cmusiclab_vlc_init(const char *vlc_lib_path, const char *vlc_plugin_path);
void                   cmusiclab_vlc_deinit(void);
int                    cmusiclab_vlc_is_initialized(void);
libvlc_instance_t*     cmusiclab_vlc_instance_new(void);
void                   cmusiclab_vlc_instance_release(libvlc_instance_t *inst);
libvlc_media_player_t* cmusiclab_vlc_player_new(libvlc_instance_t *inst);
void                   cmusiclab_vlc_player_release(libvlc_media_player_t *player);
void                   cmusiclab_vlc_player_cbytes_load(libvlc_instance_t *inst, libvlc_media_player_t *player, cBytes obj);
_Err                   cmusiclab_vlc_player_file_load(libvlc_instance_t *inst, libvlc_media_player_t *player, const char *path);
_Err                   cmusiclab_vlc_player_url_load(libvlc_instance_t *inst, libvlc_media_player_t *player, const char *url);
_Err                   cmusiclab_vlc_play(libvlc_media_player_t *player);
int                    cmusiclab_vlc_is_playing(libvlc_media_player_t *player);
_Err                   cmusiclab_vlc_play_blocking(libvlc_media_player_t *player);
void                   cmusiclab_vlc_pause(libvlc_media_player_t *player);
void                   cmusiclab_vlc_stop(libvlc_media_player_t *player);
int                    cmusiclab_vlc_get_volume(libvlc_media_player_t *player);
_Err                   cmusiclab_vlc_set_volume(libvlc_media_player_t *player, int vol_pct);

#endif  // __CVLC_H__