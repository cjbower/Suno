from __future__ import annotations

import argparse
import contextlib
from dataclasses import replace
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from typing import Any

from tools.youtube import upload_private_video as uploader


FIXTURES = Path(__file__).parent / "fixtures"
CHANNEL_ID = "UCGtP5aRMQm5jc_XrDZOyX0Q"


def load_fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class FakeListRequest:
    def __init__(self, response: dict[str, object]) -> None:
        self.response = response
        self.kwargs: dict[str, object] | None = None

    def execute(self) -> dict[str, object]:
        return self.response


class FakeChannelResource:
    def __init__(self, response: dict[str, object]) -> None:
        self.request = FakeListRequest(response)

    def list(self, **kwargs: object) -> FakeListRequest:
        self.request.kwargs = kwargs
        return self.request


class FakeVideoResource:
    def __init__(self, response: dict[str, object] | None = None) -> None:
        self.request_args: dict[str, Any] | None = None
        self.response = response or {"id": "synthetic-video-id", "status": {"privacyStatus": "private"}}

    def insert(self, **kwargs: object) -> object:
        self.request_args = kwargs
        return self.response


class FakeService:
    def __init__(
        self,
        channels: list[dict[str, object]] | None = None,
        video_response: dict[str, object] | None = None,
    ) -> None:
        self.channel_resource = FakeChannelResource({"items": channels or []})
        self.video_resource = FakeVideoResource(video_response)
        self.channel_calls = 0
        self.video_calls = 0

    def channels(self) -> FakeChannelResource:
        self.channel_calls += 1
        return self.channel_resource

    def videos(self) -> FakeVideoResource:
        self.video_calls += 1
        return self.video_resource


def channel_record(channel_id: str = CHANNEL_ID, title: str = "Christopher Bower") -> dict[str, object]:
    return {"id": channel_id, "snippet": {"title": title}}


