# modified from: https://zhuanlan.zhihu.com/p/368471270

import av
import os
import datetime


def live_record(url, path, duration=5):
    """
    音视频录制
    url：直播地址
    path：视频保存路径
    duration：每个视频时长，默认5分钟保存一个视频
    """
    options = {
        "rtsp_transport": "tcp",
        "buffer_size": "1024000",
    }
    timeout = (10, 24)

    old = datetime.datetime.now()

    if not os.path.exists(path):
        os.makedirs(path)
    has_audio = False
    with av.open(url, options=options, timeout=timeout) as r:
        r.streams.video[0].thread_type = "AUTO"
        c_con = r.streams.video[0].codec_context
        rate = c_con.framerate.numerator if c_con.framerate else 25
        frame_count = duration * rate * 60 * 1

        if len(r.streams.audio) > 0:
            has_audio = True

        while True:
            write_path = os.path.join(
                path, datetime.now().strftime("%Y-%m-%dT%H%M%S") + ".mp4"
            )
            with av.open(write_path, "w", format="mp4") as w:
                r_v = r.streams.video[0]
                o_v = w.add_stream(template=r_v)

                r_a = None
                o_a = None
                if has_audio:
                    r_a = r.streams.audio[0]
                    o_a = w.add_stream("mp3")

                frame_idx = 0

                try:
                    for packet in r.demux(r_v, r_a):
                        if datetime.datetime.now().day != old.day:
                            break

                        if packet.is_corrupt or frame_idx == 0:
                            packet.dts = 0
                            packet.pts = 0
                            first_packet = False

                        if frame_idx >= frame_count:
                            break
                        if packet.stream.type == "video":
                            packet.stream = o_v
                            w.streams.video[0].container.mux(packet)
                            frame_idx += 1
                        elif packet.stream.type == "audio":
                            packet.stream = o_a
                            w.streams.audio[0].container.mux(packet)
                    old = datetime.datetime.now()
                except av.error.ExitError as e:
                    print("stream disconnect!")


if __name__ == "__main__":
    url = "rtsp://admin:hk123456@192.168.104.80:554/Streaming/Channels/101"
    live_record(url, "record", duration=1)
