#include <signal.h>
#include "crtmidi.h"
#include "cmidi.h"
#include "cmidiconst.h"
#include "cmidi_codec.h"
#include "player_utils.h"

static volatile sig_atomic_t user_ctrl_C = 0;

void sigint_handler(int signo)
{
    if (signo == SIGINT) {
        user_ctrl_C = 1;
    }
}

_Err cmusiclab_rtmidi_play_simple(RtMidiOutPtr port, MidiRow *table, long num_rows)
{
    long i;
    MidiRow *row;
    double delta;
    signal(SIGINT, sigint_handler);
    int tempo = cbpm2tempo(120);
    const unsigned char *data;
    for (i = 0; i < num_rows; i++) {
        row = &table[i];
        if (row->delta > 0) {
            delta = ctick2second(row->delta, tempo, _DEFAULT_TICKS_PER_BEAT);
            sleep_sec(delta);
        }
        if (user_ctrl_C) {
            return ERR;
        }
        if (is_channel_status(row->status)) {
            data = bytes_ptr(row->data);
            cmusiclab_rtmidi_out_send_message(port, data, bytes_size(row->data));
        }
        else if (row->status == _TEMPO_SET) {
            tempo = row->pitch;
        }
    }
    return NO_ERR;
}
