import av
from .io import LibAVIO

def iter_av_packets(url, format, codec, rate, seek=None):
    buffer = LibAVIO()
    pos = 0
    stream = av.open(url, 'r')
    if seek:
        stream.seek(int(seek * av.time_base))
        pos += seek
    demuxer = stream.demux(audio=0)
    output_stream = av.open(buffer, 'w', format=format)    
    muxer = output_stream.add_stream(codec, rate=rate)
    while True:
        packet = next(demuxer, b'')

        # If stream is exhausted, close connection
        if not packet:
            stream.close()
            output_stream.close()
            return b''

        # If packet is corrupted, reconnect it
        if packet.is_corrupt:
            stream.close()
            stream = av.open(url, 'r')
            stream.seek(int(pos * av.time_base), any_frame=True)           
            continue

        # According PyAV if demuxer sending packet with attribute dts with value None
        # that means demuxer is sending dummy packet.
        # If dummy packet is decoded it will flush the buffers.
        if packet.dts is None:
            packet.decode()
            stream.close()
            output_stream.close()
            return b''

        # Decode the packet
        frames = packet.decode()

        for frame in frames:
            pos = frame.time
            # https://github.com/PyAV-Org/PyAV/issues/281
            frame.pts = None
            new_packets = muxer.encode(frame)
            output_stream.mux(new_packets)
            yield buffer.read()