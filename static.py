import os

FLET_APP_STORAGE_DATA = os.getenv("FLET_APP_STORAGE_DATA")
FLET_APP_CONSOLE = os.getenv("FLET_APP_CONSOLE")

MEDIA_PATH = os.path.join(FLET_APP_STORAGE_DATA, "media")
MUSIC_PATH = os.path.join(MEDIA_PATH, "music")
VIDEO_PATH = os.path.join(MEDIA_PATH, "video")
IMAGE_PATH = os.path.join(MEDIA_PATH, "image")


def init_path():
    if not os.path.exists(MEDIA_PATH):
        os.makedirs(MEDIA_PATH)
    if not os.path.exists(MUSIC_PATH):
        os.makedirs(MUSIC_PATH)
    if not os.path.exists(VIDEO_PATH):
        os.makedirs(VIDEO_PATH)