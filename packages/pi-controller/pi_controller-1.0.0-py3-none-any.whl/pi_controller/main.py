import evdev
import time
from typing import Callable


def list_devices() -> list[str]:
    return [evdev.InputDevice(d).name for d in evdev.list_devices()]

class UnsupportedControllerError(Exception): pass

class Key:
    def __init__(self, name: str, code: int):
        self.name: str = name
        self.code: int = code

        self.pressed = False

    def __str__(self):
        return f"{self.name}: {self.pressed}"
    
    def __bool__(self):
        return self.pressed
    
class RawJoystick:
    def __init__(self, name, code, max_val):
        self.name = name
        self.code = code

        self.value = 0
        self.max_val = max_val
    
    @property
    def p_val(self):
        return self.value/self.max_val

    def __str__(self):
        return self.name
    
    
class Joystick:
    def __init__(self, name: str, x: RawJoystick, y: RawJoystick):
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    @property
    def value(self):
        return self.x.value, self.y.value
    @property
    def p_val(self):
        return self.x.p_val, self.y.p_val

class ProController:
    BUTTONS = ("A", "B", "X", "Y", "CAPTURE", "L", "R", "ZL", "ZR", "MINUS", "PLUS", "HOME", "LSTICK", "RSTICK")
    JOYSTICKS = ("LJOY_X", "LJOY_Y", "RJOY_X", "RJOY_Y", "DPAD_X", "DPAD_Y")

    VENDOR_ID = 0x057e
    PRODUCT_ID = 0x2009

    def __init__(self, index, check_controller=True, min_pause_time=0):
        # setup
        try:
            self._device = evdev.InputDevice(evdev.list_devices()[index])
        except IndexError as e:
            raise IndexError(f"Invalid index, no available controller with index `{index}`. Available devices are {evdev.list_devices()}") from e
        
        print(self._device.name)
        print(self._device.info)
        if check_controller and not (self.VENDOR_ID == self._device.info.vendor and self.PRODUCT_ID == self._device.info.product):
            raise UnsupportedControllerError("The given device is not a Nintendo Switch Pro Controller. Skip this check by setting `check_controller` to `False`")

        self.active = False
        self._event_que = []

        self.min_pause_time = min_pause_time

        # mapings
        self.buttons = (
            Key("A", 305),
            Key("B", 304),
            Key("X", 307),
            Key("Y", 308),
            Key("CAPTURE", 309),
            Key("L", 310),
            Key("R", 311),
            Key("ZL", 312),
            Key("ZR", 313),
            Key("MINUS", 314),
            Key("PLUS", 315),
            Key("HOME", 316),
            Key("LSTICK", 317),
            Key("RSTICK", 318),
        )
        self.raw_joysticks = (
            RawJoystick("LJOY_X", 0, 32767),
            RawJoystick("LJOY_Y", 1, 32767),
            RawJoystick("RJOY_X", 3, 32767),
            RawJoystick("RJOY_Y", 4, 32767),

            RawJoystick("DPAD_X", 16, 1),
            RawJoystick("DPAD_Y", 17, 1)
        )

        self.joysticks = (
            Joystick("LEFT", self.raw_joysticks[0], self.raw_joysticks[1]),
            Joystick("RIGHT", self.raw_joysticks[2], self.raw_joysticks[3]),
            Joystick("DPAD", self.raw_joysticks[4], self.raw_joysticks[5])
        )


        # event storage (starts with `_on`)
        self._on_press_events: list[Callable[[Key], None]] = []
        self._on_release_events: list[Callable[[Key], None]] = []
        self._on_v_press_events: dict[str, Callable[[None], None]] = {}
        self._on_v_release_events: dict[str, Callable[[None], None]]  = {}

        self._on_every_loop: list[Callable[[None], None]] = []

        self._on_abs_events: list[Callable[[str, int], None]] = []
        self._on_v_abs_events: dict[str, Callable[[int], None]] = {}


    # useful
    def button_from_code(self, code: int):
        for b in self.buttons:
            if b.code == code:
                return b
        raise ValueError(f'No button maps to code: `code`')
    
    def raw_joystick_from_code(self, code: int):
        for j in self.raw_joysticks:
            if j.code == code:
                return j
        raise ValueError(f'No joystick maps to code: `code`')


    # process
    def _read(self):       
        try:
            for event in self._device.read():
                if event.type == evdev.ecodes.EV_SYN:
                    self._process()
                else:
                    self._event_que.append(event)
        except BlockingIOError:
            for f in self._on_every_loop:
                f()

    def _process(self):
        for event in self._event_que:
            if event.type == evdev.ecodes.EV_KEY:
                button = self.button_from_code(event.code)
                button.pressed = bool(event.value)

                if button.pressed:
                    for f in self._on_press_events:
                        f(button)

                    for b, f in self._on_v_press_events.items():
                        if button.name == b:
                            f()
                else:
                    for f in self._on_release_events:
                        f(button)

                    for b, f in self._on_v_release_events.items():
                        if button.name == b:
                            f()

            elif event.type == evdev.ecodes.EV_ABS:
                joystick = self.raw_joystick_from_code(event.code)
                joystick.value = event.value

                for f in self._on_abs_events:
                    f(joystick, event.value)

                for j, f in self._on_v_abs_events.items():
                    if j == joystick.name:
                        f(event.value)

            else:
                print(f"Unrecognised event type: {event.type}")

        for f in self._on_every_loop:
            f()
        self._event_que = []

    def run(self):
        self.active = True
        while self.active:
            t = time.time()
            self._read()
            d = time.time() - t
            if d < self.min_pause_time:
                time.sleep(self.min_pause_time - d)


    def stop(self):
        self.active = False



    # decorators (all start with `on`)
    def on_key_press(self, func):
        self._on_press_events.append(func)
    def on_key_release(self, func):
        self._on_release_events.append(func)

    def on_v_key_press(self, key: str):
        if key not in self.BUTTONS:
            raise ValueError(f"Invalid Key: {key}")
        else:
            return lambda func: self._on_v_press_events.__setitem__(key, func)
    def on_v_key_release(self, key: str):
        if key not in self.BUTTONS:
            raise ValueError(f"Invalid Key: {key}")
        else:
            return lambda func: self._on_v_release_events.__setitem__(key, func)
        
    def on_every_loop(self, func):
        self._on_every_loop.append(func)

    def on_abs_event(self, func):
        self._on_abs_events.append(func)
    def on_v_abs_event(self, joystick: str):
        if joystick not in self.JOYSTICKS:
            raise ValueError(f"Invalid Joystick: {joystick}")
        else:
            return lambda func: self._on_v_abs_events.__setitem__(joystick, func)
        


    # in progress...
    def rumble(self, duration, strong:int, weak, repeat=1):
        effect = evdev.ff.Effect(
            evdev.ecodes.FF_RUMBLE, -1, 0,
            evdev.ff.Trigger(0, 0),
            evdev.ff.Replay(duration, 0),
            evdev.ff.EffectType(
                ff_rumble_effect=evdev.ff.Rumble(
                    strong_magnitude=strong, 
                    weak_magnitude=weak # 0xfff
                    ))
        )
        e_id = self._device.upload_effect(effect),
        self._device.write(
            evdev.ecodes.EV_FF,
            e_id,
            repeat
        )
        time.sleep(duration/1000)
        self._device.erase_effect(e_id)
    
    # properties
    @property
    def a(self): return self.buttons[0]
    @property
    def b(self): return self.buttons[1]
    @property
    def x(self): return self.buttons[2]
    @property
    def y(self): return self.buttons[3]
    @property
    def capture(self): return self.buttons[4]
    @property
    def l(self): return self.buttons[5]
    @property
    def r(self): return self.buttons[6]
    @property
    def zl(self): return self.buttons[7]
    @property
    def zr(self): return self.buttons[8]
    @property
    def minus(self): return self.buttons[9]
    @property
    def plus(self): return self.buttons[10]
    @property
    def home(self): return self.buttons[11]
    @property
    def lstick(self): return self.buttons[12]
    @property
    def rstick(self): return self.buttons[13]

    @property
    def left_joystick(self): return self.joysticks[0]
    @property
    def right_joystick(self): return self.joysticks[1]

    @property
    def dpad(self): return self.joysticks[2]
    @property
    def dpad_up(self): return self.dpad.y.value == -1
    @property
    def dpad_down(self): return self.dpad.y.value == 1
    @property
    def dpad_left(self): return self.dpad.x.value == -1
    @property
    def dpad_right(self): return self.dpad.x.value == 1




if __name__ == "__main__":
    pro = ProController(0)
    print(pro._device.capabilities())
    pro.run()