import colorsys

from PIL import Image
from sklearn.cluster import KMeans


def get_dominant_colours(path, *, count):
    """
    Return a list of the dominant RGB colours in the image at ``path``.

    :param path: Path to the image file.
    :param count: Number of dominant colours to find.

    """
    im = Image.open(path)

    # Resizing means less pixels to handle, so the *k*-means clustering converges
    # faster.  Small details are lost, but the main details will be preserved.
    im = im.resize((100, 100))

    # Ensure the image is RGB, and use RGB values in [0, 1] for consistency
    # with operations elsewhere.
    im = im.convert("RGB")
    colors = [(r / 255, g / 255, b / 255) for (r, g, b) in im.getdata()]

    return KMeans(n_clusters=count).fit(colors).cluster_centers_


if __name__ == "__main__":
    import sys

    try:
        path = sys.argv[1]
    except ImportError:
        sys.exit(f"Usage: {__file__} <PATH>")

    dominant_colors = get_dominant_colours(path, count=9)
    print(dominant_colors)
    for color in dominant_colors:
        print("#%02x%02x%02x" % tuple(int(v * 255) for v in color))
