# Asset Generation: images, video, SVG, and image sequences

> Loaded when the task involves generating visuals — single images, videos, SVG, or
> image-sequence motion. Read this *instead* of the component/layout tables in
> `design-methodology.md` when the request is purely asset-shaped.

---

## 0. Decide the medium first

Pick the cheapest medium that satisfies the look. Do NOT default to hand-authored SVG
path animation for rich motion — AI gets the path math wrong.

| Need | Default medium | Why |
|---|---|---|
| Rich / photographic / 3D-rendered motion (spotlight sweep, fluid, geological scroll-through, product reveal) | **Image sequence** or video or Canvas-frame scrub | Real texture; AI generates frames reliably. |
| Scalable icons, logos, line-art UI, small interactive graphics | **SVG** (static, or driven by CSS `transform`) | Vector-crisp, KB-sized, no pixel cost. SVG is correct here — do not exile it. |
| Single hero / key-section image | **Generated raster image** (AVIF > WebP > JPEG) | Real photography beats styled-`<div>` fakes. |
| Simple pan / scale / rotate / fade of existing asset | **CSS `transform` / `opacity`** | Zero new asset cost. |

---

## 1. Single-image / video prompt structure

Build the prompt FROM the design context (Step 1 of SKILL.md), never invent it separately:

1. **Subject** — what is in frame.
2. **Style / medium** — photoreal, 3D render, illustration, film still, motion graphics.
3. **Lighting & atmosphere** — soft, dramatic, neon, natural, studio.
4. **Composition** — close-up, wide, Dutch angle, rule of thirds, centered.
5. **Color palette** — derived from the visual tokens (accent + neutrals).
6. **Motion description** (video only) — camera move, pacing, transitions, loop behavior.
7. **Negative prompts** — what to exclude: generic stock look, clutter, wrong mood, off-palette colors.
8. **Technical specs** — aspect ratio, resolution, duration, frame rate.

Always generate the image/video prompt **after** the design context exists, not before.

---

## 2. Image-sequence motion (the AI-friendly alternative to SVG animation)

Compose N still frames into motion via `<img>` frame-swap, Canvas `drawImage`, or
scroll-scrubbed `ImageBitmap`. This is the recommended path for rich/photographic/3D motion.

### 2.1 Frame budget & format

- ≤ 30 frames for a loop; 40–120 frames for scroll-scrub, scaled to desired smoothness.
- Format: AVIF > WebP > JPEG.
- Merge frames into a single sprite-sheet where possible to cut request count.
- Preload critical frames first; lazy-load the rest. Never block first paint on the full sequence.

### 2.2 Consistency across frames (the hard part)

This is what makes a sequence read as *motion* rather than *jitter*.

- **Lock the generation seed** across the whole sequence.
- **Vary exactly ONE parameter per frame**: angle, position, light direction, or time.
- **Fix everything else**: composition, framing, exposure, subject identity, style, palette.
- Drift between frames reads as jitter, not motion.

### 2.3 Sequence prompt (build as a set, not N unrelated prompts)

1. **Fixed across all frames** (lock these or the frames will drift): subject identity, composition/framing, lighting, color palette, style/medium, seed.
2. **Varies per frame** — exactly ONE parameter (angle / position / light / time). Changing more than one per frame produces jitter.
3. **Negative prompts** — exclude style-drift terms (e.g. "different lighting, recomposed, new subject") so the model doesn't reinvent the scene each frame.
4. **Frame plan** — number of frames, the delta between frame 0 and frame N, and whether it loops (loop end ≈ start) or scrubs with scroll (arbitrary start/end).
5. **Fallback frame** — designate one frame (usually the end) as the static reduced-motion / load-failure still.
6. **Technical specs** — aspect ratio, resolution, format (AVIF > WebP > JPEG), sprite-sheet vs separate files.

### 2.4 Fallback & accessibility (non-negotiable)

- If the sequence fails to load OR `prefers-reduced-motion` is set → show a single end-frame still. Never a broken/half-playing sequence.
- Pure visual motion carries no information for screen readers. Anything the user must know must also exist as text. Do not encode meaning only in the animation.
- Sequence playback is heavy — prefer pre-extracted frames (Canvas / `ImageBitmap`) over driving many `<video>` elements; the latter is expensive on the main thread.

---

## 3. SVG (when it IS the right medium)

SVG is correct for: scalable icons, logos, line-art UI, small interactive graphics, and
any graphic that must stay crisp at any size or stay under KB-level weight.

Rules when SVG is chosen:

- Can it be layered / animated? Decide up front. Prefer driving it with CSS `transform` /
  `opacity` over hand-authored path / `stroke-dashoffset` animation.
- Line weights, color treatment must come from the visual tokens (Step 1 accent + neutrals).
- If animation is needed and it's more than a simple transform, reconsider the image-sequence
  path in Section 2 — it is usually more reliable than hand-authoring SVG path animation.

---

## 4. Photography & illustration style (for raster assets)

- Photography style: candid, studio, monochrome, cinematic, etc. — state it explicitly, do not leave it to the model's default.
- Illustration style: flat, 3D, line-art, abstract, collage — same.
- Never build fake product UIs from styled `<div>` rectangles. Generate a real screenshot-like
  image, or use a clearly labeled placeholder.
- No generic placeholder copy in any asset ("Acme Co", "Jane Doe", "Lorem ipsum").