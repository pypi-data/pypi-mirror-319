import re

import pytest
from pytest import approx

from antenna_simulation_driver import necpp_output_parser
from antenna_simulation_driver.necpp_output_parser import (
    Nec2ppOutput,
    NecOutputParsingError,
    _InputPeek,
    parse_nec2pp_output,
)


def test_from_fixture() -> None:
    with open("tests/fixture_data/dipole_split.out") as infile:
        # result under test:
        rut: Nec2ppOutput = parse_nec2pp_output(infile)

    assert approx(7e6) == rut.frequency_and_wavelength.frequency
    assert approx(42.828) == rut.frequency_and_wavelength.wavelength

    assert approx(1.4414e01 - 1.0622e03j) == rut.input_and_impedance.impedance
    assert approx(1.2774e-05 + 9.4130e-04j) == rut.input_and_impedance.admittance
    assert approx(6.3869e-06) == rut.input_and_impedance.power
    assert approx(1.0) == rut.input_and_impedance.voltage
    assert approx(1.2774e-05 + 9.4130e-04j) == rut.input_and_impedance.current
    assert 2 == rut.input_and_impedance.tag
    assert 6 == rut.input_and_impedance.seg

    assert approx(6.3869e-06) == rut.power_budget.input_power
    assert approx(6.1519e-06) == rut.power_budget.radiated_power
    assert approx(2.3502e-07) == rut.power_budget.structure_loss
    assert 0.0 == rut.power_budget.network_loss
    assert approx(0.9632) == rut.power_budget.efficiency

    r = rut.radiation_pattern.rays[170]
    #   -35.00     20.00      2.54    -4.01     3.41
    #   0.0198    -25.17 RIGHT   2.6215E-02     78.65  1.2331E-02    -98.40
    assert approx(-35.0) == r.theta
    assert approx(20.0) == r.phi
    assert approx(2.54) == r.power_gain_v_db
    assert approx(-4.01) == r.power_gain_h_db
    assert approx(3.41) == r.power_gain_total
    assert approx(0.0198) == r.polarization_axial_ratio
    assert approx(-25.17) == r.polarization_axial_tilt
    assert necpp_output_parser.PolarizationSense.RIGHT == r.polarization_sense
    assert approx(0.026215) == r.e_theta_magnitude
    assert approx(78.65) == r.e_theta_phase_degrees
    assert approx(1.2331e-02) == r.e_phi_magnitude
    assert approx(-98.40) == r.e_phi_phase_degrees

    t2pg = rut.radiation_pattern.power_gain_by_theta()
    at_theta_35 = t2pg[-35.0]
    assert approx(90.0) == at_theta_35.max_gain_phi
    assert approx(5.43) == at_theta_35.max_gain
    some_rad = at_theta_35.phy_and_total_gain[9]
    assert approx(45.0) == some_rad[0]
    assert approx(4.39) == some_rad[1]

    assert approx(0.72245) == rut.total_efficiency.efficiency
    assert approx(2.0) == rut.total_efficiency.solid_angle_used_div_by_pi
    assert approx(1.4449) == rut.total_efficiency.average_power_gain


def test_not_enough_data() -> None:
    ip = _InputPeek(["7 4\n", "29\n"])
    assert [7, 4] == ip.expect_numbers("II")
    with pytest.raises(
        NecOutputParsingError,
        match='Not enough numeric fields in input line.\nFailure to parse "29"',
    ):
        ip.expect_numbers("II")


def test_too_much_data() -> None:
    ip = _InputPeek(["7 4\n", "29 31 15\n"])
    assert [7, 4] == ip.expect_numbers("II")
    with pytest.raises(
        NecOutputParsingError,
        match=r'Unconsumed fields in line "29 31 15": \["15"\]',
    ):
        ip.expect_numbers("II")


def test_non_numeric_data() -> None:
    ip = _InputPeek(["7 4\n", "29 lorem 15\n"])
    assert [7, 4] == ip.expect_numbers("II")
    with pytest.raises(
        NecOutputParsingError,
        match="ValueError.+'lorem'",
    ):
        ip.expect_numbers("III")


def test_unexpected_line() -> None:
    ip = _InputPeek(["expected line\r\n", "unexpected line \r\n"])
    ip.expect_line("expected line")
    with pytest.raises(
        NecOutputParsingError,
        match='Found: "unexpected line ", expected: "this will not work."',
    ):
        ip.expect_line("this will not work.")


def test_code_is_checked() -> None:
    ip = _InputPeek(["1 2 3"])
    with pytest.raises(NecOutputParsingError):
        ip.expect_numbers("XYZ")


def test_EOF_instead_of_expected_line_re() -> None:
    ip = _InputPeek([])
    regexp = re.compile("Rumpelstielzchen")
    with pytest.raises(NecOutputParsingError, match=regexp.pattern):
        ip.expect_re_line(regexp)


def test_unexpected_line_found_looking_for_re() -> None:
    ip = _InputPeek(["this line does not fit"])
    regexp = re.compile("This is what we expect")
    with pytest.raises(NecOutputParsingError, match=regexp.pattern):
        ip.expect_re_line(regexp)


def test_EOF_after_unexpected_lines() -> None:
    regexp = re.compile("ipsum")
    ip = _InputPeek(["some", "lines\n", "with\n", "lorem\n"])
    with pytest.raises(NecOutputParsingError, match=regexp.pattern):
        ip.skip_until_re_line(regexp)
