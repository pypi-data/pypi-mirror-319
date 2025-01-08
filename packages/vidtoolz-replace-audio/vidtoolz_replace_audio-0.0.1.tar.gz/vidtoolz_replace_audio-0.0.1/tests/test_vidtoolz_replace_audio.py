import pytest
import vidtoolz_replace_audio as w

from argparse import Namespace, ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(["video.mp4", "audio.mp3"])
    assert result.video == "video.mp4"
    assert result.audio == "audio.mp3"
    assert result.output == "output.mp4"
    assert result.volume == 30


def test_plugin(capsys):
    w.repaudio_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out
