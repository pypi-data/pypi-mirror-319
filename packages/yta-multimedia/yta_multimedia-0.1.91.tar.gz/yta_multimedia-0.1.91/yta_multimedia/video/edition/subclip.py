from yta_multimedia.video.parser import VideoParser
from moviepy.Clip import Clip
from typing import Union


def subclip_video(video: Clip, start_time: float, end_time: float) -> tuple[Union[Clip, None], Clip, Union[Clip, None]]:
    """
    Subclip the provided 'video' into 3 different subclips,
    according to the provided 'start_time' and 'end_time',
    and return them as a tuple of those 3 clips. First and
    third clip could be None.

    The first clip will be None when 'start_time' is 0, and 
    the third one when the 'end_time' is equal to the given
    'video' duration.
    """
    video = VideoParser.to_moviepy(video)

    left = None if (start_time == 0) else video.with_subclip(0, start_time)
    center = video.with_subclip(start_time, end_time)
    right = None if (end_time is None) else video.with_subclip(start_time = end_time)

    return left, center, right