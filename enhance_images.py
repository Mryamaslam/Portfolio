"""Upscale and sharpen small portfolio screenshots for sharper display."""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent
FOLDERS = [
    "email_portfolio",
    "linkdin_portfolio",
    "upwork_portfolio",
    "meta google ads",
    "upwork reviews",
]
MIN_WIDTH = 1400
EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def enhance(path: Path) -> bool:
    try:
        im = Image.open(path)
    except Exception as exc:
        print(f"SKIP {path.name}: {exc}")
        return False

    w, h = im.size
    changed = False

    if w < MIN_WIDTH:
        scale = MIN_WIDTH / w
        new_size = (MIN_WIDTH, max(1, int(h * scale)))
        im = im.resize(new_size, Image.Resampling.LANCZOS)
        changed = True

    if im.mode == "P":
        im = im.convert("RGBA")
    if im.mode in ("RGBA", "LA"):
        rgb = im.convert("RGB")
        rgb = ImageEnhance.Contrast(rgb).enhance(1.06)
        rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=3))
        alpha = im.split()[-1]
        im = Image.merge("RGBA", (*rgb.split(), alpha))
    else:
        if im.mode != "RGB":
            im = im.convert("RGB")
        im = ImageEnhance.Contrast(im).enhance(1.06)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130, threshold=3))

    if path.suffix.lower() == ".webp":
        im.save(path, quality=92, method=6)
    elif path.suffix.lower() in {".jpg", ".jpeg"}:
        im.save(path, quality=92, optimize=True)
    else:
        im.save(path, optimize=True)

    print(f"{'ENHANCED' if changed else 'SHARPENED'} {path.name}: {w}x{h} -> {im.size[0]}x{im.size[1]}")
    return True


def main():
    count = 0
    for folder in FOLDERS:
        folder_path = ROOT / folder
        if not folder_path.exists():
            continue
        for file in sorted(folder_path.iterdir()):
            if file.suffix.lower() in EXTS and file.is_file():
                if enhance(file):
                    count += 1
    print(f"Done. Processed {count} images.")


if __name__ == "__main__":
    main()
