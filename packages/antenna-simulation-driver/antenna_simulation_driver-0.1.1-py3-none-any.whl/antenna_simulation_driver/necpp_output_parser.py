import logging
import re
from dataclasses import dataclass
from enum import Enum, StrEnum, unique
from typing import Iterable, Tuple, Union, cast

EOF = [value for value in StrEnum("_END_OF_FILE_ENUM", ["⇥"])][0]
logger = logging.getLogger(__name__)


@dataclass
class AntennaInputParameters:
    tag: int
    seg: int
    voltage: complex
    current: complex
    impedance: complex
    admittance: complex
    power: float


@dataclass
class SegmentCenter:
    """Values are in wavelengths, not in meter."""

    x: float
    y: float
    z: float


@dataclass
class SegmentCurrent:
    """A segment and the current that flows through it."""

    seg: int
    tag: int
    seg_center: SegmentCenter
    seg_length: float
    current: complex
    current_magnitude: float
    current_phase: float


class NecOutputParsingError(Exception):
    """To be raised when the output of nec2++ cannot be parsed by this code."""

    pass


class _InputPeek:
    """An internal helper class for parsing."""

    def __init__(self, lines: Iterable[str]):
        """Need an iterable of lines.

        A file opened for text input does nicely."""
        self._line: str
        self._lines = iter(lines)
        self.next_line()

    def peek(self) -> str:
        """Show the next line to be processed, without line ending.

        Returns nec2pp_output_parser.EOF on end of data.
        """
        return self._line

    def next_line_is_empty(self) -> bool:
        """Return whether the next line is empty (only space, or length 0).

        Not to be called after EOF has been reached.
        """
        return 0 == len(self._line) or self._line.isspace()

    def skip_empty_lines(self) -> None:
        """Ignore as many empty lines as there may be present."""
        while self._line is not EOF and self.next_line_is_empty():
            self.next_line()

    def expect_line(self, line: str) -> None:
        """Expect a specific line, raising an exception if something else is encountered."""
        if line != self.peek():
            raise NecOutputParsingError(f'Found: "{self.peek()}", expected: "{line}".')
        else:
            self.next_line()

    def expect_re_line(self, pat: re.Pattern[str]) -> re.Match[str]:
        if mo := pat.fullmatch(self.peek()):
            self.next_line()
            return mo
        elif self.peek() is EOF:
            raise NecOutputParsingError(f'Expected regexp "{pat.pattern}" at EOF')
        else:
            raise NecOutputParsingError(
                f'Expected regexp "{pat.pattern}", found "{self.peek()}"'
            )

    def skip_until_re_line(self, pat: re.Pattern[str]) -> re.Match[str]:
        while self.peek() is not EOF:
            mo = pat.fullmatch(self.peek())
            self.next_line()
            if mo:
                return mo
        raise NecOutputParsingError(
            f'Expected regexp "{pat.pattern}" not found before EOF'
        )

    def next_line(self) -> None:
        """After processing the line returned by peek(), proceed to the next line."""
        try:
            self._line = next(self._lines).rstrip("\r\n")
        except StopIteration:
            self._line = EOF

    def expect_numbers(
        self, code: str
    ) -> list[Union[int, float, complex, SegmentCenter]]:
        """Expect a line of numeric data.

        The code consists of type letters:

        - I for int
        - F for float
        - C for complex (consuming two floats)
        - P for a position (consuming three floats)

        If there are more or less fields in the line than expected, given the type codes,
        this will raise an exception.
        """
        try:
            fields = self.peek().split()
            result: list[Union[int, float, complex, SegmentCenter]] = []
            for type_letter in code:
                try:
                    if type_letter == "C":
                        real = float(fields.pop(0))
                        imag = float(fields.pop(0))
                        result.append(complex(real=real, imag=imag))
                    elif type_letter == "I":
                        result.append(int(fields.pop(0)))
                    elif type_letter == "F":
                        result.append(float(fields.pop(0)))
                    elif type_letter == "P":
                        x = float(fields.pop(0))
                        y = float(fields.pop(0))
                        z = float(fields.pop(0))
                        result.append(SegmentCenter(x=x, y=y, z=z))
                    else:
                        raise NecOutputParsingError(
                            f'Unexpected code letter "{type_letter}"'
                        )
                except IndexError:
                    raise NecOutputParsingError(
                        "Not enough numeric fields in input line."
                    )
                except ValueError as ver:
                    raise NecOutputParsingError("Could not parse number", ver)
            if 0 == len(fields):
                self.next_line()
                return result
            else:
                unconsumed = (f'"{f}"' for f in fields)
                raise NecOutputParsingError(
                    f'Unconsumed fields in line "{self.peek()}": [{", ".join(unconsumed)}]'
                )
        except NecOutputParsingError as ex:
            ex.add_note(f'Failure to parse "{self.peek()}"')
            raise


