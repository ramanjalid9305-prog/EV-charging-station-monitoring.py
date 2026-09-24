import random
import time
from datetime import datetime

# EV battery configuration
BATTERY_CAPACITY_KWH = 60.0
INITIAL_SOC = 20.0
TARGET_SOC = 80.0

# Electricity charging tariff
TARIFF_PER_KWH = 8.0

# Charging limits
MAX_VOLTAGE = 500.0
MAX_CURRENT = 100.0

soc = INITIAL_SOC
total_energy = 0.0


def read_charging_data():
    """
    Simulate EV charging station measurements.

    In a real system, replace this function with data
    received from charging-station hardware.
    """

    voltage = random.uniform(380, 450)
    current = random.uniform(20, 80)

    return voltage, current


def calculate_power(voltage, current):
    """Calculate charging power in kW."""

    power_watts = voltage * current
    return power_watts / 1000


def calculate_energy(power_kw, elapsed_seconds):
    """Calculate energy delivered in kWh."""

    return power_kw * elapsed_seconds / 3600


def update_soc(energy_kwh):
    """Update EV battery state of charge."""

    global soc

    soc_increase = (
        energy_kwh / BATTERY_CAPACITY_KWH
    ) * 100

    soc += soc_increase

    if soc > 100:
        soc = 100


def calculate_cost(energy_kwh):
    """Calculate charging cost."""

    return energy_kwh * TARIFF_PER_KWH


def check_station_status(voltage, current, soc):
    """Check charging station operating status."""

    if voltage > MAX_VOLTAGE:
        return "HIGH VOLTAGE"

    if current > MAX_CURRENT:
        return "OVER CURRENT"

    if soc >= TARGET_SOC:
        return "CHARGING COMPLETE"

    return "CHARGING"


def main():
    global total_energy

    previous_time = time.time()

    print("=" * 65)
    print("          EV CHARGING STATION MONITORING SYSTEM")
    print("=" * 65)

    try:

        while True:

            voltage, current = read_charging_data()

            power = calculate_power(
                voltage,
                current
            )

            current_time = time.time()

            elapsed_seconds = (
                current_time - previous_time
            )

            previous_time = current_time

            energy = calculate_energy(
                power,
                elapsed_seconds
            )

            total_energy += energy

            update_soc(energy)

            cost = calculate_cost(total_energy)

            status = check_station_status(
                voltage,
                current,
                soc
            )

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            print("\n--------------------------------------------")
            print(f"Time          : {timestamp}")
            print(f"Voltage       : {voltage:.2f} V")
            print(f"Current       : {current:.2f} A")
            print(f"Power         : {power:.2f} kW")
            print(f"Energy        : {total_energy:.4f} kWh")
            print(f"Battery SOC   : {soc:.2f}%")
            print(f"Charging Cost : ₹{cost:.2f}")
            print(f"Station Status: {status}")
            print("--------------------------------------------")

            if status == "CHARGING COMPLETE":
                print("\nEV charging completed.")
                break

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
