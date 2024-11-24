import ctypes

# Define a estrutura POINT usada pelo Windows para representar coordenadas (x, y)
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_position():
    """Obtém a posição atual do mouse."""
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y
