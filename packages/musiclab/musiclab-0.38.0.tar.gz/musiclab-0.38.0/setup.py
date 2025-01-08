from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy
import os, json

include_dirs = ['musiclab/fluidmidi/cside']
extra_compile_args = []
extra_compile_args += ['-Wall', '-Wextra']
# extra_compile_args += ['-O2']
extra_compile_args += ['-g', '-O0', '-DMUSICLAB_CDEBUG']

DISTRIBUTE_INT_FLUIDSYNTH = True
CYTHONIZE_EVERYTHING      = True

PACKAGE_DATA = {
    'musiclab': ['manage/settings.json',
                 'theory/theory_data.json',
                 'kbdsynth/user_profile.json'],
}

ext_bytearray = Extension(
    'musiclab.fluidmidi.pyside.bytearray',
    sources=[
        'musiclab/fluidmidi/pyside/bytearray.pyx',
        'musiclab/fluidmidi/cside/cbytearray.c',
    ],
    include_dirs=include_dirs,
    extra_compile_args=extra_compile_args,
)

ext_midi = Extension(
    'musiclab.fluidmidi.pyside.midi',
    sources=[
        'musiclab/fluidmidi/pyside/midi.pyx',
        'musiclab/fluidmidi/cside/cmidi.c',
        'musiclab/fluidmidi/cside/cmidi_codec.c',
        'musiclab/fluidmidi/cside/ctable_printer.c',
        'musiclab/fluidmidi/cside/cbytearray.c',
        'musiclab/fluidmidi/cside/cmidiconst.c'
    ],
    include_dirs=[numpy.get_include()] + include_dirs,
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    extra_compile_args=extra_compile_args,
)

ext_vlc = Extension(
    'musiclab.vlc_player',
    sources=[
        'musiclab/vlc_player/vlc.pyx',
        'musiclab/vlc_player/cvlc.c',
        'musiclab/fluidmidi/cside/cbytearray.c',
    ],
    include_dirs=include_dirs,
    extra_compile_args=extra_compile_args,
)

ext_midiports = Extension(
    'musiclab.midiports.midi_io',
    sources = [
        'musiclab/midiports/midi_io.pyx',
        'musiclab/midiports/crtmidi.c',
        'musiclab/midiports/player.c',
        'musiclab/fluidmidi/cside/cbytearray.c',
        'musiclab/fluidmidi/cside/cmidi.c',
        'musiclab/fluidmidi/cside/cmidi_codec.c',
        'musiclab/fluidmidi/cside/cmidiconst.c',
        'musiclab/midiports/cthread_player.c',
        'musiclab/midiports/cplayer_live.c',
        'musiclab/fluidmidi/cside/ctable_printer.c',
    ],
    include_dirs=[numpy.get_include()] + include_dirs,
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    extra_compile_args=extra_compile_args,
)

def pkg_data_ensure_librtmidi(pkg_data):
    module_midiports = os.path.join('musiclab', 'midiports')
    with open(os.path.join('musiclab', 'manage', 'settings.json')) as f:
        data = json.load(f)
    int_rtmidi_version = data['INT_RTMIDI_VERSION']
    found_lib = None
    for ext in ('dylib', 'dll', 'so'):
        fname = f'librtmidi.{int_rtmidi_version}.{ext}'
        int_rtmidi = os.path.join(module_midiports, fname)
        if os.path.exists(int_rtmidi):
            found_lib = fname
            break
    if not found_lib:
        raise FileNotFoundError('Need to run ensure_rtmidilib.py first')
    pkg_data['musiclab'] += [os.path.join('midiports', found_lib)]
    return pkg_data

ext_fs = Extension(
    'musiclab.fluidsynth.fsynth',
    sources=[
        'musiclab/fluidsynth/fsynth.pyx',
        'musiclab/fluidsynth/cfsynth.c'
    ],
    include_dirs=include_dirs,
    extra_compile_args=extra_compile_args,
)

def pkg_data_ensure_libfluidsynth(pkg_data):
    if not DISTRIBUTE_INT_FLUIDSYNTH:
        return pkg_data
    module_fluidsynth = os.path.join('musiclab', 'fluidsynth')
    libfluidsynthpath = os.path.join(module_fluidsynth, 'libfluidsynth')
    if not os.path.exists(libfluidsynthpath):
        raise FileNotFoundError('libfluidsynth not found. Please run ensure_libfluidsynth.py first')
    paths = []
    for (path, directories, filenames) in os.walk(libfluidsynthpath):
        relative_path = os.path.relpath(path, libfluidsynthpath)
        for filename in filenames:
            paths.append(os.path.join('fluidsynth', 'libfluidsynth', relative_path, filename))
    pkg_data['musiclab'] += paths
    return pkg_data

# Compile python modules to C extensions
py_modules = [
    'musiclab.extras.datamapping',
    'musiclab.kbdsynth.kb_mapping',
    'musiclab.kbdsynth.kbd_synth',
    'musiclab.kbdsynth.tk_mapping',
    'musiclab.kbdsynth.tk_mapping',
    'musiclab.manage.cli',
    'musiclab.manage.settings',
    'musiclab.manage.apps.audio_devices',
    'musiclab.manage.apps.kbd_synth_main',
    'musiclab.manage.apps.kbd_synth_tkapp',
    'musiclab.manage.apps.midiports',
    'musiclab.manage.apps.soundfont',
    'musiclab.tkui.components',
    'musiclab.tkui.main_menu',
    'musiclab.tkui.tk_user_profile',
    'musiclab.tkui.tkroot',
    'musiclab.tkui.utils',
    'musiclab.theory.music_theory',
    'musiclab.theory.parsers',
]

def make_py_ext_modules(modules):
    return [
        Extension(module,
                  sources=[f"{module.replace('.', '/')}.py"])
        for module in modules
    ]

binary_modules = [ext_bytearray, ext_midi, ext_vlc, ext_midiports, ext_fs]

PACKAGE_DATA = pkg_data_ensure_libfluidsynth(pkg_data_ensure_librtmidi(PACKAGE_DATA))

if CYTHONIZE_EVERYTHING:
    binary_modules += make_py_ext_modules(py_modules)
    packages = ['musiclab']
else:
    packages = find_packages(
        include=['musiclab',
                 'musiclab.manage',
                 'musiclab.manage.apps',
                 'musiclab.extras',
                 'musiclab.fluidsynth',
                 'musiclab.midiports',
                 'musiclab.theory',
                 'musiclab.kbdsynth',
                 'musiclab.tkui',
                 ]
    )

setup(
    name = 'musiclab',
    version = '0.38.0',
    description = 'Python application for music composition and production.',
    author = 'Anustuv Pal',
    author_email = 'anustuv@gmail.com',
    ext_modules=cythonize(binary_modules),
    install_requires=['numpy', 'modgrammar', 'pynput', 'setproctitle'],
    packages=packages,
    package_data=PACKAGE_DATA,
    entry_points = {
        'console_scripts': [
           'musiclab = musiclab.manage.cli:main'
        ]
    },
)
