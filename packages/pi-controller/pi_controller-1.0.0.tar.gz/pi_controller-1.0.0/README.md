# PiController
This is a project to connect a nintendo pro controller to a raspberry pi. 
I initially did this with pygame [here](https://github.com/PreciousFood/pro_controller), but this is better suited for the pi. That project is multiplatform though, whereas this makes use of evdev, which is only available on linux. 

# Documentation

## Overview

The `ProController` module provides an abstraction for interfacing with a Nintendo Switch Pro Controller via the `evdev` library in Python. It includes classes and utilities for handling buttons, joysticks, and events, as well as support for vibration feedback.

---

## Table of Contents

1. [Installation](#installation)
2. [Classes](#classes)
   - [ProController](#1-procontroller)
   - [RawJoystick](#2-rawjoystick)
   - [Joystick](#3-joystick)
   - [Key](#1-key)
3. [Additional Functions](#additional-functions)
4. [Usage](#usage)
5. [Examples](#examples)
6. [Requirements](#requirements)

---

## Installation

1. Install the python development headers, a dependency for evdev, the one and only dependency of this library.
    ```bash
    sudo apt install python3-dev
    ```
2. Install pi_controller (inside a virtual environment is recomended)
    ```bash
    pip install pi_controller
    ```
    or clone from github
    ```bash
    git clone https://github.com/PreciousFood/pi_controller.git
    ```

## Classes

### 1. `ProController`
Represents the Nintendo Switch Pro Controller. Handles button and joystick inputs, event processing, and vibration feedback.

#### Initialization:
```python
ProController(index: int, check_controller: bool = True, min_pause_time: float = 0)
```

- `index`: Index of the controller in the list of devices. See [list_devices](#1-list_devices) to figure out what the correct index is.
- `check_controller`: If `True`, validates the controller as a Pro Controller.
- `min_pause_time`: Minimum time between event loops.

#### Attributes:
- `BUTTONS`: Tuple of button names.
- `JOYSTICKS`: Tuple of joystick names.
- `buttons`: List of `Key` objects representing controller buttons.
- `raw_joysticks`: List of `RawJoystick` objects for joystick axes.
- `joysticks`: List of `Joystick` objects for grouped joystick axes.

#### Methods:
- `run()`: Starts the event loop to process input.
- `stop()`: Stops the event loop.
- `button_from_code(code: int) -> Key`: Maps a hardware code to a `Key`.
- `raw_joystick_from_code(code: int) -> RawJoystick`: Maps a hardware code to a `RawJoystick`.

#### Event Handlers:
- `on_key_press(func: Callable[[Key], None])`: Adds a callback for button press events.
- `on_key_release(func: Callable[[Key], None])`: Adds a callback for button release events.
- `on_v_key_press(key: str)`: Adds a callback for a specific button press.
- `on_v_key_release(key: str)`: Adds a callback for a specific button release.
- `on_every_loop(func: Callable)`: Adds a callback for every event loop iteration.
- `on_abs_event(func: Callable[[RawJoystick, int], None])`: Adds a callback for joystick movement events.
- `on_v_abs_event(joystick: str)`: Adds a callback for a specific joystick movement.

#### Vibration:
> Experimental feature, not fully implemented yet
- `rumble(duration: int, strong: int, weak: int, repeat: int = 1)`: Triggers vibration feedback.

#### Properties:
- Button aliases (`a`, `b`, `x`, etc.).
- Joystick aliases (`left_joystick`, `right_joystick`, `dpad).
- D-pad directional properties (`dpad_up`, `dpad_down`, etc.).
>Note: Because of how evdev handles the dpad, it is technically a joystick with values of -1, 0, or 1. The D-pad directional properties handle this to be a simple bool

---

### 2. `RawJoystick`
Represents a raw axis of a joystick.

#### Attributes:
- `name` (str): Name of the axis.
- `code` (int): Hardware code for the axis.
- `value` (int): Current raw value of the axis.
- `max_val` (int): Maximum possible value for the axis.

#### Properties:
- `p_val` (float): Normalized value of the axis (`value / max_val`).

#### Methods:
- `__str__()`: Returns the name of the axis.

---

### 3. `Joystick`
Represents a joystick with two axes (X and Y).

#### Attributes:
- `name` (str): Name of the joystick.
- `x` (`RawJoystick`): X-axis of the joystick.
- `y` (`RawJoystick`): Y-axis of the joystick.

#### Properties:
- `value` (tuple[int, int]): Tuple of raw X and Y values.
- `p_val` (tuple[float, float]): Tuple of normalized X and Y values.

#### Methods:
- `__str__()`: Returns the joystick name.

---

### 1. `Key`
Represents a single button on the controller.

#### Attributes:
- `name` (str): Name of the button.
- `code` (int): Hardware code for the button.
- `pressed` (bool): State of the button (`True` if pressed, `False` otherwise).

#### Methods:
- `__str__()`: Returns the name of the button and whether it is pressed.
- `__bool__()`: Returns the `pressed` state.


## Additional Functions

### 1. list_devices
Lists the names of all available devices, the index of the device you want is the index to pass to `ProController`.

Returns a list of strings.

## Usage

1. **Initialize the Controller:**
   ```python
   from pro_controller import ProController

   pro = ProController(index=0)
   ```

2. **Register Event Handlers:**
   ```python
   @pro.on_key_press
   def on_button_press(key):
       print(f"{key} pressed")
   ```

3. **Start the Event Loop:**
   ```python
   pro.run()
   ```

4. **Stop the Controller:**
   ```python
   pro.stop()
   ```

---

## Examples

### Button Press Example:
```python
pro = ProController(0)

@pro.on_key_press
def handle_press(button):
    print(f"Button {button.name} was pressed!")

pro.run()
```

### Joystick Movement Example:
```python
pro = ProController(0)

@pro.on_abs_event
def handle_joystick(joystick, value):
    print(f"{joystick.name} moved to {value}")

pro.run()
```