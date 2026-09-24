#!/usr/bin/env -S uv run --script

from src.arguments import get_args
from src.label_generator import LabelGenerator


def main():
    args = get_args()
    label_generator = LabelGenerator(args)
    label_generator.generate_pdf()


if __name__ == "__main__":
    main()
