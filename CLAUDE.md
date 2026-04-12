# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`hatched` is a Python library and [vpype](https://github.com/abey79/vpype) plug-in that converts images to plotter-friendly hatched patterns. It uses OpenCV for image loading/processing, scikit-image for contour detection, Shapely for geometry operations, and svgwrite for SVG output.

## Setup

```bash
uv venv .venv
uv pip install -e .
uv pip install pytest black isort
source .venv/bin/activate
```

## Commands

**Lint / format:**
```bash
black hatched/        # format with line length 95
isort hatched/        # sort imports (black-compatible profile)
```

**Run tests:**
```bash
pytest
```

**Run a single test:**
```bash
pytest path/to/test_file.py::test_function_name
```

**Run the example:**
```bash
cd examples && python skull.py
```

## Architecture

All core logic lives in `hatched/hatched.py`. The public API is a single function `hatch()` exported via `hatched/__init__.py`.

**Processing pipeline in `hatch()`:**
1. `_load_image()` — reads image with OpenCV, resizes, blurs, optionally mirrors/inverts
2. `_build_hatch()` — detects contours at each threshold level using `skimage.measure.find_contours`, builds Shapely polygon masks from those contours, generates hatch lines (diagonal or circular), then intersects lines with the appropriate mask regions
3. `_save_to_svg()` — writes the resulting `MultiLineString` to SVG via svgwrite
4. Optional matplotlib display of contours and final pattern

**Multi-level shading:** The `levels` parameter defines N threshold values, producing N zones of increasing hatch density. Lines are interleaved: the densest zone uses `2^(N-1) * pitch` spacing, coarser zones use larger multiples so their lines fit between the denser ones.

**vpype integration:** `hatched/vpype_plugin.py` wraps `hatch()` as a vpype `@generator` command registered via the `vpype.plugins` entry point in `setup.py`. The plugin always sets `save_svg=False` and `h_mirror=False` (both handled by vpype instead).
