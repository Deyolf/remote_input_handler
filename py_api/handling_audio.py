from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(vol_percentage):
    scalar_value = vol_percentage / 100.0
    volume.SetMasterVolumeLevelScalar(scalar_value, None)
    c_volume = float(volume.GetMasterVolumeLevelScalar())
    return c_volume

def current_volume():
    c_volume = float(volume.GetMasterVolumeLevelScalar())
    return c_volume