"""The generated images of the theme, designed with the image model Z-Image-Turbo (Tongyi-MAI, Apache-2.0):
the launcher strip and the emblem of the top bar.

    python tools/images.py gen [part ...]     six drafts of each part, wip/strip/<part>_<seed>.png; a draft that exists is kept
    python tools/images.py sheet              all drafts of every part on one sheet per part, wip/strip/sheet_<part>.png
    python tools/images.py compose            the drafts named in CHOICES -> style/images/strip-centre.jpg, strip-plate.jpg,
                                             strip-cap.jpg and emblem.png

gen needs a Python with torch and diffusers and one GPU, chosen by its nvidia-smi index. On the workstation:

    CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 HF_HUB_OFFLINE=1 \\
        ~/workspace/funcraft/w40k-mechanicum/.venv-moge/bin/python tools/images.py gen

The model misspells words: read every letter of a draft with text before it goes into CHOICES.
"""
import pathlib
import sys

from PIL import Image, ImageChops, ImageDraw, ImageEnhance

ROOT = pathlib.Path(__file__).parent.parent
WIP = ROOT / "wip" / "strip"
OUT = ROOT / "style" / "images"
SEEDS = (1, 2, 3, 4, 5, 6)
HEIGHT = 68                                # height of the strip on the page in CSS pixels; the files hold twice that

STEEL = ("Warhammer 40,000 Adeptus Mechanicus forge machinery, grimdark: brushed gunmetal steel and blackened iron "
         "with polished gold inlay, the raised edges worn bright, fine scratches and oil stains, black grime in the "
         "recesses, cold grey metal, no rust, no brown, no cloth. Flat frontal orthographic view, evenly lit, no "
         "shadows, no background: the object fills the whole frame edge to edge")
COG = ("the Cog Mechanicum, the symbol of the Adeptus Mechanicus, in high relief: a large cog wheel with square teeth, "
       "divided vertically down the middle, its left half black iron and its right half bright polished steel; inside "
       "the cog one skull seen from the front, also divided vertically down the middle: the left half of the skull is "
       "a human skull of pale bone with an empty eye socket, the right half is a machine skull of dark steel plates "
       "with one round glowing red lens as its eye and thin cables running from its cheek; a thin gold rim around the cog")
JOBS = {
    # part: (width, height, prompt)
    "centre": (2048, 320,
        "A very long narrow riveted gunmetal steel frieze. In its centre " + COG + ". To the left of the cog the word "
        "in large raised gold roman capitals, spelled exactly: 'ADEPTUS'; to the right of the cog the word in large "
        "raised gold roman capitals, spelled exactly: 'MECHANICUS'. " + STEEL),
    "emblem": (1024, 1024,
        "One heavy metal badge seen from the front, centred, isolated on a pure black background: " + COG + ". Bold "
        "simple shapes that stay readable at a very small size. Warhammer 40,000 Adeptus Mechanicus, grimdark: dark "
        "gunmetal steel, pale bone, polished gold, worn edges, fine scratches. Flat frontal orthographic view, evenly "
        "lit, no shadows, nothing else in the frame"),
    "plate": (1024, 320,
        "A long narrow panel of riveted gunmetal steel plates: panel seams, rows of rivets, small engraved cog wheels, "
        "thin cables and lines of tiny engraved binary digits. No words, no skull. " + STEEL),
    "cap": (512, 512,
        "A square steel plate painted with wide diagonal black and golden yellow hazard warning stripes, the paint "
        "chipped and scratched, in a riveted steel frame. " + STEEL),
}
# part: seed of the draft that goes into the theme. Centre drafts 1 and 3 misspell MECHANICUS
CHOICES = {"centre": 5, "plate": 5, "cap": 5, "emblem": 5}
EMBLEM = 26                                # largest size of the emblem in the top bar in CSS pixels; the file holds four times that
DIM = 0.82                                 # the steel is darkened: the strip must not be the brightest thing on the page
# pixels cut from the left and right, and from the top and bottom, of a draft: the model leaves a light ground at the edges
TRIM = {"centre": (0, 6), "plate": (0, 18), "cap": (30, 30), "emblem": (0, 0)}


