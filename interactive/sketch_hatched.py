import pathlib

import vsketch

import hatched


class HatchedSketch(vsketch.SketchClass):
    # Image
    image_path = vsketch.Param("/Users/Jacob/Desktop/osk.png", choices=[])  # set via CLI or edit below
    scale = vsketch.Param(1.0, 0.1, 5.0, step=0.1)
    blur = vsketch.Param(10, 0, 50)

    # Levels
    level1 = vsketch.Param(64, 0, 255)
    level2 = vsketch.Param(128, 0, 255)
    level3 = vsketch.Param(192, 0, 255)

    # Hatch
    pitch = vsketch.Param(5.0, 0.5, 30.0, step=0.5)
    angle = vsketch.Param(45.0, 0.0, 180.0, step=1.0)
    circular = vsketch.Param(False)
    invert = vsketch.Param(False)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        path = self.image_path
        if not path or not pathlib.Path(path).exists():
            vsk.text("Set image_path to a valid image file", 10, 10)
            return

        mls = hatched.hatch(
            file_path=path,
            hatch_pitch=self.pitch,
            levels=(self.level1, self.level2, self.level3),
            blur_radius=self.blur,
            image_scale=self.scale,
            invert=self.invert,
            circular=self.circular,
            hatch_angle=self.angle,
            show_plot=False,
            save_svg=False,
        )

        vsk.geometry(mls)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesort")


if __name__ == "__main__":
    HatchedSketch.display()
