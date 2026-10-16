# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import import_media
import pytest


def test_validate_video_media(monkeypatch, tmp_path):
    monkeypatch.setattr(import_media, "MEDIA_DIR", tmp_path)
    video = tmp_path / "videos" / "M1-001.mp4"
    video.parent.mkdir(parents=True)
    video.write_bytes(b"test")

    result = import_media.validate_item(
        {
            "media_id": "M1-001-video-01",
            "knowledge_point_id": "M1-001",
            "type": "video",
            "title": "测试视频",
            "file": "videos/M1-001.mp4",
            "order": 1,
        },
        apply_changes=True,
    )

    assert result["url"] == "/media/videos/M1-001.mp4"
    assert result["format"] == "mp4"


def test_media_path_traversal_is_rejected(monkeypatch, tmp_path):
    monkeypatch.setattr(import_media, "MEDIA_DIR", tmp_path)
    with pytest.raises(ValueError):
        import_media.validate_item(
            {
                "media_id": "bad-media",
                "knowledge_point_id": "M1-001",
                "type": "video",
                "title": "非法路径",
                "file": "../outside.mp4",
            },
            apply_changes=False,
        )


def test_invalid_media_extension_is_rejected(monkeypatch, tmp_path):
    monkeypatch.setattr(import_media, "MEDIA_DIR", tmp_path)
    with pytest.raises(ValueError):
        import_media.validate_item(
            {
                "media_id": "bad-extension",
                "knowledge_point_id": "M1-001",
                "type": "slides",
                "title": "错误课件",
                "file": "slides/demo.exe",
            },
            apply_changes=False,
        )

