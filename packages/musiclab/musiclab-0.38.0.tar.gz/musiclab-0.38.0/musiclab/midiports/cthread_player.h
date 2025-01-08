#ifndef __CTHREAD_PLAYER_H__
#define __CTHREAD_PLAYER_H__

#include "cplayer_live.h"

PlayerState *cmusiclab_player_thread_create(void);
_Err         cmusiclab_player_thread_join(PlayerState *player_state);
void         cmusiclab_player_thread_playpause(PlayerState *player_state);
void         cmusiclab_player_thread_restart(PlayerState *player_state);
void         cmusiclab_player_thread_terminate(PlayerState *player_state);

#endif  // __CTHREAD_PLAYER_H__
