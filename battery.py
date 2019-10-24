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


class Battery:
    battery_proxy = None

    def __init__(self, system_bus):
        up_proxy = system_bus.get('org.freedesktop.UPower')
        devices = up_proxy.EnumerateDevices()

        for device in devices:
            device_proxy = system_bus.get('org.freedesktop.UPower', device)
            if device_proxy.Type == UP_TYPE_BATTERY:
                self.battery_proxy = device_proxy

    def status(self, spacer):
        if self.battery_proxy is None:
            return ""

        return "".join(["bat: ",
                        format_state(self.battery_proxy.State),
                        str(round(self.battery_proxy.Percentage)),
                        "%",
                        spacer])
