#include <stdlib.h>
#include <pthread.h>
#include "cmidi.h"
#include "cmidiconst.h"
#include "cmidi_codec.h"
#include "utils.h"
#include "player_utils.h"
#include "cplayer_live.h"
#include <stdio.h>

#define i1E9 (1000000000L)
#define f1E9 (1E9)

CTime ctime_now()
{
    CTime time_now;
    clock_gettime(CLOCK_REALTIME, &time_now);
    return time_now;
}

CTime ctime_add(CTime t1, CTime t2)
{
    CTime result;
    result.tv_sec = t1.tv_sec + t2.tv_sec;
    result.tv_nsec = t1.tv_nsec + t2.tv_nsec;
    // Normalize the result in case tv_nsec exceeds f1E9
    if (result.tv_nsec >= i1E9) {
        result.tv_sec += result.tv_nsec / i1E9;
        result.tv_nsec = result.tv_nsec % i1E9;
    }
    return result;
}

CTime ctime_diff(CTime t1, CTime t2)
{
    CTime result;
    result.tv_sec = t1.tv_sec - t2.tv_sec;
    if (t1.tv_nsec >= t2.tv_nsec) {
        result.tv_nsec = t1.tv_nsec - t2.tv_nsec;
    } else {
        // Borrow one second if t1.tv_nsec is less than t2.tv_nsec
        result.tv_sec -= 1;
        result.tv_nsec = i1E9 + t1.tv_nsec - t2.tv_nsec;
    }
    return result;
}

CTime ctime_mul(CTime t, double factor)
{
    CTime result;
    double total_nsec = (t.tv_sec * f1E9 + t.tv_nsec) * factor;
    result.tv_sec = (time_t)(total_nsec / f1E9);
    result.tv_nsec = (long)(total_nsec - result.tv_sec * f1E9);
    return result;
}

CTime second_to_ctime(double seconds)
{
    CTime result;
    result.tv_sec = (time_t)seconds;
    result.tv_nsec = (long)((seconds - result.tv_sec) * f1E9);
    return result;
}

double ctime_to_second(CTime ctime)
{
    return ctime.tv_sec + ctime.tv_nsec / f1E9;
}

bool ctime_less_than(CTime t1, CTime t2)
{
    if (t1.tv_sec < t2.tv_sec) {
        return true;
    } else if (t1.tv_sec == t2.tv_sec && t1.tv_nsec < t2.tv_nsec) {
        return true;
    }
    return false;
}

bool ctime_equals(CTime t1, CTime t2)
{
    return (t1.tv_sec == t2.tv_sec && t1.tv_nsec == t2.tv_nsec);
}

PlayerState *cmusiclab_live_player_create_state(int num_tables)
{
    PlayerState *pl_state = (PlayerState *) calloc (1, sizeof(PlayerState));
    if (!pl_state) {
        return NULL;
    }
    player_item_t *pl_items = (player_item_t *) calloc (num_tables, sizeof(player_item_t));
    if (!pl_items) {
        free(pl_state);
        return NULL;
    }
    pl_state->items = pl_items;
    pl_state->num_tables = num_tables;

    return pl_state;
}

void cmusiclab_live_player_init_state(PlayerState *pl_state)
{
    pl_state->tempo = cbpm2tempo(120.0);
    pl_state->is_playing = false;
    pl_state->terminate = false;
    pthread_mutex_init(&pl_state->mutex, NULL);
    pthread_cond_init(&pl_state->cond, NULL);
}

void cmusiclab_live_player_restart_state(PlayerState *pl_state)
{
    int i;
    player_item_t *item;
    for (i = 0; i < pl_state->num_tables; i++) {
        item = &pl_state->items[i];
        item->current_row = 0;
        item->loop_counter = 0;
    }
    pl_state->is_playing = false;
}

void cmusiclab_live_player_destroy_state(PlayerState **p_pl_state)
{
    if (!p_pl_state || !(*p_pl_state)) {
        return;
    }
    PlayerState *pl_state = *p_pl_state;
    pthread_mutex_destroy(&pl_state->mutex);
    pthread_cond_destroy(&pl_state->cond);
    free(pl_state->items);
    free(pl_state);
    *p_pl_state = NULL;
}

_Err cmusiclab_live_player_array_insert_item(PlayerState* pl_state, int position, RtMidiPtr port, MidiRow *table, long num_rows, int num_loop)
{
    if (position < 0 || position > pl_state->num_tables) {
        return ERR;
    }
    player_item_t *item = &pl_state->items[position];
    pthread_mutex_lock(&pl_state->mutex);
    item->midiport = port;
    item->table = table;
    item->num_rows = num_rows;
    item->current_row = 0;
    item->tstart = (CTime) { 0, 0 };
    item->sleep_sec = 0.0;
    item->num_loop = num_loop;
    item->loop_counter = 0;
    pthread_mutex_unlock(&pl_state->mutex);
    return NO_ERR;
}

_Err cmusiclab_live_player_array_sweep(PlayerState *pl_state)
{
    if (!pl_state) {
        return ERR;
    }
    int i;
    player_item_t *item;
    RtMidiOutPtr port;
    MidiRow *table;
    MidiRow *row;
    double delta;
    cBytes cbytes;
    const unsigned char *data;

    for (i = 0; i < pl_state->num_tables; i++) {
        item = &pl_state->items[i];
        port = item->midiport;
        if (!item->table) {
            continue;
        }
        if (item->current_row >= item->num_rows) {
            if (item->loop_counter < item->num_loop - 1) {
                item->loop_counter ++;
                item->current_row = 0;
                continue;
            }
            item->current_row = item->loop_counter = 0;
            pl_state->is_playing = false;
            break;
        }

        table = item->table;
        row = &table[item->current_row];
        if (row->delta) {
            delta = ctick2second(row->delta, pl_state->tempo, _DEFAULT_TICKS_PER_BEAT);
            CTime delta_ts = second_to_ctime(delta);
            clock_gettime(CLOCK_REALTIME, &(item->tstart));
            item->tend = ctime_add(item->tstart, delta_ts);
            sleep_sec(delta);
        }
        print_row(row);
        if (is_channel_status(row->status)) {
            cbytes = row->data;
            data = bytes_ptr(cbytes);
            cmusiclab_rtmidi_out_send_message(port, data, bytes_size(cbytes));
        }
        else if (i == 0 && row->status == _TEMPO_SET) {
            pl_state->tempo = row->pitch;
            fprintf(stdout, "Tempo set to: %d\n", pl_state->tempo);
        }
        item->current_row++;
    }
    return NO_ERR;
}
