import pulsectl


def volume(spacer):
    with pulsectl.Pulse('volume') as pulse:
        sink = pulse.sink_list()[0]
        if sink.mute:
            output_vol_string = '0%'
        else:
            vol = sink.volume
            output_vol_string = '{:.0f}%'.format(vol.value_flat * 100.)
        
        source = pulse.source_list()[1]
        
        if source.mute:
            input_vol_string = '0%'
        else:
            vol = source.volume
            input_vol_string = '{:.0f}%'.format(vol.value_flat * 100.)
        
        return ''.join(['vol: ', output_vol_string, '/', input_vol_string, spacer])

