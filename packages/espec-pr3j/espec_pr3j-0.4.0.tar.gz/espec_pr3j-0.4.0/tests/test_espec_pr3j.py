import pytest

from espec_pr3j import EspecPr3j, OperationMode

TARGET_TEMPERATURE = 23.0
LOWER_TEMPERATURE = 20.0
UPPER_TEMPERATURE = 30.0

TARGET_HUMIDITY = 50.0
LOWER_HUMIDITY = 40.0
UPPER_HUMIDITY = 99.0


@pytest.fixture
def STABILITY_POLL_INTERVAL(hil):
    if hil:
        return 30

    return 0.001


@pytest.fixture
def STABILITY_TIME(hil):
    if hil:
        return 60 * 5

    return 0.01


def test_temperature_limits(environmental_chamber: EspecPr3j):
    environmental_chamber.set_temperature_limits(
        upper_limit=UPPER_TEMPERATURE, lower_limit=LOWER_TEMPERATURE
    )

    temperature = environmental_chamber.get_temperature_status()

    assert temperature.lower_limit == LOWER_TEMPERATURE
    assert temperature.upper_limit == UPPER_TEMPERATURE


def test_humidity_limits(environmental_chamber: EspecPr3j):
    environmental_chamber.set_humidity_limits(
        upper_limit=UPPER_HUMIDITY, lower_limit=LOWER_HUMIDITY
    )

    humidity = environmental_chamber.get_humidity_status()

    assert humidity.lower_limit == LOWER_HUMIDITY
    assert humidity.upper_limit == UPPER_HUMIDITY


@pytest.mark.skipif(
    "config.getvalue('hil')", reason="Not valid for hardware-in-the-loop"
)
def test_modes(environmental_chamber: EspecPr3j):
    environmental_chamber.set_mode(OperationMode.CONSTANT)
    assert environmental_chamber.get_mode() == OperationMode.CONSTANT

    environmental_chamber.set_mode(OperationMode.RUN)
    assert environmental_chamber.get_mode() == OperationMode.RUN

    environmental_chamber.set_mode(OperationMode.OFF)
    assert environmental_chamber.get_mode() == OperationMode.OFF

    environmental_chamber.set_mode(OperationMode.STANDBY)
    assert environmental_chamber.get_mode() == OperationMode.STANDBY


def test_constant_condition(
    environmental_chamber: EspecPr3j, STABILITY_TIME, STABILITY_POLL_INTERVAL
):
    environmental_chamber.set_constant_condition(
        temperature=TARGET_TEMPERATURE,
        humidity=TARGET_HUMIDITY,
        stable_time=STABILITY_TIME,
        poll_interval=STABILITY_POLL_INTERVAL,
    )

    temperature = environmental_chamber.get_temperature_status()
    humidity = environmental_chamber.get_humidity_status()

    assert (
        abs(temperature.current_temperature - TARGET_TEMPERATURE)
        < environmental_chamber.temperature_accuracy
    )
    assert (
        abs(humidity.current_humidity - TARGET_HUMIDITY)
        < environmental_chamber.humidity_accuracy
    )


def test_no_humidity_control(environmental_chamber: EspecPr3j):
    environmental_chamber.set_target_humidity(None)

    humidity = environmental_chamber.get_humidity_status()
    assert humidity.target_humidity is None

    environmental_chamber.set_target_humidity(TARGET_HUMIDITY)
    humidity = environmental_chamber.get_humidity_status()
    assert humidity.target_humidity == TARGET_HUMIDITY


def test_no_humidity_control_in_constant_condition(
    environmental_chamber: EspecPr3j, STABILITY_TIME, STABILITY_POLL_INTERVAL
):
    environmental_chamber.set_constant_condition(
        temperature=TARGET_TEMPERATURE,
        humidity=None,
        stable_time=STABILITY_TIME,
        poll_interval=STABILITY_POLL_INTERVAL,
    )

    temperature = environmental_chamber.get_temperature_status()
    humidity = environmental_chamber.get_humidity_status()

    assert (
        abs(temperature.current_temperature - TARGET_TEMPERATURE)
        < environmental_chamber.temperature_accuracy
    )
    assert humidity.target_humidity is None


def test_test_area_state(environmental_chamber: EspecPr3j):
    test_area = environmental_chamber.get_test_area_state()

    assert (
        abs(test_area.current_temperature - TARGET_TEMPERATURE)
        < environmental_chamber.temperature_accuracy
    )

    assert (
        abs(test_area.current_humidity - TARGET_HUMIDITY)
        < environmental_chamber.humidity_accuracy
    )

    assert test_area.operation_state == OperationMode.CONSTANT


def test_heaters(environmental_chamber: EspecPr3j):
    heaters_status = environmental_chamber.get_heater_percentage()

    assert heaters_status is not None
    assert 0.0 <= heaters_status.humidity_heater <= 100.0
    assert 0.0 <= heaters_status.temperature_heater <= 100.0
