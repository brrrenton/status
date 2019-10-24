NM_DEVICE_TYPE_ETHERNET = 1
NM_DEVICE_TYPE_WIFI = 2
NM_STATE_ACTIVATED = 100


def format_bps(value):
    if value >= 1000:
        return "".join([str(int(value / 1000)) + " Gbit/s"])
    else:
        return "".join([str(value) + " Mbit/s"])


def format_ssid(value_list):
    char_list = []
    for v in value_list:
        char_list.append(chr(v))

    return "".join(char_list)


class Network:
    system_bus = None
    ethernet_proxy = None
    wifi_proxy = None

    def __init__(self, system_bus):
        self.system_bus = system_bus
        nm_proxy = self.system_bus.get('org.freedesktop.NetworkManager')

        devices = nm_proxy.Devices

        for device in devices:
            device_proxy = self.system_bus.get('org.freedesktop.NetworkManager', device)

            if device_proxy.DeviceType == NM_DEVICE_TYPE_ETHERNET:
                self.ethernet_proxy = device_proxy
            elif device_proxy.DeviceType == NM_DEVICE_TYPE_WIFI:
                self.wifi_proxy = device_proxy

    def ethernet(self, spacer):
        if self.ethernet_proxy is None or self.ethernet_proxy.State != NM_STATE_ACTIVATED:
            return ""

        ip4_config_proxy = self.system_bus.get('org.freedesktop.NetworkManager', self.ethernet_proxy.Ip4Config)

        return "".join([self.ethernet_proxy.Interface,
                        ": ",
                        ip4_config_proxy.AddressData[0]["address"],
                        " (",
                        format_bps(self.ethernet_proxy.Speed),
                        ")",
                        spacer])

    def wifi(self, spacer):
        if self.wifi_proxy is None or self.wifi_proxy.State != NM_STATE_ACTIVATED:
            return ""

        ip4_config_proxy = self.system_bus.get('org.freedesktop.NetworkManager', self.wifi_proxy.Ip4Config)
        active_access_point_proxy = self.system_bus.get('org.freedesktop.NetworkManager',
                                                        self.wifi_proxy.ActiveAccessPoint)

        return "".join([self.wifi_proxy.Interface,
                        ": ",
                        ip4_config_proxy.AddressData[0]["address"],
                        " (",
                        format_ssid(active_access_point_proxy.Ssid),
                        ")",
                        spacer])
