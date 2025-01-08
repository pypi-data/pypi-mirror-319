#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include "crtmidi.h"

#define PATH_MAX    (1024)

/* rtmidi_c.h declarations */
static const char* ( *prtmidi_get_version ) ( void );

static int            ( *prtmidi_get_compiled_api )    ( enum RtMidiApi *apis, unsigned int apis_size );
static const char*    ( *prtmidi_api_name )            ( enum RtMidiApi api );
static const char*    ( *prtmidi_api_display_name )    ( enum RtMidiApi api );

static RtMidiOutPtr   ( *prtmidi_out_create_default )  ( void );
static RtMidiOutPtr   ( *prtmidi_out_create )          ( enum RtMidiApi api, const char* clientName );
static void           ( *prtmidi_out_free )            ( RtMidiOutPtr device );
static enum RtMidiApi ( *prtmidi_out_get_current_api ) ( RtMidiPtr device );

static unsigned int   ( *prtmidi_get_port_count )      ( RtMidiPtr device );
static int            ( *prtmidi_get_port_name )       ( RtMidiPtr device, unsigned int portNumber,
                                                         char * bufOut, int * bufLen );

static void           ( *prtmidi_open_port )           ( RtMidiPtr device, unsigned int portNumber, const char *portName );
static void           ( *prtmidi_open_virtual_port )   ( RtMidiPtr device, const char *portName );
static void           ( *prtmidi_close_port )          ( RtMidiPtr device );
static int            ( *prtmidi_out_send_message )    ( RtMidiOutPtr device,
                                                         const unsigned char *message, int length);

static RtMidiInPtr    ( *prtmidi_in_create_default )   ( void );
static RtMidiInPtr    ( *prtmidi_in_create )           ( enum RtMidiApi api, const char* clientName, unsigned int queueSizeLimit );
static void           ( *prtmidi_in_free )             ( RtMidiInPtr device );
static enum RtMidiApi ( *prtmidi_in_get_current_api )  ( RtMidiPtr device );
static void           ( *prtmidi_in_set_callback )     ( RtMidiInPtr device, RtMidiCCallback callback, void *userData );
static void           ( *prtmidi_in_cancel_callback )  ( RtMidiInPtr device );
static void           ( *prtmidi_in_ignore_types )     ( RtMidiInPtr device, bool midiSysex, bool midiTime, bool midiSense );
static double         ( *prtmidi_in_get_message )      ( RtMidiInPtr device, unsigned char *message, size_t *size );

/* --------------------- */
void *dl_rtmidi;

_Err cmusiclab_rtmidi_init(const char *rtmidi_lib_path)
{
    LOGDBG("librtmidi path %s\n", rtmidi_lib_path);
    dl_rtmidi = dlopen(rtmidi_lib_path, RTLD_NOW | RTLD_GLOBAL);
    if (!dl_rtmidi) {
        LOGERR("dlopen error: %s\n", dlerror());
        goto fn_fail;
    }

    prtmidi_get_version = dlsym(dl_rtmidi, "rtmidi_get_version");
    if (dlerror() != NULL) {
        goto fn_fail;
    }

    prtmidi_get_compiled_api    = dlsym(dl_rtmidi, "rtmidi_get_compiled_api");
    prtmidi_api_name            = dlsym(dl_rtmidi, "rtmidi_api_name");
    prtmidi_api_display_name    = dlsym(dl_rtmidi, "rtmidi_api_display_name");
    prtmidi_out_create_default  = dlsym(dl_rtmidi, "rtmidi_out_create_default");
    prtmidi_out_create          = dlsym(dl_rtmidi, "rtmidi_out_create");
    prtmidi_out_free            = dlsym(dl_rtmidi, "rtmidi_out_free");
    prtmidi_out_get_current_api = dlsym(dl_rtmidi, "rtmidi_out_get_current_api");
    prtmidi_get_port_count      = dlsym(dl_rtmidi, "rtmidi_get_port_count");
    prtmidi_get_port_name       = dlsym(dl_rtmidi, "rtmidi_get_port_name");
    prtmidi_open_port           = dlsym(dl_rtmidi, "rtmidi_open_port");
    prtmidi_open_virtual_port   = dlsym(dl_rtmidi, "rtmidi_open_virtual_port");
    prtmidi_close_port          = dlsym(dl_rtmidi, "rtmidi_close_port");
    prtmidi_out_send_message    = dlsym(dl_rtmidi, "rtmidi_out_send_message");
    prtmidi_in_create_default   = dlsym(dl_rtmidi, "rtmidi_in_create_default");
    prtmidi_in_create           = dlsym(dl_rtmidi, "rtmidi_in_create");
    prtmidi_in_free             = dlsym(dl_rtmidi, "rtmidi_in_free");
    prtmidi_in_get_current_api  = dlsym(dl_rtmidi, "rtmidi_in_get_current_api");
    prtmidi_in_set_callback     = dlsym(dl_rtmidi, "rtmidi_in_set_callback");
    prtmidi_in_cancel_callback  = dlsym(dl_rtmidi, "rtmidi_in_cancel_callback");
    prtmidi_in_ignore_types     = dlsym(dl_rtmidi, "rtmidi_in_ignore_types");
    prtmidi_in_get_message      = dlsym(dl_rtmidi, "rtmidi_in_get_message");

    return NO_ERR;
fn_fail:
    dl_rtmidi = NULL;
    return ERR;
}

