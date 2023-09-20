from enum import Enum

class WarningMessage(Enum):
    CONFIRM_BEFORE_SEND = "Tienes que confirmar antes de enviar."
    DETECT_BEFORE_SEND = "Tienes que detectar antes de enviar."
    INPUT_PACKAGE_NUMBER = "Tienes que ingresar el número del paquete antes de enviar."
    NOT_MODIFY_AFTER_CONFIRM = "No puede modificar el programa luego de confirmar."
    NOT_STICKS_DETECTED = "No se detectó ningun palo."
    INFORMATION_NOT_STORED_IN_SERVER = "La informaciòn no pudo ser guardada en el servidor."
