#!/usr/bin/env python3
# Script name: upload_private_video.py
# Purpose: Validate and upload one release video to YouTube as private.
# Semantic version: 1.0.0
# Author: Christopher Bower
# Description: Performs guarded, resumable uploads and emits a deterministic local receipt.
# Requirements and dependencies: Python 3.10+; Google API Python Client, google-auth-oauthlib,
#                               google-auth-httplib2.
# Usage examples:
#   python3 tools/youtube/upload_private_video.py --manifest release.json --video song.mp4 --dry-run
#   python3 tools/youtube/upload_private_video.py --manifest release.json --video song.mp4
# Revision history:
#   2026-11-24 1.0.0 Initial private-only resumable YouTube uploader.

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import socket
import ssl
import stat
import sys
import tempfile
import time
from typing import Any, Callable, Sequence


VERSION = "1.0.0"
SUPPORTED_SCHEMA_VERSION = "1.0.0"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
OAUTH_SCOPES = (YOUTUBE_READONLY_SCOPE, YOUTUBE_UPLOAD_SCOPE)
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v="
PRIVACY_STATUS = "private"
NOTIFY_SUBSCRIBERS = False
CHUNK_SIZE_BYTES = 8 * 1024 * 1024
MAX_CHUNK_RETRIES = 3
BASE_RETRY_DELAY_SECONDS = 1.0
MAX_RETRY_DELAY_SECONDS = 8.0
HASH_CHUNK_SIZE_BYTES = 1024 * 1024
CHANNEL_ID_PATTERN = re.compile(r"UC[A-Za-z0-9_-]{22}\Z")
RELEASE_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")

CONFIG_DIRECTORY = Path.home() / ".config" / "psalm-music-automation"
DEFAULT_CLIENT_SECRET_FILE = CONFIG_DIRECTORY / "client_secret.json"
DEFAULT_TOKEN_FILE = CONFIG_DIRECTORY / "token.json"
DEFAULT_EXPECTED_CHANNEL_ID_FILE = CONFIG_DIRECTORY / "expected_channel_id"


class UploaderError(Exception):
    """Expected validation, authentication, API, or output failure."""


class UploadResponseError(UploaderError):
    def __init__(self, message: str, receipt: dict[str, Any]) -> None:
        super().__init__(message)
        self.receipt = receipt


@dataclass(frozen=True)
class ReleaseManifest:
    release_id: str
    title: str
    description: str
    tags: tuple[str, ...]
    category_id: str
    made_for_kids: bool
    contains_synthetic_media: bool
    expected_channel_id: str
    video_id: str | None


@dataclass(frozen=True)
class VideoInfo:
    path: Path
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class ChannelInfo:
    channel_id: str
    title: str


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as source:
            value = json.load(source)
    except FileNotFoundError as exc:
        raise UploaderError(f"{label} file does not exist: {path}.") from exc
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UploaderError(f"Unable to read valid JSON from {label} file: {path}.") from exc
    if not isinstance(value, dict):
        raise UploaderError(f"{label} must contain a JSON object.")
    return value


def read_expected_channel_id(path: Path) -> str:
    try:
        channel_id = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise UploaderError(f"Expected-channel-ID file does not exist: {path}.") from exc
    except (OSError, UnicodeDecodeError) as exc:
        raise UploaderError(f"Unable to read expected-channel-ID file: {path}.") from exc
    if not CHANNEL_ID_PATTERN.fullmatch(channel_id):
        raise UploaderError("Expected-channel-ID file must contain one valid YouTube channel ID.")
    return channel_id


def validate_credential_file(path: Path, label: str) -> None:
    try:
        file_stat = path.stat()
    except FileNotFoundError as exc:
        raise UploaderError(f"{label} file does not exist: {path}.") from exc
    except OSError as exc:
        raise UploaderError(f"Unable to inspect {label} file: {path}.") from exc
    if not stat.S_ISREG(file_stat.st_mode):
        raise UploaderError(f"{label} path must be a regular file: {path}.")
    if not os.access(path, os.R_OK):
        raise UploaderError(f"{label} file is not readable: {path}.")
    if os.name == "posix" and stat.S_IMODE(file_stat.st_mode) not in (0o400, 0o600):
        raise UploaderError(f"{label} file permissions are insecure; restrict access to its owner.")


