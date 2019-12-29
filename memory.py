def format_byte(value):
    if value < 1024:
        return ''.join([str(round(value, 1)) + ' KiB'])
    elif value < (1024 * 1024):
        return ''.join([str(round((value / 1024), 1)) + ' MiB'])
    else:
        return ''.join([str(round((value / (1024 * 1024)), 1)) + ' GiB'])


def memory_free(spacer):
    meminfo = open('/proc/meminfo', 'r')

    mem_total_string = meminfo.readline()
    mem_free_string = meminfo.readline()
    meminfo.readline()
    # mem_available_string = meminfo.readline()
    buffers_string = meminfo.readline()
    cached_string = meminfo.readline()

    meminfo.close()

    mem_total = int(mem_total_string.split()[1])
    mem_free = int(mem_free_string.split()[1])
    # mem_available = int(mem_available_string.split()[1])
    buffers = int(buffers_string.split()[1])
    cached = int(cached_string.split()[1])

    mem_used = mem_total - mem_free - buffers - cached

    return ''.join(['mem: ', format_byte(mem_used), spacer])
