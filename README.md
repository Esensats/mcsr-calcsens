# EyeZoom sensitivity calculator

When using Ninjabrain Bot with a 16384 pixels tall Minecraft window, you'll notice that your sensitivity feels very high, and it's very difficult to make small adjustments. The rotational sensitivity remains the same, but perceived sensitivity is much higher due to zoomed in view.

This calculator helps you find a configuration that feels similar to the sensitivity you're used to, while conforming to [this list](https://github.com/Ninjabrain1/Ninjabrain-Bot/wiki/Boat-measurements). The default target mouseSensitivity is 0.02291165, because it is very small and has a small error. The calculator gives you waywall sensitivities (for both normal gameplay and EyeZoom tall window). The EyeZoom tall sensitivity coefficient is the one you set with `waywall.set_sensitivity` when you change the resolution to 16384 pixels tall.