_RE_ANTENNA_INPUT_PARAMETERS_HEADLINE = re.compile(
    r"\s+\-+ ANTENNA INPUT PARAMETERS \-+\s*"
)


def parse_antenna_input_parameters(ip: _InputPeek) -> AntennaInputParameters:
    ip.skip_until_re_line(_RE_ANTENNA_INPUT_PARAMETERS_HEADLINE)
    ip.expect_line(
        "  TAG   SEG       VOLTAGE (VOLTS)         CURRENT (AMPS)"
        "         IMPEDANCE (OHMS)        ADMITTANCE (MHOS)     POWER"
    )
    ip.expect_line(
        "  NO.   NO.     REAL      IMAGINARY     REAL      IMAGINARY     REAL"
        "      IMAGINARY    REAL       IMAGINARY   (WATTS)"
    )
    tag, seg, voltage, current, impedance, admittance, power = ip.expect_numbers(
        "IICCCCF"
    )
    return AntennaInputParameters(
        tag=cast(int, tag),
        seg=cast(int, seg),
        voltage=cast(complex, voltage),
        current=cast(complex, current),
        impedance=cast(complex, impedance),
        admittance=cast(complex, admittance),
        power=cast(float, power),
    )


def parse_currents_and_location(ip: _InputPeek) -> list[SegmentCurrent]:
    ip.skip_empty_lines()
    ip.expect_line("                        ----- CURRENTS AND LOCATION -----")
    ip.expect_line(
        "                            DISTANCES IN WAVELENGTHS "
    )  # There's a spurious " " here.
    ip.skip_empty_lines()
    ip.expect_line(
        "   SEG  TAG    COORDINATES OF SEGM CENTER     SEGM    ------------- CURRENT (AMPS) -------------"
    )
    ip.expect_line(
        "   No:  No:       X         Y         Z      LENGTH     REAL      IMAGINARY    MAGN        PHASE"
    )
    result: list[SegmentCurrent] = []
    while not (ip.next_line_is_empty() or ip.peek() is EOF):
        seg, tag, seg_center, seg_length, current, current_magnitude, current_phase = (
            ip.expect_numbers("IIPFCFF")
        )
        result.append(
            SegmentCurrent(
                seg=cast(int, seg),
                tag=cast(int, tag),
                seg_center=cast(SegmentCenter, seg_center),
                seg_length=cast(float, seg_length),
                current=cast(complex, current),
                current_magnitude=cast(float, current_magnitude),
                current_phase=cast(float, current_phase),
            )
        )
    return result


_RE_FREQUENCY_HEADLINE = re.compile(r"\s+\-+ FREQUENCY \-+\s*")
_RE_FREQUENCY_LINE = re.compile(r"\s+FREQUENCY=\s+([\dE\+\.]+) MHZ")
_RE_WAVELENGTH_LINE = re.compile(r"\s+WAVELENGTH=\s+([\dE\+\.]+) METERS")


@dataclass
class FrequencyAndWavelength:
    """Frequency in Hz, wavelength in m."""

    frequency: float
    wavelength: float


def parse_frequency_and_wavelength(ip: _InputPeek) -> FrequencyAndWavelength:
    ip.skip_until_re_line(_RE_FREQUENCY_HEADLINE)
    frequency = float(ip.expect_re_line(_RE_FREQUENCY_LINE).group(1)) * 1e6
    wavelength = float(ip.expect_re_line(_RE_WAVELENGTH_LINE).group(1))
    return FrequencyAndWavelength(frequency=frequency, wavelength=wavelength)


@dataclass
class PowerBudget:
    """All powers in W, efficiency as a number between 0 and 1."""

    input_power: float
    radiated_power: float
    structure_loss: float
    network_loss: float
    efficiency: float


