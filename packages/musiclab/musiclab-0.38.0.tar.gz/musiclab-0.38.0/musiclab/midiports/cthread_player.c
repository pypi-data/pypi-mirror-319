#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include "cthread_player.h"
#include "cplayer_live.h"

const char *RTMIDI_PATH;

static int _cmusiclab_player_thread_synchronous_worker(PlayerState *player_state)
{
    while (player_state->is_playing && !player_state->terminate) {
        cmusiclab_live_player_array_sweep(player_state);
    }
    return 0;
}

static void *_cmusiclab_player_thread_event_loop(void *arg)
{
    PlayerState *player_state = (PlayerState *) arg;

    while (true) {
        pthread_mutex_lock(&player_state->mutex);
        while (!player_state->is_playing && !player_state->terminate) {
            // printf("Waiting for condition.\n");
            pthread_cond_wait(&player_state->cond, &player_state->mutex);
            // printf("Condition met.\n");
        }
        if (player_state->terminate) {
            pthread_mutex_unlock(&player_state->mutex);
            break;
        }
        pthread_mutex_unlock(&player_state->mutex);
        _cmusiclab_player_thread_synchronous_worker(player_state);
    }

    printf("Player loop terminated.\n");
    return NULL;
}

PlayerState *cmusiclab_player_thread_create()
{
    PlayerState *player_state;
    player_state = cmusiclab_live_player_create_state(1);
    if (player_state == NULL) {
        LOGERR("Player state was not created.\n");
        return NULL;
    }
    cmusiclab_live_player_init_state(player_state);
    _Err err = pthread_create(&player_state->thread, NULL, _cmusiclab_player_thread_event_loop, (void *) player_state);
    if (err != 0) {
        LOGERR("Error creating player thread: %d.\n", err);
        return NULL;
    }
    return player_state;
}

_Err cmusiclab_player_thread_join(PlayerState *player_state)
{
    if (pthread_join(player_state->thread, NULL) != 0) {
        fprintf(stderr, "Error joining player thread.\n");
        return 2;
    }
    cmusiclab_live_player_destroy_state(&player_state);
    return NO_ERR;
}

void cmusiclab_player_thread_playpause(PlayerState *player_state)
{
    pthread_mutex_lock(&player_state->mutex);
    player_state->is_playing = !player_state->is_playing;
    pthread_cond_signal(&player_state->cond);
    pthread_mutex_unlock(&player_state->mutex);
}

void cmusiclab_player_thread_restart(PlayerState *player_state)
{
    pthread_mutex_lock(&player_state->mutex);
    cmusiclab_live_player_restart_state(player_state);
    pthread_cond_signal(&player_state->cond);
    pthread_mutex_unlock(&player_state->mutex);
}

void cmusiclab_player_thread_terminate(PlayerState *player_state)
{
    pthread_mutex_lock(&player_state->mutex);
    player_state->terminate = true;
    player_state->is_playing = true;
    pthread_cond_signal(&player_state->cond);
    pthread_mutex_unlock(&player_state->mutex);
}
