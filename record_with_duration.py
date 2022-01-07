import datetime
import ffmpeg
import subprocess
import psutil
import time

rtsp_format = "rtsp://admin:hk123456@{}:554/Streaming/Channels/101"
duration = datetime.timedelta(minutes=15)

if __name__ == "__main__":
    x = subprocess.Popen(
        "ffmpeg -i {} "
        " -c copy -map 0 -segment_time 00:01:00 -f "
        " segment -strftime 1 temp/TEST_%Y%m%d_%H%M%S.mp4".format(
            rtsp_format.format("192.168.104.72")
        ),
        stdout=None,
    ).pid
    print(x)

    while 1:
        time.sleep(1)

#     (
#         ffmpeg
#         .input(rtsp_format.format("192.168.104.72"))
#         .
#     )
# #       ffmpeg -i rtsp://admin:hk123456@192.168.104.72:554/Streaming/Channels/101 `
# #    -c copy -map 0 -segment_time 00:15:00 -f segment -strftime 1 "TEST_%Y%m%d_%H%M%S.mp4"