def validate_manifest(path: Path, expected_channel_id: str) -> ReleaseManifest:
    data = _read_json_object(path, "Release manifest")
    if data.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        raise UploaderError(f"Unsupported manifest schema_version; expected {SUPPORTED_SCHEMA_VERSION}.")

    release_id = data.get("release_id")
    if not isinstance(release_id, str) or not RELEASE_ID_PATTERN.fullmatch(release_id):
        raise UploaderError("release_id must be nonempty and filesystem-safe.")

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        raise UploaderError("title must be a nonempty string.")

    description = data.get("description")
    if not isinstance(description, str):
        raise UploaderError("description must be a string.")

    tags = data.get("tags")
    if (
        not isinstance(tags, list)
        or any(not isinstance(tag, str) or not tag.strip() for tag in tags)
    ):
        raise UploaderError("tags must be a list of nonempty strings.")

    category_id = data.get("category_id")
    if not isinstance(category_id, str) or not re.fullmatch(r"[0-9]+", category_id):
        raise UploaderError("category_id must be a numeric string.")

    made_for_kids = data.get("made_for_kids")
    if type(made_for_kids) is not bool:
        raise UploaderError("made_for_kids must be a Boolean.")

    contains_synthetic_media = data.get("contains_synthetic_media")
    if type(contains_synthetic_media) is not bool:
        raise UploaderError("contains_synthetic_media must be a Boolean.")

    youtube = data.get("youtube")
    if not isinstance(youtube, dict):
        raise UploaderError("youtube must be an object.")
    manifest_channel_id = youtube.get("expected_channel_id")
    if manifest_channel_id != expected_channel_id:
        raise UploaderError("Manifest expected_channel_id does not match the local expected channel ID.")
    video_id = youtube.get("video_id")
    if video_id is not None:
        raise UploaderError("Manifest youtube.video_id is already set; refusing a duplicate upload.")

    return ReleaseManifest(
        release_id=release_id,
        title=title,
        description=description,
        tags=tuple(tags),
        category_id=category_id,
        made_for_kids=made_for_kids,
        contains_synthetic_media=contains_synthetic_media,
        expected_channel_id=expected_channel_id,
        video_id=None,
    )


def validate_video(path: Path) -> VideoInfo:
    try:
        expanded_path = path.expanduser()
        resolved_path = expanded_path.resolve(strict=True)
        file_stat = resolved_path.stat()
    except FileNotFoundError as exc:
        raise UploaderError(f"Video file does not exist: {path}.") from exc
    except OSError as exc:
        raise UploaderError(f"Unable to inspect video file: {path}.") from exc

    if expanded_path.is_symlink() or not stat.S_ISREG(file_stat.st_mode):
        raise UploaderError("Video path must refer to a regular, non-symlink file.")
    if not os.access(resolved_path, os.R_OK):
        raise UploaderError("Video file is not readable.")
    if resolved_path.suffix.lower() != ".mp4":
        raise UploaderError("Video file extension must be .mp4.")
    if mimetypes.guess_type(resolved_path.name)[0] != "video/mp4":
        raise UploaderError("Video filename must resolve to MIME type video/mp4.")
    if file_stat.st_size <= 0:
        raise UploaderError("Video file must be nonempty.")

    digest = hashlib.sha256()
    try:
        with resolved_path.open("rb") as source:
            while chunk := source.read(HASH_CHUNK_SIZE_BYTES):
                digest.update(chunk)
    except OSError as exc:
        raise UploaderError("Unable to read video file for SHA-256 validation.") from exc
    return VideoInfo(path=resolved_path, size_bytes=file_stat.st_size, sha256=digest.hexdigest())


def google_auth_exception_types() -> tuple[type[BaseException], ...]:
    try:
        from google.auth.exceptions import GoogleAuthError
        import httplib2
    except ImportError as exc:
        raise UploaderError(
            "Google API dependencies are missing; install tools/youtube/requirements.txt."
        ) from exc
    return (GoogleAuthError, httplib2.HttpLib2Error)


def google_api_exception_types() -> tuple[type[BaseException], ...]:
    try:
        from googleapiclient.errors import Error as GoogleApiError
        import httplib2
    except ImportError as exc:
        raise UploaderError(
            "Google API dependencies are missing; install tools/youtube/requirements.txt."
        ) from exc
    return (GoogleApiError, httplib2.HttpLib2Error)


def retry_exception_types() -> tuple[type[BaseException], ...]:
    return (*google_api_exception_types(), OSError, ssl.SSLError, socket.timeout)


def transient_network_exception_types() -> tuple[type[BaseException], ...]:
    try:
        import httplib2
    except ImportError as exc:
        raise UploaderError(
            "Google API dependencies are missing; install tools/youtube/requirements.txt."
        ) from exc
    return (OSError, ssl.SSLError, socket.timeout, httplib2.HttpLib2Error)