def generate(parts):
    import torch
    from diffusers import ZImagePipeline
    WIP.mkdir(parents=True, exist_ok=True)
    pipe = None
    for part in parts:
        width, height, prompt = JOBS[part]
        for seed in SEEDS:
            draft = WIP / f"{part}_{seed}.png"
            if draft.exists():
                continue
            if pipe is None:
                pipe = ZImagePipeline.from_pretrained("Tongyi-MAI/Z-Image-Turbo", torch_dtype=torch.bfloat16).to("cuda")
            image = pipe(prompt=prompt, width=width, height=height, num_inference_steps=9, guidance_scale=0.0,
                         generator=torch.Generator("cuda").manual_seed(seed)).images[0]
            image.save(draft)
            print("wrote", draft.name, flush=True)


def sheet():
    """All drafts of a part below each other, each with its seed, to choose from."""
    for part in JOBS:
        drafts = [(seed, WIP / f"{part}_{seed}.png") for seed in SEEDS if (WIP / f"{part}_{seed}.png").exists()]
        if not drafts:
            continue
        images = [(seed, Image.open(path).convert("RGB")) for seed, path in drafts]
        width = 1000
        scaled = [(seed, im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)) for seed, im in images]
        out = Image.new("RGB", (width, sum(im.height + 6 for _, im in scaled)), "black")
        y = 0
        for seed, im in scaled:
            out.paste(im, (0, y))
            ImageDraw.Draw(out).text((6, y + 4), str(seed), fill=(255, 60, 60))
            y += im.height + 6
        out.save(WIP / f"sheet_{part}.png")
        print("wrote", f"sheet_{part}.png", out.size)


def chosen(part):
    image = Image.open(WIP / f"{part}_{CHOICES[part]}.png").convert("RGB")
    x, y = TRIM[part]
    image = image.crop((x, y, image.width - x, image.height - y))
    return ImageEnhance.Brightness(image).enhance(DIM)


def compose():
    """The chosen drafts at twice the height of the strip, as JPEG files of the theme."""
    height = 2 * HEIGHT

    def fit(image):
        return image.resize((round(image.width * height / image.height), height), Image.LANCZOS)

    centre = fit(chosen("centre"))
    # the plate beside its mirror image: the tile then repeats without a visible seam
    plate = fit(chosen("plate"))
    tile = Image.new("RGB", (2 * plate.width, height))
    tile.paste(plate, (0, 0))
    tile.paste(plate.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (plate.width, 0))
    # the hazard stripes: their yellow is turned towards the gold of the theme
    cap = fit(chosen("cap"))
    cap = ImageEnhance.Color(cap).enhance(0.72)
    for name, image in (("strip-centre.jpg", centre), ("strip-plate.jpg", tile), ("strip-cap.jpg", cap)):
        image.save(OUT / name, quality=84, optimize=True)
        print(name, image.size, (OUT / name).stat().st_size // 1024, "kB")
    emblem()


def emblem():
    """The emblem draft without its black ground, as a square PNG with transparency."""
    image = Image.open(WIP / f"emblem_{CHOICES['emblem']}.png").convert("RGB")
    # the ground is the black that is connected to the border; the black inside the gear stays
    work = image.copy()
    marker = (255, 0, 255)
    for seed in ((0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1)):
        ImageDraw.floodfill(work, seed, marker, thresh=48)
    alpha = ImageChops.difference(work, Image.new("RGB", image.size, marker)).convert("L").point(lambda v: 255 if v else 0)
    cut = image.copy()
    cut.putalpha(alpha)
    cut = cut.crop(alpha.getbbox())
    side = max(cut.size)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(cut, ((side - cut.width) // 2, (side - cut.height) // 2))
    square = square.resize((4 * EMBLEM, 4 * EMBLEM), Image.LANCZOS)
    square.save(OUT / "emblem.png", optimize=True)
    print("emblem.png", square.size, (OUT / "emblem.png").stat().st_size // 1024, "kB")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "gen":
        generate(sys.argv[2:] or list(JOBS))
    elif command == "sheet":
        sheet()
    elif command == "compose":
        compose()
    else:
        sys.exit(__doc__)
