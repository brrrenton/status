import pulsectl


def volume(spacer):
    with pulsectl.Pulse('volume') as pulse:

        output_vol_string = '-'

        if len(pulse.sink_list()) is not 0:
            sink = pulse.sink_list()[0]

            if sink.name != 'auto_null':
                if sink.mute:
                    output_vol_string = '0%'
                else:
                    vol = sink.volume
                    output_vol_string = '{:.0f}%'.format(vol.value_flat * 100.)

        input_vol_string = '-'

        if len(pulse.source_list()) is not 0:

            source = pulse.source_list()[0]

            if source.name != 'auto_null.monitor':
                if source.mute:
                    input_vol_string = '0%'
                else:
                    vol = source.volume
                    input_vol_string = '{:.0f}%'.format(vol.value_flat * 100.)

        return ''.join(['vol: ', output_vol_string, '/', input_vol_string, spacer])