class TestWorkspace(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.manifest_path = self.root / "release.json"
        self.video_path = self.root / "source.mp4"
        self.token_path = self.root / "token.json"
        self.client_secret_path = self.root / "client_secret.json"
        self.expected_channel_path = self.root / "expected_channel_id"
        self.manifest_path.write_text(
            json.dumps(load_fixture("valid_release.json"), indent=2) + "\n",
            encoding="utf-8",
        )
        self.video_path.write_bytes(b"synthetic MP4 fixture bytes")
        self.token_path.write_text("synthetic token fixture, not an OAuth token\n", encoding="utf-8")
        self.client_secret_path.write_text("synthetic client secret fixture\n", encoding="utf-8")
        self.expected_channel_path.write_text(f"{CHANNEL_ID}\n", encoding="utf-8")
        for path in (self.token_path, self.client_secret_path):
            path.chmod(0o600)
        self.secret_path_patch = mock.patch.object(
            uploader, "DEFAULT_CLIENT_SECRET_FILE", self.client_secret_path
        )
        self.secret_path_patch.start()
        self.addCleanup(self.secret_path_patch.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def manifest_data(self) -> dict[str, object]:
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def write_manifest(self, data: dict[str, object]) -> Path:
        path = self.root / "another-release.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def valid_manifest(self) -> uploader.ReleaseManifest:
        return uploader.validate_manifest(self.manifest_path, CHANNEL_ID)

    def valid_video(self) -> uploader.VideoInfo:
        return uploader.validate_video(self.video_path)

    def insert_args(self, service: FakeService) -> dict[str, Any]:
        request_args = service.video_resource.request_args
        if request_args is None:
            raise AssertionError("videos.insert was not requested")
        return request_args


class ManifestValidationTests(TestWorkspace):
    def test_valid_manifest(self) -> None:
        manifest = self.valid_manifest()
        self.assertEqual(manifest.release_id, "psalm-2026-12-01-pop-punk-v1")
        self.assertEqual(manifest.tags, ("psalm", "pop punk", "original music"))
        self.assertTrue(manifest.contains_synthetic_media)

    def test_missing_manifest(self) -> None:
        with self.assertRaisesRegex(uploader.UploaderError, "does not exist"):
            uploader.validate_manifest(self.root / "missing.json", CHANNEL_ID)

    def test_malformed_json(self) -> None:
        self.manifest_path.write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(uploader.UploaderError, "valid JSON"):
            self.valid_manifest()

    def test_unsupported_schema_version(self) -> None:
        data = self.manifest_data()
        data["schema_version"] = "2.0.0"
        with self.assertRaisesRegex(uploader.UploaderError, "Unsupported manifest schema_version"):
            uploader.validate_manifest(self.write_manifest(data), CHANNEL_ID)

    def test_empty_release_id(self) -> None:
        data = self.manifest_data()
        data["release_id"] = " "
        with self.assertRaisesRegex(uploader.UploaderError, "release_id"):
            uploader.validate_manifest(self.write_manifest(data), CHANNEL_ID)

    def test_unsafe_release_id(self) -> None:
        data = self.manifest_data()
        data["release_id"] = "../unsafe"
        with self.assertRaisesRegex(uploader.UploaderError, "filesystem-safe"):
            uploader.validate_manifest(self.write_manifest(data), CHANNEL_ID)

    def test_empty_title(self) -> None:
        data = self.manifest_data()
        data["title"] = "  "
        with self.assertRaisesRegex(uploader.UploaderError, "title"):
            uploader.validate_manifest(self.write_manifest(data), CHANNEL_ID)

    def test_invalid_tags(self) -> None:
        data = self.manifest_data()
        data["tags"] = ["valid", 3]
        with self.assertRaisesRegex(uploader.UploaderError, "tags"):
            uploader.validate_manifest(self.write_manifest(data), CHANNEL_ID)

    def test_invalid_category_id(self) -> None:
        data = self.manifest_data()
        data["category_id"] = "music"
        with self.assertRaisesRegex(uploader.UploaderError, "category_id"):
            uploader.validate_manifest(self.write_manifest(data), CHANNEL_ID)

    def test_invalid_boolean_fields(self) -> None:
        for field, value in (("made_for_kids", "false"), ("contains_synthetic_media", 1)):
            with self.subTest(field=field):
                data = self.manifest_data()
                data[field] = value
                with self.assertRaisesRegex(uploader.UploaderError, field):
                    uploader.validate_manifest(self.write_manifest(data), CHANNEL_ID)

    def test_manifest_channel_mismatch(self) -> None:
        with self.assertRaisesRegex(uploader.UploaderError, "does not match"):
            uploader.validate_manifest(FIXTURES / "wrong_channel.json", CHANNEL_ID)

    def test_existing_video_id_refused(self) -> None:
        with self.assertRaisesRegex(uploader.UploaderError, "already set"):
            uploader.validate_manifest(FIXTURES / "existing_video_id.json", CHANNEL_ID)


class VideoValidationTests(TestWorkspace):
    def test_missing_video(self) -> None:
        with self.assertRaisesRegex(uploader.UploaderError, "does not exist"):
            uploader.validate_video(self.root / "missing.mp4")

    def test_empty_video(self) -> None:
        empty_path = self.root / "empty.mp4"
        empty_path.touch()
        with self.assertRaisesRegex(uploader.UploaderError, "nonempty"):
            uploader.validate_video(empty_path)

    def test_non_mp4_extension(self) -> None:
        other_path = self.root / "source.mov"
        other_path.write_bytes(b"synthetic video")
        with self.assertRaisesRegex(uploader.UploaderError, "extension"):
            uploader.validate_video(other_path)

    def test_incorrect_mime_type(self) -> None:
        with mock.patch.object(uploader.mimetypes, "guess_type", return_value=("application/octet-stream", None)):
            with self.assertRaisesRegex(uploader.UploaderError, "MIME type"):
                uploader.validate_video(self.video_path)

    def test_sha256_calculation(self) -> None:
        result = self.valid_video()
        self.assertEqual(result.size_bytes, len(b"synthetic MP4 fixture bytes"))
        self.assertEqual(result.sha256, hashlib.sha256(self.video_path.read_bytes()).hexdigest())


class CredentialValidationTests(TestWorkspace):
    def test_missing_token(self) -> None:
        with self.assertRaisesRegex(uploader.UploaderError, "does not exist"):
            uploader.validate_credential_file(self.root / "missing-token.json", "OAuth token")

    def test_insecure_token_permissions(self) -> None:
        self.token_path.chmod(0o644)
        with self.assertRaisesRegex(uploader.UploaderError, "permissions are insecure"):
            uploader.validate_credential_file(self.token_path, "OAuth token")

    def test_missing_expected_channel_file(self) -> None:
        with self.assertRaisesRegex(uploader.UploaderError, "does not exist"):
            uploader.read_expected_channel_id(self.root / "missing-channel-id")


class ChannelIdentityTests(TestWorkspace):
    def test_zero_authenticated_channels(self) -> None:
        service = FakeService()
        with self.assertRaisesRegex(uploader.UploaderError, "received 0"):
            uploader.validate_authenticated_channel(service, CHANNEL_ID)

    def test_multiple_authenticated_channels(self) -> None:
        service = FakeService([channel_record(), channel_record("UC0000000000000000000000", "Other")])
        with self.assertRaisesRegex(uploader.UploaderError, "received 2"):
            uploader.validate_authenticated_channel(service, CHANNEL_ID)

    def test_wrong_authenticated_channel(self) -> None:
        service = FakeService([channel_record("UC0000000000000000000000", "Other")])
        with self.assertRaisesRegex(uploader.UploaderError, "channel mismatch"):
            uploader.validate_authenticated_channel(service, CHANNEL_ID)

    def test_correct_authenticated_channel_uses_mine_guard(self) -> None:
        service = FakeService([channel_record()])
        channel = uploader.validate_authenticated_channel(service, CHANNEL_ID)
        self.assertEqual(channel.channel_id, CHANNEL_ID)
        self.assertEqual(channel.title, "Christopher Bower")
        self.assertEqual(service.channel_resource.request.kwargs, {"part": "id,snippet", "mine": True})


class DryRunTests(TestWorkspace):
    def test_dry_run_never_invokes_videos_insert_and_preserves_inputs(self) -> None:
        manifest_before = self.manifest_path.read_bytes()
        video_before = self.video_path.read_bytes()
        service = FakeService([channel_record()])
        args = argparse_namespace(self, dry_run=True)
        with mock.patch.object(uploader, "load_credentials", return_value=object()), mock.patch.object(
            uploader, "build_youtube_service", return_value=service
        ), contextlib.redirect_stderr(io.StringIO()):
            receipt, _ = uploader.run_upload(args)
        self.assertEqual(service.video_calls, 0)
        self.assertFalse(receipt["upload_performed"])
        self.assertIsNone(receipt["video"]["id"])
        self.assertIsNone(receipt["video"]["url"])
        self.assertEqual(receipt["video"]["privacy_status"], "private")
        self.assertEqual(receipt["notify_subscribers"], False)
        self.assertEqual(receipt["expected_channel_id"], CHANNEL_ID)
        self.assertEqual(manifest_before, self.manifest_path.read_bytes())
        self.assertEqual(video_before, self.video_path.read_bytes())


class RequestMappingTests(TestWorkspace):
    def test_videos_insert_is_private(self) -> None:
        service = FakeService()
        uploader.build_insert_request(
            service,
            self.valid_manifest(),
            self.valid_video(),
            media_upload_factory=lambda *args, **kwargs: ("media", args, kwargs),
        )
        body = self.insert_args(service)["body"]
        self.assertEqual(body["status"]["privacyStatus"], "private")

    def test_notify_subscribers_is_false(self) -> None:
        service = FakeService()
        uploader.build_insert_request(
            service,
            self.valid_manifest(),
            self.valid_video(),
            media_upload_factory=mock.Mock(return_value=object()),
        )
        self.assertIs(self.insert_args(service)["notifySubscribers"], False)

    def test_metadata_is_mapped_correctly(self) -> None:
        service = FakeService()
        manifest = self.valid_manifest()
        media_calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

        def fake_media(*args: object, **kwargs: object) -> object:
            media_calls.append((args, kwargs))
            return object()

        uploader.build_insert_request(service, manifest, self.valid_video(), media_upload_factory=fake_media)
        request = self.insert_args(service)
        self.assertEqual(request["part"], "snippet,status")
        self.assertEqual(
            request["body"]["snippet"],
            {
                "title": manifest.title,
                "description": manifest.description,
                "tags": list(manifest.tags),
                "categoryId": manifest.category_id,
            },
        )
        self.assertEqual(media_calls[0][1], {
            "mimetype": "video/mp4",
            "chunksize": uploader.CHUNK_SIZE_BYTES,
            "resumable": True,
        })

    def test_contains_synthetic_media_is_mapped(self) -> None:
        manifest = replace(self.valid_manifest(), contains_synthetic_media=True)
        body = uploader.build_video_insert_body(manifest)
        self.assertIs(body["status"]["containsSyntheticMedia"], True)

    def test_made_for_kids_value_is_mapped(self) -> None:
        manifest = replace(self.valid_manifest(), made_for_kids=True)
        body = uploader.build_video_insert_body(manifest)
        self.assertIs(body["status"]["selfDeclaredMadeForKids"], True)

    def test_resumable_media_is_mp4_with_deliberate_chunk_size(self) -> None:
        service = FakeService()
        media_args: list[tuple[tuple[object, ...], dict[str, object]]] = []

        def fake_media(*args: object, **kwargs: object) -> object:
            media_args.append((args, kwargs))
            return object()

        uploader.build_insert_request(
            service, self.valid_manifest(), self.valid_video(), media_upload_factory=fake_media
        )
        self.assertEqual(media_args[0][1]["mimetype"], "video/mp4")
        self.assertEqual(media_args[0][1]["chunksize"], 8 * 1024 * 1024)
        self.assertIs(media_args[0][1]["resumable"], True)


class UploadResponseTests(TestWorkspace):
    def test_successful_private_upload_returns_receipt(self) -> None:
        service = FakeService([channel_record()])
        args = argparse_namespace(self, dry_run=False)
        with mock.patch.object(uploader, "load_credentials", return_value=object()), mock.patch.object(
            uploader, "build_youtube_service", return_value=service
        ), mock.patch.object(uploader, "build_insert_request", return_value=object()), mock.patch.object(
            uploader,
            "upload_resumable",
            return_value={"id": "synthetic-video-id", "status": {"privacyStatus": "private"}},
        ), contextlib.redirect_stderr(io.StringIO()):
            receipt, _ = uploader.run_upload(args)
        self.assertEqual(receipt["video"]["id"], "synthetic-video-id")
        self.assertEqual(receipt["video"]["url"], "https://www.youtube.com/watch?v=synthetic-video-id")
        self.assertTrue(receipt["upload_performed"])

    def test_returned_video_id_is_required(self) -> None:
        service = FakeService([channel_record()])
        args = argparse_namespace(self, dry_run=False)
        with mock.patch.object(uploader, "load_credentials", return_value=object()), mock.patch.object(
            uploader, "build_youtube_service", return_value=service
        ), mock.patch.object(uploader, "build_insert_request", return_value=object()), mock.patch.object(
            uploader, "upload_resumable", return_value={"status": {"privacyStatus": "private"}}
        ), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(uploader.UploaderError, "did not contain a video ID"):
                uploader.run_upload(args)

    def test_returned_privacy_status_must_be_private(self) -> None:
        service = FakeService([channel_record()])
        args = argparse_namespace(self, dry_run=False)
        with mock.patch.object(uploader, "load_credentials", return_value=object()), mock.patch.object(
            uploader, "build_youtube_service", return_value=service
        ), mock.patch.object(uploader, "build_insert_request", return_value=object()), mock.patch.object(
            uploader,
            "upload_resumable",
            return_value={"id": "synthetic-video-id", "status": {"privacyStatus": "public"}},
        ), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(uploader.UploaderError, "did not confirm private status"):
                uploader.run_upload(args)


class ReceiptTests(TestWorkspace):
    def receipt(self) -> dict[str, object]:
        return uploader.make_receipt(
            self.valid_manifest(),
            self.valid_video(),
            uploader.ChannelInfo(CHANNEL_ID, "Christopher Bower"),
            video_id="synthetic-video-id",
            upload_performed=True,
        )

    def test_existing_receipt_is_refused(self) -> None:
        receipt_path = self.root / "receipt.json"
        receipt_path.write_text("existing", encoding="utf-8")
        with self.assertRaisesRegex(uploader.UploaderError, "already exists"):
            uploader.write_receipt(receipt_path, self.receipt())

    def test_receipt_write_is_atomic_and_private(self) -> None:
        receipt_path = self.root / "receipt.json"
        uploader.write_receipt(receipt_path, self.receipt())
        self.assertEqual(json.loads(receipt_path.read_text(encoding="utf-8")), self.receipt())
        self.assertEqual(receipt_path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(list(self.root.glob(".receipt.json.*.tmp")), [])

    def test_temporary_receipt_is_cleaned_after_failure(self) -> None:
        receipt_path = self.root / "receipt.json"
        with mock.patch.object(uploader.os, "link", side_effect=OSError("synthetic link failure")):
            with self.assertRaisesRegex(uploader.UploaderError, "publish receipt atomically"):
                uploader.write_receipt(receipt_path, self.receipt())
        self.assertFalse(receipt_path.exists())
        self.assertEqual(list(self.root.glob(".receipt.json.*.tmp")), [])

    def test_receipt_contains_no_secret_fields_or_values(self) -> None:
        serialized = uploader.serialize_receipt(self.receipt())
        for forbidden in ("client_secret", "access_token", "refresh_token", "token.json"):
            self.assertNotIn(forbidden, serialized)
        self.assertNotIn("synthetic client secret fixture", serialized)
        self.assertNotIn("synthetic token fixture", serialized)

    def test_receipt_serialization_is_deterministic(self) -> None:
        receipt = self.receipt()
        self.assertEqual(uploader.serialize_receipt(receipt), uploader.serialize_receipt(receipt))

    def test_manifest_and_video_are_not_modified(self) -> None:
        manifest_before = self.manifest_path.read_bytes()
        video_before = self.video_path.read_bytes()
        _ = self.valid_manifest()
        _ = self.valid_video()
        self.assertEqual(manifest_before, self.manifest_path.read_bytes())
        self.assertEqual(video_before, self.video_path.read_bytes())


class RetryTests(TestWorkspace):
    class HttpError(Exception):
        def __init__(self, status: int) -> None:
            self.resp = type("Response", (), {"status": status})()

    class FakeRequest:
        def __init__(self, outcomes: list[object]) -> None:
            self.outcomes = outcomes
            self.calls = 0

        def next_chunk(self, *, num_retries: int) -> tuple[None, dict[str, object] | None]:
            self.calls += 1
            if num_retries != 0:
                raise AssertionError("SDK retries must remain disabled; retry policy is explicit.")
            outcome = self.outcomes.pop(0)
            if isinstance(outcome, BaseException):
                raise outcome
            return None, outcome  # type: ignore[return-value]

    def test_transient_retry_is_bounded(self) -> None:
        request = self.FakeRequest(
            [self.HttpError(503), self.HttpError(503), self.HttpError(503), {"id": "done"}]
        )
        sleeps: list[float] = []
        with mock.patch.object(uploader, "retry_exception_types", return_value=(self.HttpError,)):
            response = uploader.upload_resumable(request, report=lambda _: None, sleeper=sleeps.append)
        self.assertEqual(response, {"id": "done"})
        self.assertEqual(request.calls, 4)
        self.assertEqual(sleeps, [1.0, 2.0, 4.0])

    def test_deterministic_4xx_is_not_retried(self) -> None:
        request = self.FakeRequest([self.HttpError(400), {"id": "must-not-run"}])
        sleeps: list[float] = []
        with mock.patch.object(uploader, "retry_exception_types", return_value=(self.HttpError,)):
            with self.assertRaisesRegex(uploader.UploaderError, "HTTP 400"):
                uploader.upload_resumable(request, report=lambda _: None, sleeper=sleeps.append)
        self.assertEqual(request.calls, 1)
        self.assertEqual(sleeps, [])


class CliBoundaryTests(TestWorkspace):
    def test_no_public_unlisted_schedule_or_delete_options(self) -> None:
        parser = uploader.build_parser()
        options = {
            option
            for action in parser._actions
            for option in action.option_strings
        }
        for forbidden in (
            "--privacy",
            "--public",
            "--unlisted",
            "--publish-at",
            "--schedule",
            "--delete",
            "--output",
        ):
            self.assertNotIn(forbidden, options)

    def test_help_contains_only_supported_optional_paths_and_dry_run(self) -> None:
        help_text = uploader.build_parser().format_help()
        for forbidden in (
            "--privacy",
            "--public",
            "--unlisted",
            "--publish-at",
            "--schedule",
            "--delete",
            "--output",
        ):
            self.assertNotIn(forbidden, help_text)
        for option in ("--manifest", "--video", "--token-file", "--expected-channel-id-file", "--receipt-output", "--dry-run"):
            self.assertIn(option, help_text)

    def test_no_live_upload_during_tests(self) -> None:
        service = FakeService([channel_record()])
        args = argparse_namespace(self, dry_run=True)
        with mock.patch.object(uploader, "load_credentials", return_value=object()), mock.patch.object(
            uploader, "build_youtube_service", return_value=service
        ), contextlib.redirect_stderr(io.StringIO()):
            receipt, _ = uploader.run_upload(args)
        self.assertFalse(receipt["upload_performed"])
        self.assertEqual(service.video_calls, 0)

    def test_stdout_is_json_receipt_and_dry_run_writes_no_file(self) -> None:
        receipt = uploader.make_receipt(
            self.valid_manifest(),
            self.valid_video(),
            uploader.ChannelInfo(CHANNEL_ID, "Christopher Bower"),
            video_id=None,
            upload_performed=False,
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(uploader, "run_upload", return_value=(receipt, None)), contextlib.redirect_stdout(
            stdout
        ), contextlib.redirect_stderr(stderr):
            exit_code = uploader.main(
                ["--manifest", str(self.manifest_path), "--video", str(self.video_path), "--dry-run"]
            )
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(stdout.getvalue()), receipt)
        self.assertEqual(stderr.getvalue(), "")
        self.assertFalse((self.root / "receipt.json").exists())


def argparse_namespace(test: TestWorkspace, *, dry_run: bool) -> argparse.Namespace:
    return argparse.Namespace(
        manifest=test.manifest_path,
        video=test.video_path,
        token_file=test.token_path,
        expected_channel_id_file=test.expected_channel_path,
        receipt_output=None,
        dry_run=dry_run,
    )


if __name__ == "__main__":
    unittest.main()