_RE_POWER_BUDGET_HEADLINE = re.compile(r"\s+\-+ POWER BUDGET \-+\s*")
_RE_INPUT_POWER = re.compile(r"\s+INPUT POWER\s*\=\s*([\+\-E\.\d]+) Watts\s*")
_RE_RADIATED_POWER = re.compile(r"\s+RADIATED POWER\s*\=\s*([\+\-E\.\d]+) Watts\s*")
_RE_STRUCTURE_LOSS = re.compile(r"\s+STRUCTURE LOSS\s*\=\s*([\+\-E\.\d]+) Watts\s*")
_RE_NETWORK_LOSS = re.compile(r"\s+NETWORK LOSS\s*\=\s*([\+\-E\.\d]+) Watts\s*")
_RE_EFFICIENCY = re.compile(r"\s+EFFICIENCY\s*\=\s*([\+\-E\.\d]+) Percent\s*")


def parse_power_budget(ip: _InputPeek) -> PowerBudget:
    ip.skip_until_re_line(_RE_POWER_BUDGET_HEADLINE)
    input_power = float(ip.expect_re_line(_RE_INPUT_POWER).group(1))
    radiated_power = float(ip.expect_re_line(_RE_RADIATED_POWER).group(1))
    structure_loss = float(ip.expect_re_line(_RE_STRUCTURE_LOSS).group(1))
    network_loss = float(ip.expect_re_line(_RE_NETWORK_LOSS).group(1))
    efficiency = float(ip.expect_re_line(_RE_EFFICIENCY).group(1)) * 1e-2
    return PowerBudget(
        input_power=input_power,
        radiated_power=radiated_power,
        structure_loss=structure_loss,
        network_loss=network_loss,
        efficiency=efficiency,
    )


@dataclass
@unique
class PolarizationSense(Enum):
    NONE = 0
    LINEAR = 1
    LEFT = 2
    RIGHT = 3


@dataclass
class RadiationPatternRay:
    theta: float  # ray's vertical angle in degrees from z-axis (straight up)
    phi: float  # ray's horizontal angle in degrees, measured between x-axis and projection of ray to xy-plane
    power_gain_v_db: float
    power_gain_h_db: float
    power_gain_total: float
    polarization_axial_ratio: float
    polarization_axial_tilt: float
    polarization_sense: PolarizationSense
    e_theta_magnitude: float
    e_theta_phase_degrees: float
    e_phi_magnitude: float
    e_phi_phase_degrees: float


@dataclass
class PowerGainForTheta:
    phy_and_total_gain: list[Tuple[float, float]]
    max_gain_phi: float
    max_gain: float


@dataclass
class RadiationPattern:
    rays: list[RadiationPatternRay]

    def power_gain_by_theta(self) -> dict[float, PowerGainForTheta]:
        """The dict returned has theta as key and a list of tuples phi, power_gain_total as values."""
        theta_to_phy_and_total_gain: dict[float, list[Tuple[float, float]]] = {}
        theta_to_max_gain_phi: dict[float, float] = {}
        theta_to_max_gain: dict[float, float] = {}
        for ray in self.rays:
            theta = ray.theta
            ls = theta_to_phy_and_total_gain.get(theta)
            if ls is None:
                theta_to_phy_and_total_gain[theta] = ls = []
            ls.append((ray.phi, ray.power_gain_total))
            gain = ray.power_gain_total
            if theta_to_max_gain.get(theta, gain - 1.0) < gain:
                theta_to_max_gain_phi[theta] = ray.phi
                theta_to_max_gain[theta] = gain

        result: dict[float, PowerGainForTheta] = {}
        for theta in sorted(theta_to_phy_and_total_gain.keys()):
            result[theta] = PowerGainForTheta(
                phy_and_total_gain=theta_to_phy_and_total_gain[theta],
                max_gain_phi=theta_to_max_gain_phi[theta],
                max_gain=theta_to_max_gain[theta],
            )
        return result


_RE_RADIATION_PATTERNS = re.compile(r"\s+\-+\s+RADIATION PATTERNS\s+\-+\s*")
_RE_RADIATION_RAY = re.compile(
    r"(?:\s*([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"\s*( {6}|LINEAR|RIGHT |LEFT  )"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"(?:\s+([\+\-]?\d+\.\d*(?:E[\+\-]\d+)?))"
    r"\s*"
)


