"""Music helpers.

These functions are intentionally non-blocking.

Historically, calling `pygame.mixer.init()` and `pygame.mixer.music.load()` directly
from the main loop could stall gameplay while MP3s were initialized/loaded.

We fix that by executing all mixer operations on a single background worker thread
(serialized), so callers can request music changes without blocking rendering/input.
"""

from __future__ import annotations

import queue
import threading
from typing import Callable

import pygame


_task_queue: "queue.Queue[Callable[[], None]]" = queue.Queue()
_worker_started = False
_worker_lock = threading.Lock()
_mixer_ready = False


def _ensure_worker_started() -> None:
    global _worker_started
    if _worker_started:
        return
    with _worker_lock:
        if _worker_started:
            return
        thread = threading.Thread(target=_worker_loop, name="music-worker", daemon=True)
        thread.start()
        _worker_started = True


def _worker_loop() -> None:
    while True:
        task = _task_queue.get()
        try:
            task()
        except Exception as exc:  # Avoid killing the worker on audio errors
            print(f"Music worker error: {exc}")
        finally:
            _task_queue.task_done()


def _enqueue(task: Callable[[], None]) -> None:
    _ensure_worker_started()
    _task_queue.put(task)


def _ensure_mixer_ready() -> None:
    global _mixer_ready
    if _mixer_ready:
        return
    try:
        pygame.mixer.init()
        _mixer_ready = True
    except pygame.error as e:
        print(f"Error initializing mixer: {e}")


def _play_music(path: str, *, loop: bool, volume: float) -> None:
    _ensure_mixer_ready()
    if not _mixer_ready:
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0)
    except pygame.error as e:
        print(f"Error loading music '{path}': {e}")


def load_music() -> None:
    """Start gameplay background music (async)."""
    _enqueue(lambda: _play_music("assets/music.mp3", loop=True, volume=0.5))


def load_main_menu_music() -> None:
    """Start main menu music (async)."""
    _enqueue(lambda: _play_music("assets/mainmenu.mp3", loop=True, volume=0.5))


def victory_music() -> None:
    """Play victory music once (async)."""
    _enqueue(lambda: _play_music("assets/victory.mp3", loop=False, volume=0.5))


def defeat_music() -> None:
    """Play defeat music once (async)."""
    _enqueue(lambda: _play_music("assets/defeat.mp3", loop=False, volume=0.5))


def stop_music() -> None:
    """Stop current music (async)."""

    def _stop() -> None:
        _ensure_mixer_ready()
        if not _mixer_ready:
            return
        try:
            pygame.mixer.music.stop()
        except pygame.error as e:
            print(f"Error stopping music: {e}")

    _enqueue(_stop)
