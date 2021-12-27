import os


class ExportManager():
    def __init__(self, root_dir: str = './export-res'):
        try:
            os.makedirs(root_dir + '/frames')
        except FileExistsError:
            pass

        self._frame_cnt: int = 0
        self._root_dir: str = root_dir

    @property
    def frame_name(self) -> str:
        return self._root_dir + f'/frames/{self._frame_cnt:05d}.png'

    def gen_video(self) -> None:
        print('export .mp4 video...')
        os.chdir(self._root_dir + '/frames')
        os.system('ti video -f24')
        os.system('mv video.mp4 ../')

    def gen_gif(self) -> None:
        print('export .gif ...')
        os.system('ti gif -i video.mp4 -f24')
        os.system('mv video.gif ../')
