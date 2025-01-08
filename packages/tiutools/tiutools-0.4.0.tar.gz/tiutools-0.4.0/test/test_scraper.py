from pathlib import Path


def test_getimage_twice(canvas_scraper):
    """ ok """
    ids = [12539, 12448]
    img_dir = Path("screenshots")
    for i in ids:
        path_img = img_dir / Path(f"{i}.png")
        path_img.unlink(missing_ok=True)
        canvas_scraper.get_gradebook_image(i)
        assert path_img.exists()
