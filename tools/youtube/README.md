# Private YouTube uploader

## Purpose and boundary

`upload_private_video.py` uploads one release-manifest MP4 as **private** to the locally authorized YouTube channel. Privacy is fixed in the request body; subscriber notifications are always disabled. The tool does not support public or unlisted uploads, scheduling, deletion, or changes to existing videos. Scheduling is not implemented yet.

The uploader is an explicit release operation, not part of the Psalm planner or content-generation path. It does not modify the input manifest or source video, and it does not select a channel by title.

## OAuth prerequisites and local files

Complete the OAuth bootstrap separately and authorize both `youtube.readonly` and `youtube.upload`. The default files are:

```text
~/.config/psalm-music-automation/client_secret.json
~/.config/psalm-music-automation/token.json
~/.config/psalm-music-automation/expected_channel_id
```

The client-secret and token files must be regular, readable files with owner-only permissions on POSIX systems (for example, mode `0600`). The expected-channel file contains only the immutable channel ID. The uploader checks these paths and permissions but never prints or copies credential values. Do not pass credentials as command-line arguments.

The default token and expected-channel paths may be overridden with `--token-file` and `--expected-channel-id-file` for controlled testing. The client-secret path is fixed and is not a CLI option.

Install the pinned dependencies into the Python environment used to run the uploader:

```sh
python3 -m pip install -r tools/youtube/requirements.txt
```

## Release manifest

The manifest is versioned JSON. `youtube.video_id` must be `null`; a manifest containing a video ID is refused to prevent duplicate uploads.

```json
{
  "schema_version": "1.0.0",
  "release_id": "psalm-2026-12-01-pop-punk-v1",
  "title": "Example title",
  "description": "An original song inspired by Psalm 72.",
  "tags": ["psalm", "pop punk", "original music"],
  "category_id": "10",
  "made_for_kids": false,
  "contains_synthetic_media": true,
  "youtube": {
    "expected_channel_id": "UCGtP5aRMQm5jc_XrDZOyX0Q",
    "video_id": null
  }
}
```

The schema version, filesystem-safe release ID, title, description, tags, numeric-string category, Boolean values, and channel ID are validated. Invalid data is rejected rather than silently corrected.

## Validation and upload

The video must be a readable, regular, nonempty `.mp4` file whose filename resolves to `video/mp4`. The uploader records its byte size and SHA-256 digest. This is filename/MIME validation, not codec-level media validation; no `ffprobe` check is performed.

Run a dry run before an upload:

```sh
python3 tools/youtube/upload_private_video.py \
  --manifest release.json \
  --video final.mp4 \
  --dry-run
```

Dry run validates the manifest, MP4, credential-file presence and permissions, expected channel file, and authenticated channel identity. It makes the read-only `channels.list(mine=true)` request but never calls `videos.insert`. Its JSON receipt has null video ID and URL and `upload_performed: false`.

The immutable channel ID returned by YouTube must exactly match the ID in the local expected-channel file and manifest. Exactly one authenticated channel must be returned. Channel title is reported for operator confirmation but is never used for selection.

Perform an upload only after reviewing the dry-run output:

```sh
python3 tools/youtube/upload_private_video.py \
  --manifest release.json \
  --video final.mp4
```

The tool calls `videos.insert(part="snippet,status", notifySubscribers=false)` with privacy fixed to `private`, and maps the manifest metadata to the API request. It uses a resumable `video/mp4` upload with 8 MiB chunks. Transient network errors and HTTP 5xx responses retry only the current resumable chunk, at most three times with bounded backoff. Deterministic 4xx responses are not retried. The tool never starts a fresh upload session automatically after an ambiguous terminal failure.

The uploader refuses an existing receipt path and a manifest with a preexisting video ID. It does not infer success from a timeout, update the input manifest, or automatically retry a complete upload after an ambiguous outcome. Inspect the returned video in YouTube before any operator-managed retry.

## Receipt

Successful uploads print deterministic JSON to stdout. `--receipt-output PATH` optionally publishes the same receipt to a new file using a flushed/fsynced sibling temporary file and an atomic no-overwrite publication. Existing files are not replaced. The receipt contains release, channel, video ID/URL, source path, size, SHA-256, privacy status, notification setting, and whether an upload occurred. It contains no OAuth credentials or tokens.

```sh
python3 tools/youtube/upload_private_video.py \
  --manifest release.json \
  --video final.mp4 \
  --receipt-output receipts/psalm-2026-12-01.json
```

Diagnostics and progress are written to stderr; JSON receipts are written to stdout. Credentials, authorization headers, and OAuth JSON values are not included in output or error text.

## Testing

Tests use synthetic manifests and local MP4-shaped byte fixtures. All YouTube API operations are mocked; the suite performs no live upload.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s tools/youtube/tests \
  -v

PYTHONPYCACHEPREFIX=/tmp/suno-youtube-pycache python3 -m py_compile \
  tools/youtube/upload_private_video.py
```

## Limitations and security notes

- The dry run makes a real read-only YouTube API channel-identity request and therefore requires a valid local OAuth token and network access.
- The uploader does not perform codec validation, scheduling, public/unlisted publishing, playlist operations, thumbnail uploads, comments, branding, deletion, or metadata updates to existing videos.
- A successful resumable upload may still require manual inspection if the local process loses its connection after YouTube has accepted the final chunk. Do not blindly retry an ambiguous upload.
- A local receipt is a record of the API response, not proof of public availability; uploads remain private.
- Keep OAuth files outside the repository. Never stage or commit secrets, tokens, cookies, or live credentials.