def parse_radiation_pattern(ip: _InputPeek) -> RadiationPattern:
    ip.skip_until_re_line(_RE_RADIATION_PATTERNS)
    ip.expect_line(
        " ---- ANGLES -----     ----- POWER GAINS -----       "
        "---- POLARIZATION ----   ---- E(THETA) ----    ----- E(PHI) ------"
    )
    ip.expect_line(
        "  THETA      PHI       VERTC   HORIZ   TOTAL       AXIAL      TILT  SENSE   "
        "MAGNITUDE    PHASE    MAGNITUDE     PHASE"
    )
    ip.expect_line(
        " DEGREES   DEGREES        DB       DB       DB       RATIO   DEGREES"
        "            VOLTS/M   DEGREES     VOLTS/M   DEGREES"
    )
    rays: list[RadiationPatternRay] = []
    current_line = ip.peek()
    try:
        while mo := _RE_RADIATION_RAY.fullmatch(current_line):
            theta = float(mo.group(1))
            phi = float(mo.group(2))
            power_gain_v_db = float(mo.group(3))
            power_gain_h_db = float(mo.group(4))
            power_gain_total = float(mo.group(5))
            polarization_axial_ratio = float(mo.group(6))
            polarization_axial_tilt = float(mo.group(7))
            ps = mo.group(8)
            if ps == "LEFT  ":
                polarization_sense = PolarizationSense.LEFT
            elif ps == "RIGHT ":
                polarization_sense = PolarizationSense.RIGHT
            elif ps == "LINEAR":
                polarization_sense = PolarizationSense.LINEAR
            elif ps == "      ":
                polarization_sense = PolarizationSense.NONE
            else:
                raise RuntimeError(f'Polarization sense "{ps}" not implemented.')
            e_theta_magnitude = float(mo.group(9))
            e_theta_phase_degrees = float(mo.group(10))
            e_phi_magnitude = float(mo.group(11))
            e_phi_phase_degrees = float(mo.group(12))
            ray = RadiationPatternRay(
                theta=theta,
                phi=phi,
                power_gain_v_db=power_gain_v_db,
                power_gain_h_db=power_gain_h_db,
                power_gain_total=power_gain_total,
                polarization_axial_ratio=polarization_axial_ratio,
                polarization_axial_tilt=polarization_axial_tilt,
                polarization_sense=polarization_sense,
                e_theta_magnitude=e_theta_magnitude,
                e_theta_phase_degrees=e_theta_phase_degrees,
                e_phi_magnitude=e_phi_magnitude,
                e_phi_phase_degrees=e_phi_phase_degrees,
            )
            rays.append(ray)
            ip.next_line()
            current_line = ip.peek()
    except Exception:
        logger.error('Problem parsing line "%s", see exception.', ip.peek())
        raise
    if ip.next_line_is_empty():
        return RadiationPattern(rays=rays)
    else:
        raise RuntimeError(f'Unexpected line "{ip.peek()}"')


@dataclass
class TotalEfficiency:
    efficiency: float
    average_power_gain: float
    solid_angle_used_div_by_pi: float


_RE_POWER_GAIN = re.compile(
    r"\s+AVERAGE POWER GAIN:\s+([\d\+\-\.E]+) \- "
    r"SOLID ANGLE USED IN AVERAGING: \(\s*([\d\+\-\.E]+)\s*\)\*PI STERADIANS\s*"
)


def parse_total_efficiency(ip: _InputPeek) -> TotalEfficiency:
    mo = ip.skip_until_re_line(_RE_POWER_GAIN)
    average_power_gain = float(mo.group(1))
    solid_angle_used_div_by_pi = float(mo.group(2))
    efficiency = average_power_gain / solid_angle_used_div_by_pi
    return TotalEfficiency(
        efficiency=efficiency,
        average_power_gain=average_power_gain,
        solid_angle_used_div_by_pi=solid_angle_used_div_by_pi,
    )


@dataclass
class Nec2ppOutput:
    frequency_and_wavelength: FrequencyAndWavelength
    input_and_impedance: AntennaInputParameters
    currents: list[SegmentCurrent]
    power_budget: PowerBudget
    radiation_pattern: RadiationPattern
    total_efficiency: TotalEfficiency


def parse_nec2pp_output(output_text: Iterable[str]) -> Nec2ppOutput:
    ip = _InputPeek(output_text)

    frequency_and_wavelength = parse_frequency_and_wavelength(ip)
    input_and_impedance = parse_antenna_input_parameters(ip)
    currents = parse_currents_and_location(ip)
    power_budget = parse_power_budget(ip)
    radiation_pattern = parse_radiation_pattern(ip)
    total_efficiency = parse_total_efficiency(ip)

    return Nec2ppOutput(
        frequency_and_wavelength=frequency_and_wavelength,
        input_and_impedance=input_and_impedance,
        currents=currents,
        power_budget=power_budget,
        total_efficiency=total_efficiency,
        radiation_pattern=radiation_pattern,
    )
