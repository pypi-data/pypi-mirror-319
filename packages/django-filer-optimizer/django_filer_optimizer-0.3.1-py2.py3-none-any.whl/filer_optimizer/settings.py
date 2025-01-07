from django.conf import settings
from .utils import setting


settings.THUMBNAIL_PREFIX = setting("THUMBNAIL_PREFIX", "thumbs_")

settings.THUMBNAIL_NAMER = setting(
    "THUMBNAIL_NAMER", "easy_thumbnails.namers.source_hashed"
)

settings.THUMBNAIL_HIGH_RESOLUTION = setting("THUMBNAIL_HIGH_RESOLUTION", True)

settings.THUMBNAIL_PROCESSORS = setting(
    "THUMBNAIL_PROCESSORS",
    (
        "easy_thumbnails.processors.colorspace",
        "easy_thumbnails.processors.autocrop",
        # 'easy_thumbnails.processors.scale_and_crop',
        "filer.thumbnail_processors.scale_and_crop_with_subject_location",
        "easy_thumbnails.processors.filters",
    ),
)

settings.THUMBNAIL_ALIASES = setting(
    "THUMBNAIL_ALIASES",
    {
        "default": {
            "head": {"size": (1920, 1080), "crop": True},
            "middle": {"size": (1080, 1620), "crop": True},
            "preview": {"size": (750, 480), "crop": True},
            "grid": {"size": (800, 720), "crop": True},
            "70": {"size": (70, 70), "crop": True},
            "130": {"size": (130, 130), "crop": True},
            "250": {"size": (250, 250), "crop": True},
        },
    },
)

settings.FILER_WEBP_QUALITY = setting("FILER_WEBP_QUALITY", 80)
settings.FILER_AVIF_QUALITY = setting("FILER_AVIF_QUALITY", 60)

# todo: this overwrite is not take in account by filer
settings.FILER_STORAGES = setting(
    "FILER_STORAGES",
    {
        "public": {
            "thumbnails": {
                "THUMBNAIL_OPTIONS": {"base_dir": ""},
            },
        },
    },
)
