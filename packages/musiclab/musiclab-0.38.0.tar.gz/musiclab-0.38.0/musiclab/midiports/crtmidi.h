#ifndef __CRTMIDI_H__
#define __CRTMIDI_H__

#include "cmidi_types.h"

#include <stdbool.h>

enum RtMidiApi {
    RTMIDI_API_UNSPECIFIED,
    RTMIDI_API_MACOSX_CORE,
    RTMIDI_API_LINUX_ALSA,
    RTMIDI_API_UNIX_JACK,
    RTMIDI_API_WINDOWS_MM,
    RTMIDI_API_RTMIDI_DUMMY,
    RTMIDI_API_WEB_MIDI_API,
    RTMIDI_API_WINDOWS_UWP,
    RTMIDI_API_ANDROID,
    RTMIDI_API_NUM
};

struct RtMidiWrapper {
    void *ptr;
    void *data;
    bool ok;
    const char* msg;
};

typedef struct RtMidiWrapper* RtMidiPtr;
typedef struct RtMidiWrapper* RtMidiInPtr;
typedef struct RtMidiWrapper* RtMidiOutPtr;

typedef void          ( *RtMidiCCallback )             ( double timeStamp, const unsigned char* message,
                                                         size_t messageSize, void *userData);

_Err cmusiclab_rtmidi_init(const char *rtmidi_lib_path);
void cmusiclab_rtmidi_deinit(void);
int  cmusiclab_rtmidi_is_initialized();
const char* cmusiclab_rtmidi_get_version(void);
_Err cmusiclab_rtmidi_get_compiled_api_names(const char ***papi_names, int *api_count);

RtMidiOutPtr cmusiclab_rtmidi_out_create_default(void);
void cmusiclab_rtmidi_out_free(RtMidiOutPtr device);
enum RtMidiApi cmusiclab_rtmidi_out_get_current_api(RtMidiPtr device);
unsigned int cmusiclab_rtmidi_port_count(RtMidiPtr device);
void cmusiclab_rtmidi_get_port_name(RtMidiPtr device, int portNumber, char **pstring);

void cmusiclab_rtmidi_open_port(RtMidiPtr device, unsigned int port_num, const char *portName);
void cmusiclab_rtmidi_open_virtual_port(RtMidiPtr device, const char *portName);
void cmusiclab_rtmidi_close_port(RtMidiPtr device);
void cmusiclab_rtmidi_out_send_message(RtMidiOutPtr device, const unsigned char *message, int length);

RtMidiInPtr cmusiclab_rtmidi_in_create_default(void);
RtMidiInPtr cmusiclab_rtmidi_in_create(enum RtMidiApi api, const char *clientName, unsigned int queueSize);
void cmusiclab_rtmidi_in_free(RtMidiPtr device);
enum RtMidiApi cmusiclab_rtmidi_in_get_current_api(RtMidiPtr device);
void cmusiclab_rtmidi_in_set_test_callback(RtMidiPtr device);
void cmusiclab_rtmidi_in_cancel_callback(RtMidiPtr device);

_Err cmusiclab_rtmidi_play_simple(RtMidiOutPtr port, MidiRow *table, long num_rows);

RtMidiInPtr cmusiclab_rtmidi_in_create_default(void);

#endif  // __CRTMIDI_H__
