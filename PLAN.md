# Performance Optimization Plan

## Baseline

Profiled on `examples/skull.png` with `hatch_pitch=5, levels=(20, 100, 180), blur_radius=1`.

**Total: 24 seconds**

| Function | Time | % |
|---|---|---|
| `_build_mask` | 23.4s | 97% |
| → `union` (1,112 calls) | 12.4s | 51% |
| → `difference` (898 calls) | 10.5s | 44% |
| `difference`+`intersection` in `_build_hatch` | 0.35s | 1.5% |
| `find_contours` (skimage) | 0.16s | 0.7% |
| Everything else | 0.15s | 0.6% |

## Root Cause

`_build_mask` builds a Shapely polygon by sequentially unioning/differencing one contour ring
at a time. With 2,010 contour rings in skull.png, this is 2,010 GEOS operations where each
call operates on an increasingly complex accumulated polygon.

```python
# Current — O(N²) effective complexity
for r in lr:
    mask = mask.union(Polygon(r).buffer(0.5))      # 1,112 times
    # or
    mask = mask.difference(Polygon(r).buffer(-0.5)) # 898 times
```

## Fix (surgical, no behavioral change)

Separate CCW rings (outer filled areas) from CW rings (holes), then:

1. Bulk-union all fills with `shapely.unary_union()` — 1 GEOS call instead of 1,112
2. Bulk-union all holes with `shapely.unary_union()`, then subtract in one `.difference()` — 1 GEOS call instead of 898

```python
# Target — O(1) GEOS calls
fills = [Polygon(r).buffer(0.5) for r in lr if r.is_ccw]
holes = [Polygon(r).buffer(-0.5) for r in lr if not r.is_ccw]
mask = shapely.unary_union(fills)
if holes:
    mask = mask.difference(shapely.unary_union(holes))
```

## Results

**18× speedup: 24.1s → 1.3s** (profiled on skull.png, same parameters)

| | Before | After |
|---|---|---|
| Total | 24.1s | 1.3s |
| `_build_mask` | 23.4s | 0.71s |
| `union` calls | 1,112 | 6 |
| `difference` calls | 898 | 6 |

## Steps

- [x] Implement fix in `_build_mask`
- [x] Re-profile to confirm improvement
- [ ] Update CLAUDE.md
