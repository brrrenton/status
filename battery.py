from pydbus import SystemBus

UP_TYPE_BATTERY = 2
UP_STATE_CHARGING = 1
UP_STATE_DISCHARGING = 2
UP_STATE_FULLY_CHARGED = 4


def format_state(value):
    if value == UP_STATE_CHARGING:
        return "+"
    elif value == UP_STATE_DISCHARGING:
        return "-"
    elif value == UP_STATE_FULLY_CHARGED:
        return "~"
    else:
        return "?"


def battery_status():
    system_bus = SystemBus()
    up_proxy = system_bus.get('org.freedesktop.UPower')
    devices = up_proxy.EnumerateDevices()

    for device in devices:
        device_proxy = system_bus.get('org.freedesktop.UPower', device)
        if device_proxy.Type == UP_TYPE_BATTERY:
            return format_state(device_proxy.State) + str(round(device_proxy.Percentage)) + "%"
