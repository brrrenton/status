from pydbus import SystemBus
import ipaddress

NM_DEVICE_TYPE_ETHERNET = 1
NM_DEVICE_TYPE_WIFI = 2
NM_STATE_ACTIVATED = 100


def format_bps(value):
    if value >= 1000:
        return str(int(value / 1000)) + " Gbit/s"
    else:
        return str(value) + " Mbit/s"


def format_ssid(value_list):
    ssid = ""

    for value in value_list:
        ssid += chr(value)

    return ssid


def networks(spacer):
    system_bus = SystemBus()
    nm_proxy = system_bus.get('org.freedesktop.NetworkManager')
    devices = nm_proxy.Devices

    string = ""

    for device in devices:
        device_proxy = system_bus.get('org.freedesktop.NetworkManager', device)

        if device_proxy.State == NM_STATE_ACTIVATED:
            if len(string) != 0:
                string += spacer

            if device_proxy.DeviceType == NM_DEVICE_TYPE_ETHERNET:
                ip4_config_proxy = system_bus.get('org.freedesktop.NetworkManager', device_proxy.Ip4Config)
                string += device_proxy.Interface + ": " + ip4_config_proxy.AddressData[0][
                    "address"] + " (" + format_bps(device_proxy.Speed) + ")"

            elif device_proxy.DeviceType == NM_DEVICE_TYPE_WIFI:
                ip4_config_proxy = system_bus.get('org.freedesktop.NetworkManager', device_proxy.Ip4Config)
                active_access_point_proxy = system_bus.get('org.freedesktop.NetworkManager',
                                                           device_proxy.ActiveAccessPoint)

                string += device_proxy.Interface + ": " + ip4_config_proxy.AddressData[0][
                    "address"] + " (" + format_ssid(active_access_point_proxy.Ssid) + ")"

    return string
