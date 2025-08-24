import argparse
import math
from dataclasses import dataclass


@dataclass
class NewConfig:
    newMouseSens: float
    normalCoef: float
    tallCoef: float

    def print(self):
        return (
            f"New Minecraft mouseSensitivity: {self.newMouseSens}\n"
            f"New normal sensitivity coefficient (waywall): {self.normalCoef}\n"
            f"New tall sensitivity coefficient (waywall): {self.tallCoef}"
        )


def mc_effective_sens(s: float) -> float:
    """
    Minecraft's nonlinear effective sensitivity function.
    The game computes: f = s * 0.6 + 0.2; result = (f^3) * 8
    """
    return (0.6 * s + 0.2) ** 3 * 8.0


def visible_vfov(v_deg: float, display_h: int, fb_h: int) -> float:
    """
    Visible vertical FOV (deg) with cropped framebuffer.
    display_h = actual visible window height (pixels)
    fb_h = framebuffer height (pixels)
    """
    k = display_h / fb_h
    return math.degrees(2 * math.atan(math.tan(math.radians(v_deg) / 2) * k))


def calcSens(
    currentMouseSens: float,
    currentNormalCoef: float = 1.0,
    normalResolution: tuple[int, int] = (1920, 1080),
    tallResolution: tuple[int, int] = (384, 16384),
    newMouseSens: float = 0.02291165,
    v_fov: float = 30.0,
    currentTallCoef: float | None = None,
) -> NewConfig:
    """
    Compute new Waywall sensitivity coefficients given a lower Minecraft in-game sensitivity.
    If currentTallCoef is None, compute it from the resolution ratio.
    """
    # Step 1: compute Minecraft's nonlinear effective sensitivities
    eff_old = mc_effective_sens(currentMouseSens)
    eff_new = mc_effective_sens(newMouseSens)
    scale = eff_old / eff_new

    # Step 2: rescale normal coefficient
    new_normal = currentNormalCoef * scale

    # Step 3: tall coefficient
    if currentTallCoef is None:
        # derive from vertical FOV shrink
        vfov_normal = visible_vfov(v_fov, normalResolution[1], normalResolution[1])
        vfov_tall = visible_vfov(v_fov, normalResolution[1], tallResolution[1])
        Z = vfov_normal / vfov_tall
        new_tall = new_normal / Z
    else:
        new_tall = currentTallCoef * scale

    return NewConfig(
        newMouseSens=newMouseSens, normalCoef=new_normal, tallCoef=new_tall
    )


def main():
    # currentMouseSens = 0.058765005
    # currentNormalCoef = 5.73718
    currentMouseSens = 0.3371454
    currentNormalCoef = 1.0
    normalRes = (1920, 1080)
    tallRes = (384, 16384)
    # normalRes = (2560, 1440)
    # tallRes = (384, 16384)

    cfg = calcSens(
        currentMouseSens,
        currentNormalCoef,
        normalRes,
        tallRes,
        newMouseSens=0.02291165,
        v_fov=30.0,
        currentTallCoef=None,
    )  # None = auto-compute

    print(cfg)


def cli():
    parser = argparse.ArgumentParser(
        description="Calculate new Waywall sensitivity coefficients."
    )
    parser.add_argument(
        "currentMouseSens", type=float, help="Current mouse sensitivity"
    )
    parser.add_argument(
        "currentNormalCoef", type=float, help="Current normal sensitivity coefficient"
    )
    parser.add_argument(
        "--normalRes",
        type=int,
        nargs=2,
        default=(1920, 1080),
        help="Normal resolution (width height)",
    )
    parser.add_argument(
        "--tallRes",
        type=int,
        nargs=2,
        default=(384, 16384),
        help="Tall resolution (width height)",
    )
    parser.add_argument(
        "--newMouseSens",
        type=float,
        default=0.02291165,
        help="New mouse sensitivity",
    )
    parser.add_argument(
        "--vFov", type=float, default=30.0, help="Vertical FOV in degrees"
    )
    parser.add_argument(
        "--currentTallCoef",
        type=float,
        default=None,
        help="Current tall sensitivity coefficient (if not provided, it will be computed from resolutions)",
    )

    args = parser.parse_args()

    cfg = calcSens(
        args.currentMouseSens,
        args.currentNormalCoef,
        tuple(args.normalRes),
        tuple(args.tallRes),
        args.newMouseSens,
        args.vFov,
        args.currentTallCoef,
    )

    print(cfg.print())


def testVisibleVFOV():
    print(f"30, 1080, 1080: {visible_vfov(30, 1080, 1080)}")
    print(f"30, 1080, 16384: {visible_vfov(30, 1080, 16384)}")
    print(f"30, 540, 1080: {visible_vfov(30, 540, 1080)}")
    print(f"30, 540, 16384: {visible_vfov(30, 540, 16384)}")


if __name__ == "__main__":
    cli()
