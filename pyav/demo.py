import av

container = av.open("output.mkv")

for frame in container.decode(video=0):
    frame.to_image().save('frames/frame-%04d.jpg' % frame.index)
