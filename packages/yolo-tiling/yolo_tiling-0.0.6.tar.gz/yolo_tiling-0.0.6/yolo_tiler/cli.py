"""Console script for yolo_tiler."""
import argparse
import sys

from yolo_tiler import YoloTiler, TileConfig


def main():
    """Console script for yolo_tiler."""
    parser = argparse.ArgumentParser(description="Tile YOLO dataset images and annotations.")

    parser.add_argument("--source", type=str,
                        help="Source directory containing YOLO dataset")

    parser.add_argument("--target", type=str,
                        help="Target directory for sliced dataset")

    parser.add_argument("--slice_wh", type=int, nargs=2, default=(640, 480),
                        help="Slice width and height")

    parser.add_argument("--overlap_wh", type=float, nargs=2, default=(0.1, 0.1),
                        help="Overlap width and height")

    parser.add_argument("--ext", type=str, default=".png",
                        help="Image extension")

    parser.add_argument("--annotation_type", type=str, default="object_detection",
                        help="Type of annotation")

    parser.add_argument("--densify_factor", type=float, default=0.01,
                        help="Densify factor for segmentation")

    parser.add_argument("--smoothing_tolerance", type=float, default=0.99,
                        help="Smoothing tolerance for segmentation")

    parser.add_argument("--train_ratio", type=float, default=0.7,
                        help="Train split ratio")

    parser.add_argument("--valid_ratio", type=float, default=0.2,
                        help="Validation split ratio")

    parser.add_argument("--test_ratio", type=float, default=0.1,
                        help="Test split ratio")

    args = parser.parse_args()
    config = TileConfig(
        slice_wh=tuple(args.slice_wh),
        overlap_wh=tuple(args.overlap_wh),
        ext=args.ext,
        annotation_type=args.annotation_type,
        densify_factor=args.densify_factor,
        smoothing_tolerance=args.smoothing_tolerance,
        train_ratio=args.train_ratio,
        valid_ratio=args.valid_ratio,
        test_ratio=args.test_ratio
    )
    tiler = YoloTiler(
        source=args.source,
        target=args.target,
        config=config,
    )
    tiler.run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
