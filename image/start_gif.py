import sys
import os
from PIL import Image, ImageTk, ImageSequence

class Configs:
    def __init__(self, loading):
        self.loading = loading
        self._animation_id = None

        self.get_gif_path()
        self.open_gif()
        self.animate_gif()

    def get_gif_path(self):
        self.loading_file = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        self.loading_path = os.path.join(os.path.abspath(self.loading_file), 'AnimationLoading.gif')

    def open_gif(self):
        self.gif = Image.open(self.loading_path)
        self.frames = [frame.copy().resize((70, 70)) for frame in ImageSequence.Iterator(self.gif)]
        self.delay = self.gif.info.get("duration", 100)

    def animate_gif(self, index=0):
        self.frame = self.frames[index]
        self.photo = ImageTk.PhotoImage(self.frame)
        self.loading.configure(image=self.photo, text='')
        self.loading.image = self.photo

        self._animation_id = self.loading.after(
            self.delay,
            lambda: self.animate_gif((index + 1) % len(self.frames))
        )

    def stop_animation(self):
        if self._animation_id is not None:
            self.loading.after_cancel(self._animation_id)
            self._animation_id = None

class FinishedGif:
    def __init__(self, config_obj):
        config_obj.stop_animation()
        config_obj.loading.configure(image=None)
        config_obj.loading.image = None
        print('[DEBUG] Animação removida da label')
