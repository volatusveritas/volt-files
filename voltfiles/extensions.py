from typing import TypeAlias


ExtensionList: TypeAlias = tuple[str, ...]


COMPRESSED: ExtensionList = (
    "7z",
    "s7z",
    "apk",
    "zip",
)

IMAGE: ExtensionList = (
    "png",
    "gif",
    "ico",
    "jpg",
    "jpeg",
    "png",
)

AUDIO: ExtensionList = (
    "wav",
    "flac",
    "mp3",
    "ogg",
)

PDF: ExtensionList = (
    "pdf",
)

ALL: ExtensionList = COMPRESSED + IMAGE + AUDIO + PDF
