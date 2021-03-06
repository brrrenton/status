from pydbus import SystemBus

system_bus = SystemBus()

NM_DEVICE_TYPE_ETHERNET = 1
NM_DEVICE_TYPE_WIFI = 2


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
    _nm_proxy = None
    _device_proxies = []

    _spacer = ''
    status = ''

    def __init__(self, spacer):
        self._spacer = spacer

        self._nm_proxy = system_bus.get('org.freedesktop.NetworkManager')

        if self._nm_proxy is not None:
            self._update1()
            self._nm_proxy.PropertiesChanged.connect(self._update1)

    def _update1(self, values='', sep='', end=''):
        self._device_proxies = []

        active_connections = self._nm_proxy.ActiveConnections

        for active_connection in active_connections:
            try:
                active_connection_proxy = system_bus.get('org.freedesktop.NetworkManager', active_connection)
            except:
                continue

            devices = active_connection_proxy.Devices

            for device in devices:
                device_proxy = system_bus.get('org.freedesktop.NetworkManager', device)
                device_proxy.PropertiesChanged.connect(self._update2)
                self._device_proxies.append(device_proxy)

        self._update2()

    def _update2(self, values='', sep='', end=''):
        self.status = ''

        for device_proxy in self._device_proxies:
            if device_proxy.DeviceType == NM_DEVICE_TYPE_ETHERNET:
                try:
                    ip4_config_proxy = system_bus.get('org.freedesktop.NetworkManager', device_proxy.Ip4Config)
                except:
                    continue

                if device_proxy.Speed == 0:
                    self.status += ''.join([device_proxy.Interface,
                                            ': ',
                                            ip4_config_proxy.AddressData[0]["address"],
                                            self._spacer])
                else:
                    self.status += ''.join([device_proxy.Interface,
                                            ': ',
                                            ip4_config_proxy.AddressData[0]["address"],
                                            ' (',
                                            format_bps(device_proxy.Speed),
                                            ')',
                                            self._spacer])
            elif device_proxy.DeviceType == NM_DEVICE_TYPE_WIFI:
                try:
                    active_access_point_proxy = system_bus.get('org.freedesktop.NetworkManager',
                                                               device_proxy.ActiveAccessPoint)
                except:
                    continue

                self.status += ''.join([device_proxy.Interface,
                                        ': ',
                                        format_ip4_addr(device_proxy.Ip4Address),
                                        ' (',
                                        format_ssid(active_access_point_proxy.Ssid),
                                        ')',
                                        self._spacer])

        self.parent_update_function()

    def parent_update_function(self):
        pass
