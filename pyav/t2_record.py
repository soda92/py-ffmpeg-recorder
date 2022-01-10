# from: https://github.com/PyAV-Org/PyAV/issues/358
import av
import time

in_container = av.open("rtsp://admin:hk123456@192.168.104.80:554/Streaming/Channels/101", "r")
video_stream = in_container.streams.video[0]

out_container = None

def start_container(stream, timestamp):
    global out_container
    filename = "./record/file_" + str(timestamp) + ".mp4"
    out_container = av.open(filename, "w", format="mp4")
    outstream = out_container.add_stream(template=stream)
    outstream.options = {}

def stop_container():
    global out_container
    out_container.close()
    out_container = None

first_packet = True
rescaling_nr = 0
clip_duration = 60 * 1000 #60 seconds
first_frame_timestamp = int(time.time() * 1000)

for packet in in_container.demux(video_stream):
    if first_packet:
        packet.dts = 0
        packet.pts = 0
        first_packet = False

    cur_timestamp = int(time.time() * 1000)
    if packet.is_keyframe and (cur_timestamp - first_frame_timestamp) >= clip_duration:
        stop_container()

    if out_container is None:
        start_container(video_stream, cur_timestamp)
        rescaling_nr = packet.dts
        first_frame_timestamp = cur_timestamp

    packet.pts -= rescaling_nr
    packet.dts -= rescaling_nr

    out_container.mux_one(packet)
