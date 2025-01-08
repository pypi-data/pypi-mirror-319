"""""" # start delvewheel patch
def _delvewheel_patch_1_8_0():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'openmeeg.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_8_0()
del _delvewheel_patch_1_8_0
# end delvewheel patch

from importlib.metadata import version as _version
import warnings as _warnings

from . import _distributor_init

# https://github.com/swig/swig/issues/2881
with _warnings.catch_warnings():
    _warnings.simplefilter("ignore")
    from ._openmeeg_wrapper import HeadMat  # noqa
    del HeadMat


# Here we import as few things as possible to keep our API as limited as
# possible
from ._openmeeg_wrapper import (
    HeadMat,
    Sensors,
    Integrator,
    Head2EEGMat,
    Head2MEGMat,
    DipSourceMat,
    DipSource2MEGMat,
    GainEEG,
    GainMEG,
    GainEEGadjoint,
    GainMEGadjoint,
    GainEEGMEGadjoint,
    Forward,
    SurfSourceMat,
    SurfSource2MEGMat,
    Matrix,
    SymMatrix,
)
from ._make_geometry import make_geometry, make_nested_geometry, read_geometry
from ._utils import get_log_level, set_log_level, use_log_level

try:
    __version__ = _version("openmeeg")
except Exception:
    __version__ = "0.0.0"
del _version

# https://github.com/swig/swig/issues/2881
with _warnings.catch_warnings():
    _warnings.simplefilter("ignore")
    set_log_level("warning")
