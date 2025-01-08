from yta_multimedia.video.parser import VideoParser
from yta_multimedia.image.edition.image_editor import ImageEditor
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_general_utils.programming.parameter_validator import NumberValidator
from moviepy.Clip import Clip
from moviepy import CompositeVideoClip
from typing import Union



END_OF_CLIP = 999999

class SubClip:
    """
    Class to represent a subclip of a clip in which we
    can apply different modifications such as color
    temperature, zoom, movement, etc.

    This class represent the same as one of the subclips
    in any of your video editor apps.
    """
    video: Clip = None
    layer: int = None
    # TODO: Add all needed attributes
    # Volume
    _volume: int = None
    # Color attributes
    _color_temperature: int = None
    # Zoom and movement
    _zoom: int = None
    x_movement: int = None
    y_movement: int = None
    rotation: int = None

    def __init__(self, video: Clip, layer: int = 1, start_time: Union[float, None] = 0, end_time: Union[float, None] = END_OF_CLIP):
        """
        This method returns a tuple containing the left clip,
        the center clip (which is the one stored in this 
        instance) and the left clip product of subclipping the
        main clip.
        """
        # TODO: This configuration must be in a general settings
        # file
        if not NumberValidator.is_number_between(layer, 1, 10):
            raise Exception('The provided "layer" is not a valid layer, it must be an int value between [1, 10].')
        
        video = VideoParser.to_moviepy(video)

        left_clip, center_clip, right_clip = subclip_video(video, start_time, end_time)

        self.video = center_clip
        self.layer = layer
        self.volume = 100

        # TODO: Should I return the left and right clip to be updated in
        # the other file who instantiates this class (?)

        # TODO: Maybe we should handle any moviepy 'video' as a SubClip
        # in our application so we handle all attributes and, if we
        # subclip a SubClip instance, we .copy() the previous attributes
        # to the left, center and right clips we obtain when subclipping.
        # This would preserve previous configurations and let us manage
        # all the clips, so we work on top of moviepy library in any
        # change we process and use moviepy only for basic and frame
        # transformations.
        return left_clip, center_clip, right_clip
    
    @property
    def zoom(self):
        return self._zoom
    
    @zoom.setter
    def zoom(self, value):
        # TODO: This limit must be a config file
        ZOOM_LIMIT = (1, 500)
        
        if not NumberValidator.is_number_between(value, ZOOM_LIMIT[0], ZOOM_LIMIT[1]):
            raise Exception(f'The "value" parameter provided is not a number between [{ZOOM_LIMIT[0]}, {ZOOM_LIMIT[1]}].')
        
        self._zoom = int(value)

    @property
    def color_temperature(self):
        return self._color_temperature
    
    @color_temperature.setter
    def color_temperature(self, value):
        from yta_multimedia.image.edition.image_editor import COLOR_TEMPERATURE_CHANGE_LOWER_LIMIT, COLOR_TEMPERATURE_CHANGE_UPPER_LIMIT

        if not NumberValidator.is_number_between(value, COLOR_TEMPERATURE_CHANGE_LOWER_LIMIT, COLOR_TEMPERATURE_CHANGE_UPPER_LIMIT):
            raise Exception(f'The "value" parameter provided is not a number between [{COLOR_TEMPERATURE_CHANGE_LOWER_LIMIT}, {COLOR_TEMPERATURE_CHANGE_UPPER_LIMIT}].')

        self._color_temperature = value

    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, value):
        VOLUME_LIMIT = (0, 300)

        if not NumberValidator.is_number_between(value, VOLUME_LIMIT[0], VOLUME_LIMIT[1]):
            raise Exception(f'The "value" parameter provided is not a number between [{VOLUME_LIMIT[0]}, {VOLUME_LIMIT[1]}].')
        
        self._volume = int(value)
    
    def process(self):
        """
        Process the video clip with the attributes set and 
        obtain a copy of the original video clip with those
        attributes and effects applied on it. This method
        uses a black (but transparent) background with the
        same video size to make sure everything works 
        properly.

        This method doesn't change the original clip, it
        applies the changes on a copy of the original one
        and returns that copy modified.
        """
        video = self.video.copy()
        black_background_video = ClipGenerator.get_default_background_video(duration = video.duration)

        # TODO: Maybe I can separate a function that can be
        # processed in a whole clip as a value for each frame
        # (as I do in other classes) and apply that modification
        # to each frame, but I'm not sure. I do this in
        # MoviepyWithPrecalculated class, and it looks like this:
        """
        if resized_list is not None:
            video = video.resized(lambda t: resized_list[video_handler.frame_time_to_frame_index(t, video_handler.fps)])
        """

        # Functions that need to be processed frame by frame
        def modify_video_frame_by_frame(get_frame, t):
            frame = get_frame(t)

            if self.color_temperature is not None:
                frame = ImageEditor.modify_color_temperature(frame, self.color_temperature)

        # Apply frame by frame video modifications
        video = video.transform(lambda get_frame, t: modify_video_frame_by_frame(get_frame, t))

        # Functions that can be processed in the whole clip
        size = video.size
        if self.zoom is not None:
            size = (self.zoom / 100 * size[0], self.zoom / 100 * size[1])
        
            video = video.resized(size)

        position = ('center', 'center')
        # TODO: Apply position changer, please check MoviepyWithPrecalculated

        rotation = 0
        # TODO: Apply rotation changer, please check MoviepyWithPrecalculated

        # Functions that changes the audio
        if self.volume != 100:
            video = video.with_volume_scaled(self.volume / 100)

        # TODO: This below is repeated in VideoEditor class as
        # '._overlay_video()'
        return CompositeVideoClip([
            black_background_video,
            video.with_position(position)
        ])#.with_audio(VideoAudioCombinator(audio_mode).process_audio(background_video, video))

    



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

    left = None if (start_time == 0 or start_time == None) else video.with_subclip(0, start_time)
    center = video.with_subclip(start_time, end_time)
    right = None if (end_time is None or end_time < END_OF_CLIP) else video.with_subclip(start_time = end_time)

    return left, center, right