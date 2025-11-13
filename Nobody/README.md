# Nobody Package (MVP Refactor)

This directory contains the refactored MVP (Model-View-Presenter) version of the original `Nobody3.py` application.

## Directory Layout

```
Nobody/
|-- __init__.py              # Package bootstrap
|-- main.py                  # Application entry point
|-- config/                  # Configuration helpers
|   |-- __init__.py
|   `-- constants.py         # Theme and other constants
|-- utils/                   # Shared utilities
|   |-- __init__.py
|   |-- cache.py             # Cache-directory helpers
|   |-- logging.py           # Logging bootstrap
|   `-- ffmpeg.py            # FFmpeg discovery/download
|-- models/                  # Domain models
|   |-- __init__.py
|   `-- settings.py          # AppSettings definition
|-- services/                # Background workers (threads)
|   |-- __init__.py
|   |-- ffmpeg_checker.py    # Silent FFmpeg download thread
|   |-- searcher.py          # Metadata fetcher
|   `-- downloader.py        # Download worker
`-- views/                   # UI components
    |-- __init__.py
    |-- main_window.py       # Main window implementation
    |-- format_settings_dialog.py
    |-- settings_dialog.py
    |-- components.py
    |-- mini_player.py
    |-- layout_builder.py
    `-- video_table.py
```

## Running the Refactored App

```bash
# from the project root (recommended)
python -m Nobody.main

# or from inside the package
cd Nobody
python main.py
```

> **Important:** Run from the project root if you rely on automatic FFmpeg download, because the helper expects to place binaries beside the executable.

## Refactor Progress

### Completed
1. Utilities extracted (logging, cache resolution, FFmpeg helpers)
2. Application settings split into dedicated model
3. Service layer created (search, download, ffmpeg-check threads)
4. Config constants isolated
5. View layer decomposed into dialogs, components, layout builder, and presenter

### Next Ideas
- Split additional responsibilities out of `VideoDownloader` if desired
- Consider dependency-injection to simplify testing
- Continue growing unit-test coverage for presenters and services

## Relation to `Nobody3.py`

- `legacy/Nobody3.py` keeps the original monolithic implementation for reference
- `Nobody/` hosts the refactored MVP structure; both can be launched independently

## References

- MVP architecture pattern notes
- Emphasis on modularity for easier maintenance and testing

