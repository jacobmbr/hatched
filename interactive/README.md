# hatched interactive tuner

Interactive parameter tuning for `hatched` using [vsketch](https://github.com/abey79/vsketch).

## Setup

```bash
uv venv
uv pip install vsketch
uv pip install -e ..
```

## Usage

```bash
uv run vsk run sketch_hatched.py
```

This opens a GUI with sliders for all `hatched` parameters. Set `image_path` to the path of your input image, then tune:

| Parameter | Description |
|-----------|-------------|
| `image_path` | Path to input image |
| `scale` | Resize factor before processing (0.1–5.0) |
| `blur` | Blur radius applied before thresholding (0 to disable) |
| `level1/2/3` | Threshold values separating dark/mid/light zones (0–255) |
| `pitch` | Hatch line spacing for the densest zone (px) |
| `angle` | Hatch angle in degrees (0–180) |
| `circular` | Use circular instead of diagonal hatches |
| `invert` | Invert the image before processing |

The sketch re-renders on every parameter change. Use `vsk save` to export the result as SVG.
