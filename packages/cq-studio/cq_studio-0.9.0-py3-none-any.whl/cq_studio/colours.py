import functools
import itertools
import operator
import math

import cadquery as cq

from cq_studio.defaults import defaults


class ColourGenerator:
    def __init__(self, colour_quantization: int = defaults["colour_quantization"]):
        self.colour_quantization = colour_quantization
        # possible values for any one component of colour
        self.values = [i / colour_quantization for i in range(colour_quantization + 1)]
        # then combinations for each of the 3 components
        combinations = itertools.product(self.values, repeat=3)
        # remove combinations like (0, 0.25, 0) that just look black and hide detail
        colours = [(r, g, b) for r, g, b in combinations if sum([r, g, b]) > 0.5]

        # re-sort
        sets = []
        # want prime, specific value picked by trial-and-error
        stepval = 17
        for i in range(stepval):
            sets.append(colours[i::stepval])
        self._colours = functools.reduce(operator.add, sets)
        self.num_colours = len(self._colours)
        self.reset_colours()

    def reset_colours(self):
        # Clear state and start from the beginning, to make output deterministic.
        # repeat from beginning if user generates a *lot* of colours
        self.endless_colours = itertools.cycle(self._colours)

    def colour(self):
        return next(self.endless_colours)


colour_generator = ColourGenerator()

colour = colour_generator.colour
# for US English speakers
color = colour


def main():
    """Generate test swatches of all colours with current settings.

    This is basically a self-test.  It can't be run in-place because cq-studio will exclude
    the file itself from consideration during reload determinations (because it's part of
    cq-studio), which results in an empty list of files for it to look at.  For testing,
    you can just copy the file outside of the cq-studio package dir.

    Note that the YACV server seems to have a problem with the number of objects here, so
    it will actually give a missing object message about swatch 0 - the specific number it
    supports before the earliest swatches disappear has varied with different versions of
    YACV.
    """
    wp = cq.Workplane("XY")
    swatch_size = 20
    swatches = []
    grid_size = int(math.ceil(math.sqrt(colour_generator.num_colours)))
    colours = colour_generator._colours[:][:100]

    swatch = (
        wp
        .box(swatch_size, swatch_size, 1.0, centered=False)
    )

    for row in range(grid_size):
        for col in range(grid_size):
            if not colours:
                break
            colour_ = colours.pop(0)
            print(f"{row=} {col=} {colour_=}")
            swatches.append(
                swatch
                .translate((col * swatch_size, row * swatch_size, 0))
            )
            swatches[-1].colour = colour_
            swatches[-1].export_stl = False

    return {
        f"swatch-{i}": swatch for i, swatch in enumerate(swatches)
    }
