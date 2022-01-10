import av
import datetime
import cv2

end_time = datetime.datetime.now() + datetime.timedelta(seconds=60)

input_container = av.open(
    "rtsp://admin:hk123456@192.168.104.72:554/Streaming/Channels/101"
)
input_stream = input_container.streams[0]

output_container = av.open("test.mp4", "w")
output_stream = output_container.add_stream("mp4")

class ForLoopBreak(Exception):
    pass

try:
    for frame in input_container.decode(input_stream):
        for packet in output_stream.encode(frame):
            output_container.mux(packet)
            if datetime.datetime.now() >= end_time:
                raise ForLoopBreak()
except ForLoopBreak:
    pass

for packet in output_stream.encode(None):
    output_container.mux(packet)

output_container.close()
