from pydbus import SystemBus
system_bus = SystemBus()

NM_DEVICE_TYPE_ETHERNET = 1
NM_DEVICE_TYPE_WIFI = 2
NM_STATE_ACTIVATED = 100


def format_bps(value):
    if value >= 1000:
        return ''.join([str(int(value / 1000)) + ' Gbit/s'])
    else:
        return ''.join([str(value) + ' Mbit/s'])


def format_ssid(value_list):
    char_list = []
    for v in value_list:
        char_list.append(chr(v))

    return ''.join(char_list)


def format_ip4_addr(ip4_addr_decimal):
    return ''.join([str(ip4_addr_decimal & 0xFF), '.',
                    str((ip4_addr_decimal & (0xFF << 8)) >> 8), '.',
                    str((ip4_addr_decimal & (0xFF << 16)) >> 16), '.',
                    str((ip4_addr_decimal & (0xFF << 24)) >> 24)])


class Network:
    _ethernet_proxy = None
    _wifi_proxy = None

    _spacer = ''
    ethernet_status = ''
    wifi_status = ''

    def __init__(self, spacer):
        self._spacer = spacer

        nm_proxy = system_bus.get('org.freedesktop.NetworkManager')

        devices = nm_proxy.Devices

        for device in devices:
            device_proxy = system_bus.get('org.freedesktop.NetworkManager', device)

            if device_proxy.DeviceType == NM_DEVICE_TYPE_ETHERNET:
                self._ethernet_proxy = device_proxy
            elif device_proxy.DeviceType == NM_DEVICE_TYPE_WIFI:
                self._wifi_proxy = device_proxy

        if self._ethernet_proxy is not None:
            self._update_ethernet()
            self._ethernet_proxy.PropertiesChanged.connect(self._update_ethernet)

        if self._wifi_proxy is not None:
            self._update_wifi()
            self._wifi_proxy.PropertiesChanged.connect(self._update_wifi)

    def _update_ethernet(self, values='', sep='', end=''):
        if self._ethernet_proxy is None or self._ethernet_proxy.State != NM_STATE_ACTIVATED:
            self.ethernet_status = ''
            return

        self.ethernet_status = ''.join([self._ethernet_proxy.Interface,
                                        ': ',
                                        format_ip4_addr(self._ethernet_proxy.Ip4Address),
                                        ' (',
                                        format_bps(self._ethernet_proxy.Speed),
                                        ')',
                                        self._spacer])

    def _update_wifi(self, values='', sep='', end=''):
        if self._wifi_proxy is None or self._wifi_proxy.State != NM_STATE_ACTIVATED:
            self.wifi_status = ''
            return

        active_access_point_proxy = system_bus.get('org.freedesktop.NetworkManager',
                                                   self._wifi_proxy.ActiveAccessPoint)

        self.wifi_status = ''.join([self._wifi_proxy.Interface,
                                    ': ',
                                    format_ip4_addr(self._wifi_proxy.Ip4Address),
                                    ' (',
                                    format_ssid(active_access_point_proxy.Ssid),
                                    ')',
                                    self._spacer])
