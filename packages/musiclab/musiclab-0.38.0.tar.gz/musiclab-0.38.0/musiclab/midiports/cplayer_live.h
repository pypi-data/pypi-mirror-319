#ifndef __CPLAYER_LIVE_H__
#define __CPLAYER_LIVE_H__

#include <stdbool.h>
#include <pthread.h>
#include "player_utils.h"
#include "cmidi_types.h"
#include "crtmidi.h"

typedef struct timespec CTime;
CTime  ctime_now();
CTime  ctime_add(CTime t1, CTime t2);
CTime  ctime_diff(CTime t1, CTime t2);
CTime  ctime_mul(CTime t, double factor);
CTime  second_to_ctime(double seconds);
double ctime_to_second(CTime ctime);
bool   ctime_less_than(CTime t1, CTime t2);
bool   ctime_equals(CTime t1, CTime t2);

typedef struct player_item_s {
    MidiRow  *table;
    long      num_rows;
    long      current_row;
    CTime     tstart;
    double    sleep_sec;
    CTime     tend;
    int       num_loop;  // -1 could be infinite loop
    int       loop_counter;
    RtMidiOutPtr  midiport;
} player_item_t;

typedef struct player_thread_s{
    player_item_t  *items;
    int             num_tables;
    int             tempo;
    CTime           tpaused;
    volatile bool   is_playing;
    volatile bool   terminate;
    pthread_t       thread;
    pthread_mutex_t mutex;
    pthread_cond_t  cond;
} PlayerState;

PlayerState *cmusiclab_live_player_create_state(int num_tables);
void         cmusiclab_live_player_init_state(PlayerState *pl_state);
void         cmusiclab_live_player_destroy_state(PlayerState **pitem_array);
_Err         cmusiclab_live_player_array_insert_item(PlayerState* player_items, int position, RtMidiOutPtr port, MidiRow *table, long num_rows, int num_loop);
void         cmusiclab_live_player_restart_state(PlayerState *pl_state);
_Err         cmusiclab_live_player_array_sweep(PlayerState *pl_state);

#endif  // __CPLAYER_LIVE_H__
