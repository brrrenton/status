import pulsectl


def volume(spacer):
    with pulsectl.Pulse('volume') as pulse:

        output_vol_string = '-'

        for sink in pulse.sink_list():
            if sink.name != 'auto_null' and sink.monitor_source == 0:
                if sink.mute:
                    output_vol_string = '0%'
                else:
                    vol = sink.volume
                    output_vol_string = '{:.0f}%'.format(vol.value_flat * 100.)
                break;

        input_vol_string = '-'

        for source in pulse.source_list():
            if source.name != 'auto_null.monitor' and source.monitor_of_sink != 0:
                if source.mute:
                    input_vol_string = '0%'
                else:
                    vol = source.volume
                    input_vol_string = '{:.0f}%'.format(vol.value_flat * 100.)
                break;

        return ''.join(['vol: ', output_vol_string, '/', input_vol_string, spacer])

