import sys, json, datetime

d = json.load(sys.stdin)
r = d.get('rate_limits', {})
W = 8

def bar(p):
    f = round(p / 100 * W)
    return '█' * f + '░' * (W - f)

def secs_remaining(block):
    ts = block.get('resets_at') or block.get('reset_at') or block.get('reset_time')
    if not ts:
        return -1
    try:
        s = float(ts) - datetime.datetime.now(datetime.timezone.utc).timestamp()
        return max(0, int(s))
    except Exception:
        return -1

def time_until(block):
    s = secs_remaining(block)
    if s < 0:
        return ''
    if s == 0:
        return ' ↺ now'
    h, rem = divmod(s, 3600)
    m = rem // 60
    if h >= 24:
        dd, hh = divmod(h, 24)
        return f' ↺ {dd}d{hh:02d}h'
    return f' ↺ {h}h{m:02d}m' if h else f' ↺ {m}m'

def send_to_arduino(five_pct, seven_pct, five_secs, seven_secs):
    try:
        import serial
        import serial.tools.list_ports
        keywords = ['arduino', 'ch340', 'ch341', 'cp210', 'ftdi', 'usb serial']
        port = None
        for p in serial.tools.list_ports.comports():
            desc = (p.description + ' ' + (p.manufacturer or '')).lower()
            if any(k in desc for k in keywords):
                port = p.device
                break
        if port:
            s = serial.Serial()
            s.port = port
            s.baudrate = 9600
            s.timeout = 1
            s.dtr = False
            s.open()
            s.write(f'{int(five_pct)},{int(seven_pct)},{five_secs},{seven_secs}\n'.encode())
            s.close()
    except Exception:
        pass

five_block = r.get('five_hour', {})
seven_block = r.get('seven_day', {})
five_pct  = five_block.get('used_percentage')
seven_pct = seven_block.get('used_percentage')

parts = []
for label, block in [('5h', five_block), ('7d', seven_block)]:
    p = block.get('used_percentage')
    if p is not None:
        parts.append(f'{label}[{bar(p)}]{int(p)}%{time_until(block)}')

if parts:
    print('  '.join(parts))

if five_pct is not None and seven_pct is not None:
    send_to_arduino(five_pct, seven_pct,
                    secs_remaining(five_block), secs_remaining(seven_block))