def load_credentials(token_path: Path) -> Any:
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
    except ImportError as exc:
        raise UploaderError(
            "Google API dependencies are missing; install tools/youtube/requirements.txt."
        ) from exc

    try:
        credentials = Credentials.from_authorized_user_file(str(token_path), scopes=OAUTH_SCOPES)
    except (OSError, ValueError, UnicodeDecodeError, *google_auth_exception_types()) as exc:
        raise UploaderError("Unable to load the local OAuth token; verify authorization and file format.") from exc

    granted_scopes = credentials.granted_scopes or credentials.scopes
    if granted_scopes is not None and not set(OAUTH_SCOPES).issubset(set(granted_scopes)):
        raise UploaderError("OAuth token is missing one or more required YouTube API scopes.")
    if credentials.expired or not credentials.token:
        if not credentials.refresh_token:
            raise UploaderError("OAuth token is expired and has no refresh token.")
        try:
            credentials.refresh(Request())
        except (*google_auth_exception_types(), OSError, ssl.SSLError, socket.timeout) as exc:
            raise UploaderError("OAuth access-token refresh failed.") from exc
    return credentials


def build_youtube_service(credentials: Any) -> Any:
    try:
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise UploaderError(
            "Google API dependencies are missing; install tools/youtube/requirements.txt."
        ) from exc
    try:
        return build("youtube", "v3", credentials=credentials, cache_discovery=False)
    except google_api_exception_types() as exc:
        raise UploaderError("Unable to initialize the YouTube Data API client.") from exc


def validate_authenticated_channel(service: Any, expected_channel_id: str) -> ChannelInfo:
    try:
        response = (
            service.channels()
            .list(part="id,snippet", mine=True)
            .execute()
        )
    except (*google_api_exception_types(), OSError, ssl.SSLError, socket.timeout) as exc:
        status = _http_status(exc)
        suffix = f" (HTTP {status})" if status is not None else ""
        raise UploaderError(f"YouTube channel identity request failed{suffix}.") from exc

    channels = response.get("items") if isinstance(response, dict) else None
    if not isinstance(channels, list) or len(channels) != 1:
        count = len(channels) if isinstance(channels, list) else 0
        raise UploaderError(f"Expected exactly one authenticated YouTube channel; received {count}.")
    item = channels[0]
    if not isinstance(item, dict):
        raise UploaderError("YouTube returned an invalid authenticated-channel record.")
    channel_id = item.get("id")
    snippet = item.get("snippet")
    title = snippet.get("title") if isinstance(snippet, dict) else None
    if (
        not isinstance(channel_id, str)
        or not CHANNEL_ID_PATTERN.fullmatch(channel_id)
        or not isinstance(title, str)
    ):
        raise UploaderError("YouTube channel response has an invalid ID or is missing its title.")
    if channel_id != expected_channel_id:
        raise UploaderError(
            f"Authenticated channel mismatch: expected {expected_channel_id}, received {channel_id}."
        )
    return ChannelInfo(channel_id=channel_id, title=title)


def build_video_insert_body(manifest: ReleaseManifest) -> dict[str, Any]:
    return {
        "snippet": {
            "title": manifest.title,
            "description": manifest.description,
            "tags": list(manifest.tags),
            "categoryId": manifest.category_id,
        },
        "status": {
            "privacyStatus": PRIVACY_STATUS,
            "selfDeclaredMadeForKids": manifest.made_for_kids,
            "containsSyntheticMedia": manifest.contains_synthetic_media,
        },
    }


def build_insert_request(
    service: Any,
    manifest: ReleaseManifest,
    video: VideoInfo,
    *,
    media_upload_factory: Callable[..., Any] | None = None,
) -> Any:
    upload_factory = media_upload_factory
    if upload_factory is None:
        try:
            from googleapiclient.http import MediaFileUpload
        except ImportError as exc:
            raise UploaderError(
                "Google API dependencies are missing; install tools/youtube/requirements.txt."
            ) from exc
        upload_factory = MediaFileUpload
    media = upload_factory(
        str(video.path),
        mimetype="video/mp4",
        chunksize=CHUNK_SIZE_BYTES,
        resumable=True,
    )
    try:
        return service.videos().insert(
            part="snippet,status",
            body=build_video_insert_body(manifest),
            media_body=media,
            notifySubscribers=NOTIFY_SUBSCRIBERS,
        )
    except google_api_exception_types() as exc:
        status = _http_status(exc)
        suffix = f" (HTTP {status})" if status is not None else ""
        raise UploaderError(f"Unable to start a YouTube resumable upload{suffix}.") from exc


