from pathlib import Path
from threading import Thread
from time import sleep
import os

from colorama import Fore, init, deinit
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEvent, FileSystemEventHandler,
    FileCreatedEvent, FileModifiedEvent
)

from voltfiles import out
from voltfiles import colors
from voltfiles import extensions


DOWNLOAD_MODIFY_THRESHOLD: int = 4
DOWNLOAD_VERIFY_THRESHOLD: int = 1


volt_files_path: Path = Path(__file__).parent.resolve()

downloads_path: Path = Path.home() / "Downloads"
downloads_pdf_path: Path = downloads_path / "PDF"
downloads_image_path: Path = downloads_path / "Images"
downloads_audio_path: Path = downloads_path / "Audio"
downloads_compressed_path: Path = downloads_path / "Compressed"
downloads_other_path: Path = downloads_path / "Other"

modify_counter: dict[str, int] = {}


class OrganizingFileHandler(FileSystemEventHandler):
    def dispatch(self, event: FileSystemEvent) -> None:
        if isinstance(event, FileModifiedEvent):
            file_extension: str = Path(event.src_path).suffix[1:]

            if event.src_path not in modify_counter.keys():
                modify_counter[event.src_path] = 1
            else:
                modify_counter[event.src_path] += 1

            if modify_counter[event.src_path] < DOWNLOAD_MODIFY_THRESHOLD:
                return

            del modify_counter[event.src_path]

            destination: Path

            if file_extension in extensions.COMPRESSED:
                destination = downloads_compressed_path
            elif file_extension in extensions.IMAGE:
                destination = downloads_image_path
            elif file_extension in extensions.AUDIO:
                destination = downloads_audio_path
            elif file_extension in extensions.PDF:
                destination = downloads_pdf_path
            else:
                destination = downloads_other_path

            Thread(
                target=move_file_timed,
                args=(
                    Path(event.src_path),
                    destination,
                    DOWNLOAD_VERIFY_THRESHOLD
                ),
            ).start()


def move_file_timed(origin: Path, destination: Path, delay: float) -> None:
    sleep(delay)

    try:
        origin.replace(destination / origin.name)
        out.out(
            f"{colors.SPECIAL}{origin}"
            f"{colors.INFO} moved to "
            f"{colors.SPECIAL}{destination}"
        )
    except:
        out.error(f"Can't move file {origin}")


def ensure_paths() -> None:
    out.info("Ensuring directory structures...")

    downloads_pdf_path.mkdir(exist_ok=True)
    downloads_image_path.mkdir(exist_ok=True)
    downloads_audio_path.mkdir(exist_ok=True)
    downloads_compressed_path.mkdir(exist_ok=True)
    downloads_other_path.mkdir(exist_ok=True)

    out.info("Directory structures found or created.")


def show_title() -> None:
    with (volt_files_path / "title.txt").open("r") as title:
        print(Fore.MAGENTA + "".join([line for line in title.readlines()]))


def start_watching() -> None:
    event_handler: OrganizingFileHandler = OrganizingFileHandler()

    observer: Observer = Observer()
    observer.schedule(event_handler, downloads_path)
    observer.start()

    out.info("Listening to file changes...\n")

    try:
        while observer.is_alive():
            observer.join(1.0)
    except KeyboardInterrupt:
        print()
        out.info("Stopping Volt Files...")
    finally:
        observer.stop()
        observer.join()


init()

show_title()

out.info("Starting Volt Files...")

ensure_paths()
start_watching()

deinit()
