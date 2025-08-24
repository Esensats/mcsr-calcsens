# EyeZoom sensitivity calculator

When using Ninjabrain Bot with a 16384 pixels tall Minecraft window, you'll
notice that your sensitivity feels very high, and it's very difficult to make
small adjustments. The rotational sensitivity remains the same, but perceived
sensitivity is much higher due to zoomed in view. Also, the minimum angle
increment might also feel too high.

This calculator helps you find a configuration that feels similar to the
sensitivity you're used to, while conforming to
[this list](https://github.com/Ninjabrain1/Ninjabrain-Bot/wiki/Boat-measurements).
The default target `mouseSensitivity` is `0.02291165`, because it is very small and
has a small error. The calculator gives you waywall sensitivities (for both
normal gameplay and EyeZoom tall window). The EyeZoom tall sensitivity
coefficient is the one you set with `waywall.set_sensitivity` when you change
the resolution to 16384 pixels tall.

## Usage

1. Write down your current `mouseSensitivity` from `options.txt` or `standardsettings.json`. Let's say it's `0.5` (displayed as 100% in-game)
2. Write down your current `sensitivity` in waywall's config. Let's say it's `1.0`.
3. Use this tool as the following:

```sh
python calcsens.py 0.5 1.0 # 0.5 is Minecraft sensitivity, 1.0 is waywall sensitivity
# Output:
# New Minecraft mouseSensitivity: 0.02291165
# New normal sensitivity coefficient (waywall): 21.822959062311096
# New tall sensitivity coefficient (waywall): 1.4721637642674297
```

4. Set your Minecraft `mouseSensitivity` to the new value (`0.02291165` in this example)
5. Set your waywall `sensitivity` to the new normal sensitivity coefficient (around `21.823` in this example). Example:

```lua
local waywall = require("waywall")

local config = {
	input = {
    --- ...
		sensitivity = 14.715,
	},
  -- ...
}

--- ...

return config
```

6. Add `waywall.set_sensitivity(1.472)` to the line where you change the resolution to 16384 pixels tall in lua. Example:

```lua
local tall_enable = function()
  -- Set resolution to 384x16384...
  -- Turn on the needed mirrors...
	waywall.set_sensitivity(0.9926665158627155)
end
```

7. Add `waywall.set_sensitivity(0)` to the line where you change the resolution back to normal (when it's 0, waywall uses the normal sensitivity coefficient). Example:

```lua
local tall_disable = function()
  -- Set resolution back to normal...
  -- Turn off the mirrors...
  waywall.set_sensitivity(0)
end
```

Done! You should now have a similar perceived sensitivity feeling in both
normal and EyeZoom tall window modes and your muscle memory is saved,
while also having a sensitivity suitable for precise boat measurements.

## Other options

Use the `--help` flag to see other options:

```sh
python calcsens.py --help
# Output:
# usage: calcsens.py [-h] [--normalRes NORMALRES NORMALRES] [--tallRes TALLRES TALLRES] [--newMouseSens NEWMOUSESENS]
#                    [--vFov VFOV] [--currentTallCoef CURRENTTALLCOEF]
#                    currentMouseSens currentNormalCoef
#
# Calculate new Waywall sensitivity coefficients.
#
# positional arguments:
#   currentMouseSens      Current Minecraft mouseSensitivity
#   currentNormalCoef     Current sensitivity in waywall
#
# options:
#   -h, --help            show this help message and exit
#   --normalRes NORMALRES NORMALRES
#                         Normal resolution (width height). Default is 1920x1080
#   --tallRes TALLRES TALLRES
#                         Tall resolution (width height). Default is 384x16384
#   --newMouseSens NEWMOUSESENS
#                         New mouse sensitivity. Default is 0.02291165
#   --vFov VFOV           Vertical FOV in degrees. Default is 30
#   --currentTallCoef CURRENTTALLCOEF
#                         Current tall sensitivity coefficient (if not provided, it will be computed from resolutions)
```
