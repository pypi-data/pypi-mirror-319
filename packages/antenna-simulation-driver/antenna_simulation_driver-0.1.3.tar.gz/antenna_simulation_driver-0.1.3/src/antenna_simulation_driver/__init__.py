from subprocess import PIPE, run

from antenna_simulation_driver.necpp_output_parser import (
    Nec2ppOutput,
    parse_nec2pp_output,
)

_INFINITY = float("Infinity")


def swr(z: complex, z0: complex = 50) -> float:
    """Calculate the SWR of the impedance z relative to the base impedance z0."""
    if z == _INFINITY:
        return _INFINITY
    else:
        abs_reflection_factor = abs((z - z0) / (z + z0))
        if 1 == abs_reflection_factor:
            return _INFINITY
        else:
            return (1 + abs_reflection_factor) / (1 - abs_reflection_factor)


def run_nec2pp(stdin: str) -> Nec2ppOutput:
    """Run nec2++, feed it the stdin text, and parse the result."""
    run_result = run(
        ["nec2++", "-i", "-", "-o", "-"],
        text=True,
        input=stdin,
        check=True,
        stdout=PIPE,
    )
    return parse_nec2pp_output(run_result.stdout.splitlines())