def _http_status(error: BaseException) -> int | None:
    response = getattr(error, "resp", None)
    status = getattr(response, "status", None)
    return status if isinstance(status, int) else None


def upload_resumable(
    request: Any,
    *,
    report: Callable[[str], None] | None = None,
    sleeper: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    emit = report or (lambda message: print(message, file=sys.stderr))
    response: dict[str, Any] | None = None
    retries = 0
    emit("Starting resumable upload session.")

    while response is None:
        try:
            status, response = request.next_chunk(num_retries=0)
            retries = 0
            if status is not None:
                uploaded = int(status.resumable_progress)
                total_value = status.total_size
                if total_value is None:
                    emit(f"Uploaded {uploaded} bytes.")
                else:
                    total = int(total_value)
                    percent = (uploaded / total * 100) if total else 0.0
                    emit(f"Uploaded {uploaded} of {total} bytes ({percent:.1f}%).")
        except retry_exception_types() as exc:
            status_code = _http_status(exc)
            transient = status_code is not None and status_code >= 500
            if status_code is None:
                transient = isinstance(exc, transient_network_exception_types())
            if not transient or retries >= MAX_CHUNK_RETRIES:
                suffix = f" (HTTP {status_code})" if status_code is not None else ""
                raise UploaderError(f"Resumable upload failed{suffix}; no new upload session was started.") from exc
            retries += 1
            delay = min(BASE_RETRY_DELAY_SECONDS * (2 ** (retries - 1)), MAX_RETRY_DELAY_SECONDS)
            emit(
                f"Transient upload failure; retrying the current resumable chunk "
                f"({retries}/{MAX_CHUNK_RETRIES}) after {delay:g}s."
            )
            sleeper(delay)

    return response


def make_receipt(
    manifest: ReleaseManifest,
    video: VideoInfo,
    channel: ChannelInfo,
    *,
    video_id: str | None,
    upload_performed: bool,
    privacy_status: str | None = PRIVACY_STATUS,
) -> dict[str, Any]:
    return {
        "schema_version": SUPPORTED_SCHEMA_VERSION,
        "record_type": "youtube_private_upload_receipt",
        "release_id": manifest.release_id,
        "channel": {
            "id": channel.channel_id,
            "title": channel.title,
        },
        "expected_channel_id": manifest.expected_channel_id,
        "video": {
            "id": video_id,
            "privacy_status": privacy_status,
            "url": f"{YOUTUBE_VIDEO_URL}{video_id}" if video_id else None,
        },
        "source": {
            "path": str(video.path),
            "size_bytes": video.size_bytes,
            "sha256": video.sha256,
        },
        "notify_subscribers": NOTIFY_SUBSCRIBERS,
        "upload_performed": upload_performed,
    }


def serialize_receipt(receipt: dict[str, Any]) -> str:
    return json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"


def write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    destination = path.expanduser().absolute()
    if destination.exists():
        raise UploaderError(f"Receipt path already exists; refusing to overwrite: {destination}.")
    if not destination.parent.is_dir():
        raise UploaderError(f"Receipt parent directory does not exist: {destination.parent}.")

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            os.fchmod(temporary.fileno(), 0o600)
            temporary.write(serialize_receipt(receipt))
            temporary.flush()
            os.fsync(temporary.fileno())
        os.link(temporary_path, destination)
    except FileExistsError as exc:
        raise UploaderError(f"Receipt path already exists; refusing to overwrite: {destination}.") from exc
    except OSError as exc:
        raise UploaderError(f"Unable to publish receipt atomically: {destination}.") from exc
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError as exc:
                raise UploaderError(
                    f"Unable to remove temporary receipt file: {temporary_path}."
                ) from exc


def _ensure_receipt_path_available(path: Path | None) -> None:
    if path is None:
        return
    destination = path.expanduser().absolute()
    if destination.exists():
        raise UploaderError(f"Receipt path already exists; refusing to overwrite: {destination}.")
    if not destination.parent.is_dir():
        raise UploaderError(f"Receipt parent directory does not exist: {destination.parent}.")


def _validate_local_inputs(
    manifest_path: Path,
    video_path: Path,
    token_path: Path,
    expected_channel_path: Path,
    receipt_path: Path | None,
) -> tuple[ReleaseManifest, VideoInfo, str]:
    expected_channel_id = read_expected_channel_id(expected_channel_path.expanduser())
    manifest = validate_manifest(manifest_path.expanduser(), expected_channel_id)
    video = validate_video(video_path.expanduser())
    validate_credential_file(DEFAULT_CLIENT_SECRET_FILE, "OAuth client-secret")
    validate_credential_file(token_path.expanduser(), "OAuth token")
    _ensure_receipt_path_available(receipt_path)
    return manifest, video, expected_channel_id


def run_upload(args: argparse.Namespace) -> tuple[dict[str, Any], Path | None]:
    started = time.monotonic()
    print("Validating private YouTube upload request.", file=sys.stderr)
    print("Validating manifest, video, and local credential files.", file=sys.stderr)
    manifest, video, expected_channel_id = _validate_local_inputs(
        args.manifest,
        args.video,
        args.token_file,
        args.expected_channel_id_file,
        args.receipt_output,
    )
    print(f"Validated release manifest: {manifest.release_id}.", file=sys.stderr)
    print(
        f"Validated MP4: {video.path} ({video.size_bytes} bytes, SHA-256 {video.sha256}).",
        file=sys.stderr,
    )

    credentials = load_credentials(args.token_file.expanduser())
    service = build_youtube_service(credentials)
    print("Validating authenticated channel identity with YouTube.", file=sys.stderr)
    channel = validate_authenticated_channel(service, expected_channel_id)
    print(
        f"Authenticated channel: {channel.title!r} ({channel.channel_id}); "
        f"privacy={PRIVACY_STATUS}, notifySubscribers={str(NOTIFY_SUBSCRIBERS).lower()}.",
        file=sys.stderr,
    )

    if args.dry_run:
        receipt = make_receipt(
            manifest,
            video,
            channel,
            video_id=None,
            upload_performed=False,
        )
        print("Dry run complete; upload_performed=false.", file=sys.stderr)
    else:
        request = build_insert_request(service, manifest, video)
        response = upload_resumable(request)
        returned_video_id = response.get("id") if isinstance(response, dict) else None
        status = response.get("status") if isinstance(response, dict) else None
        returned_privacy = status.get("privacyStatus") if isinstance(status, dict) else None
        if not isinstance(returned_video_id, str) or not returned_video_id:
            raise UploaderError(
                "YouTube upload response did not contain a video ID; inspect the resumable session manually."
            )
        receipt = make_receipt(
            manifest,
            video,
            channel,
            video_id=returned_video_id,
            upload_performed=True,
            privacy_status=returned_privacy if isinstance(returned_privacy, str) else None,
        )
        if returned_privacy != PRIVACY_STATUS:
            raise UploadResponseError(
                "YouTube upload response did not confirm private status; inspect the video manually.",
                receipt,
            )
        print(f"YouTube returned video ID {returned_video_id}.", file=sys.stderr)
        print(f"Final privacy status: {PRIVACY_STATUS}.", file=sys.stderr)
    elapsed = time.monotonic() - started
    print(f"Elapsed time: {elapsed:.2f}s.", file=sys.stderr)
    return receipt, args.receipt_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and upload one video to YouTube with privacy fixed to private."
    )
    parser.add_argument("--manifest", type=Path, required=True, help="Versioned release manifest JSON.")
    parser.add_argument("--video", type=Path, required=True, help="Source MP4 file.")
    parser.add_argument(
        "--token-file",
        type=Path,
        default=DEFAULT_TOKEN_FILE,
        help="Local authorized-user token file.",
    )
    parser.add_argument(
        "--expected-channel-id-file",
        type=Path,
        default=DEFAULT_EXPECTED_CHANNEL_ID_FILE,
        help="Local file containing the immutable expected channel ID.",
    )
    parser.add_argument(
        "--receipt-output",
        type=Path,
        help="Optional path for an atomically published upload receipt.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and authenticated channel without calling videos.insert.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        receipt, receipt_path = run_upload(args)
        serialized = serialize_receipt(receipt)
        sys.stdout.write(serialized)
        if receipt_path is not None:
            write_receipt(receipt_path, receipt)
            print(f"Receipt written to {receipt_path.expanduser().absolute()}.", file=sys.stderr)
        return 0
    except UploadResponseError as exc:
        sys.stdout.write(serialize_receipt(exc.receipt))
        if args.receipt_output is not None:
            try:
                write_receipt(args.receipt_output, exc.receipt)
            except UploaderError as receipt_error:
                print(f"ERROR: {receipt_error}", file=sys.stderr)
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except UploaderError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