void cmusiclab_rtmidi_deinit()
{
    prtmidi_get_version         = NULL;
    prtmidi_get_compiled_api    = NULL;
    prtmidi_api_name            = NULL;
    prtmidi_api_display_name    = NULL;
    prtmidi_out_create_default  = NULL;
    prtmidi_out_create          = NULL;
    prtmidi_out_free            = NULL;
    prtmidi_out_get_current_api = NULL;
    prtmidi_get_port_count      = NULL;
    prtmidi_get_port_name       = NULL;
    prtmidi_open_port           = NULL;
    prtmidi_open_virtual_port   = NULL;
    prtmidi_close_port          = NULL;
    prtmidi_out_send_message    = NULL;
    prtmidi_in_create_default   = NULL;
    prtmidi_in_create           = NULL;
    prtmidi_in_free             = NULL;
    prtmidi_in_get_current_api  = NULL;
    prtmidi_in_set_callback     = NULL;
    prtmidi_in_cancel_callback  = NULL;
    prtmidi_in_ignore_types     = NULL;
    prtmidi_in_get_message      = NULL;

    dlclose(dl_rtmidi);
    dl_rtmidi = NULL;
}

int cmusiclab_rtmidi_is_initialized()
{
    if (dl_rtmidi != NULL)
        return 1;
    return 0;
}

const char* cmusiclab_rtmidi_get_version(void)
{
    return prtmidi_get_version();
}

_Err cmusiclab_rtmidi_get_compiled_api_names(const char ***papi_names, int *api_count)
{
    int num_apis = prtmidi_get_compiled_api(NULL, 0);
    enum RtMidiApi *apis = (enum RtMidiApi *) malloc(num_apis * sizeof(enum RtMidiApi));
    const char **api_names = (const char **) malloc(num_apis * sizeof(const char *));
    num_apis = prtmidi_get_compiled_api(apis, num_apis);
    if (num_apis < 0) {
        goto fn_fail;
    }
    int i;
    for (i = 0; i < num_apis; i++) {
        api_names[i] = prtmidi_api_display_name(apis[i]);
    }
    *papi_names = api_names;
    *api_count = num_apis;
    return NO_ERR;
fn_fail:
    return ERR;
}

RtMidiOutPtr cmusiclab_rtmidi_out_create_default()
{
    return prtmidi_out_create_default();
}

RtMidiOutPtr cmusiclab_rtmidi_out_create(enum RtMidiApi api, const char *clientName)
{
    return prtmidi_out_create(api, clientName);
}

enum RtMidiApi cmusiclab_rtmidi_out_get_current_api(RtMidiPtr device)
{
    return prtmidi_out_get_current_api(device);
}

void cmusiclab_rtmidi_out_free(RtMidiOutPtr device)
{
    prtmidi_out_free(device);
}

unsigned int cmusiclab_rtmidi_port_count(RtMidiPtr device)
{
    return prtmidi_get_port_count(device);
}

void cmusiclab_rtmidi_get_port_name(RtMidiPtr device, int portNumber, char **pstring)
{
    int buf_len;
    int retval = prtmidi_get_port_name(device, portNumber, NULL, &buf_len);
    if (retval < 0) {
        *pstring = NULL;
        return;
    }
    char *name = (char *) malloc(buf_len * sizeof(char));
    retval = prtmidi_get_port_name(device, portNumber, name, &buf_len);
    *pstring = name;
}

void cmusiclab_rtmidi_open_port(RtMidiPtr device, unsigned int port_num, const char *portName)
{
    prtmidi_open_port(device, port_num, portName);
}

void cmusiclab_rtmidi_open_virtual_port(RtMidiPtr device, const char *portName)
{
    prtmidi_open_virtual_port(device, portName);
}

void cmusiclab_rtmidi_close_port(RtMidiPtr device)
{
    prtmidi_close_port(device);
}

void cmusiclab_rtmidi_out_send_message(RtMidiOutPtr device, const unsigned char *message, int length)
{
    prtmidi_out_send_message(device, message, length);
}

RtMidiInPtr cmusiclab_rtmidi_in_create_default()
{
    return prtmidi_in_create_default();
}

RtMidiInPtr cmusiclab_rtmidi_in_create(enum RtMidiApi api, const char *clientName, unsigned int queueSize)
{
    return prtmidi_in_create(api, clientName, queueSize);
}

void cmusiclab_rtmidi_in_free(RtMidiPtr device)
{
    prtmidi_in_free(device);
}

enum RtMidiApi cmusiclab_rtmidi_in_get_current_api(RtMidiPtr device)
{
    return prtmidi_in_get_current_api(device);
}

void test_callback(double time_stamp, const unsigned char *msg, size_t len, void *usr_data)
{
    fprintf(stderr, "Test callback: %lf\t", time_stamp);
    size_t i;
    for (i=0; i<len; i++)
        fprintf(stderr, "%d ", msg[i]);
    fprintf(stderr, "\n");
}

void cmusiclab_rtmidi_in_set_test_callback(RtMidiPtr device)
{
    prtmidi_in_set_callback(device, test_callback, NULL);
}

void cmusiclab_rtmidi_in_cancel_callback(RtMidiPtr device)
{
    prtmidi_in_cancel_callback(device);
}
