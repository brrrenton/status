from pydbus import SystemBus

system_bus = SystemBus()

UPOWER_TYPE_BATTERY = 2
UPOWER_STATE_CHARGING = 1
UPOWER_STATE_DISCHARGING = 2
UPOWER_STATE_FULLY_CHARGED = 4


def format_state(value):
    if value == UPOWER_STATE_CHARGING:
        return '+'
    elif value == UPOWER_STATE_DISCHARGING:
        return '-'
    elif value == UPOWER_STATE_FULLY_CHARGED:
        return ''
    else:
        return '?'


def format_time(total_seconds):
    total_minutes = total_seconds // 60

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return ' ({}:{:0>2})'.format(hours, minutes)


class Battery:
    _device_proxy = None
    _spacer = ''
    status = ''

    def __init__(self, spacer):
        self._spacer = spacer

        upower_proxy = system_bus.get('org.freedesktop.UPower')
        devices = upower_proxy.EnumerateDevices()

        for device in devices:
            device_proxy = system_bus.get('org.freedesktop.UPower', device)
            if device_proxy.Type == UPOWER_TYPE_BATTERY:
                self._device_proxy = device_proxy
                break

        if self._device_proxy is not None:
            self._update()
            self._device_proxy.PropertiesChanged.connect(self._update)

    def _update(self, values='', sep='', end=''):

        state = self._device_proxy.State

        time = ' '

        if state == UPOWER_STATE_CHARGING:
            time = format_time(self._device_proxy.TimeToFull)
        elif state == UPOWER_STATE_DISCHARGING:
            time = format_time(self._device_proxy.TimeToEmpty)

        self.status = ''.join(['bat: ',
                               format_state(state),
                               str(round(self._device_proxy.Percentage)),
                               '%',
                               time,
                               self._spacer])
