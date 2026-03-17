"""
Image Generation Module for Ouroboros
Provides procedural image generation capabilities using PIL and matplotlib.
Can be extended with external APIs (DALL-E, Stable Diffusion) when available.
"""

import base64
import io
import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class ImageGenerator:
    """Core image generation class with multiple techniques."""

    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height

    def create_canvas(self, color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """Create a blank canvas."""
        return Image.new("RGB", (self.width, self.height), color)

    def generate_abstract_art(
        self,
        palette: List[Tuple[int, int, int]] = None,
        shapes: int = 20,
        seed: Optional[int] = None
    ) -> Image.Image:
        """Generate abstract art with random shapes."""
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        if palette is None:
            palette = [
                (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                for _ in range(5)
            ]

        img = self.create_canvas((20, 20, 30))
        draw = ImageDraw.Draw(img)

        for _ in range(shapes):
            shape_type = random.choice(["rectangle", "ellipse", "polygon"])
            color = random.choice(palette)
            alpha = random.randint(30, 200)

            if shape_type == "rectangle":
                x1 = random.randint(0, self.width)
                y1 = random.randint(0, self.height)
                x2 = random.randint(x1, self.width)
                y2 = random.randint(y1, self.height)
                draw.rectangle([x1, y1, x2, y2], fill=color + (alpha,))

            elif shape_type == "ellipse":
                x1 = random.randint(0, self.width)
                y1 = random.randint(0, self.height)
                x2 = random.randint(x1, self.width)
                y2 = random.randint(y1, self.height)
                draw.ellipse([x1, y1, x2, y2], fill=color + (alpha,))

            else:  # polygon
                points = [
                    (random.randint(0, self.width), random.randint(0, self.height))
                    for _ in range(random.randint(3, 6))
                ]
                draw.polygon(points, fill=color + (alpha,))

        return img

    def generate_landscape(
        self,
        terrain_type: str = "mountains",
        seed: Optional[int] = None
    ) -> Image.Image:
        """Generate a simple fantasy landscape."""
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        img = self.create_canvas()

        # Sky gradient
        draw = ImageDraw.Draw(img)
        for y in range(self.height // 2):
            color = (
                int(135 + (y / (self.height / 2)) * 50),
                int(206 - (y / (self.height / 2)) * 50),
                int(235 - (y / (self.height / 2)) * 50)
            )
            draw.line([(0, y), (self.width, y)], fill=color)

        # Terrain based on type
        if terrain_type == "mountains":
            self._draw_mountains(draw)
        elif terrain_type == "forest":
            self._draw_forest(draw)
        elif terrain_type == "plains":
            self._draw_plains(draw)
        elif terrain_type == "desert":
            self._draw_desert(draw)
        else:
            self._draw_mountains(draw)  # default

        return img

    def _draw_mountains(self, draw: ImageDraw.Draw):
        """Draw mountain range."""
        ground_level = self.height * 2 // 3
        # Mountains
        for i in range(5):
            x_start = i * self.width // 4
            x_mid = x_start + self.width // 8
            x_end = x_start + self.width // 4
            peak_y = random.randint(50, ground_level - 100)

            draw.polygon([
                (x_start, ground_level),
                (x_mid, peak_y),
                (x_end, ground_level)
            ], fill=(100, 100, 120))

        # Base
        draw.rectangle([0, ground_level, self.width, self.height], fill=(60, 80, 40))

    def _draw_forest(self, draw: ImageDraw.Draw):
        """Draw forest."""
        ground_level = self.height * 2 // 3
        # Ground
        draw.rectangle([0, ground_level, self.width, self.height], fill=(34, 139, 34))

        # Trees
        for x in range(20, self.width, 40):
            tree_height = random.randint(80, 150)
            tree_y = ground_level - tree_height
            draw.rectangle([x - 10, tree_y, x + 10, ground_level], fill=(101, 67, 33))
            draw.polygon([
                (x, tree_y - 40),
                (x - 30, tree_y + 20),
                (x + 30, tree_y + 20)
            ], fill=(0, 100, 0))
            draw.polygon([
                (x, tree_y - 60),
                (x - 25, tree_y),
                (x + 25, tree_y)
            ], fill=(0, 80, 0))

    def _draw_plains(self, draw: ImageDraw.Draw):
        """Draw plains."""
        ground_level = self.height * 2 // 3
        draw.rectangle([0, ground_level, self.width, self.height], fill=(154, 205, 50))
        # Add some grass tufts
        for x in range(0, self.width, 20):
            y = ground_level + random.randint(0, 50)
            draw.line([x, y, x + 5, y - 10], fill=(100, 160, 30))

    def _draw_desert(self, draw: ImageDraw.Draw):
        """Draw desert."""
        ground_level = self.height * 2 // 3
        draw.rectangle([0, ground_level, self.width, self.height], fill=(238, 214, 175))
        # Dunes
        for i in range(3):
            x_offset = i * self.width // 3
            draw.ellipse([
                x_offset, ground_level - 50,
                x_offset + self.width // 2, ground_level + 100
            ], fill=(222, 184, 135))

    def add_text(
        self,
        img: Image.Image,
        text: str,
        position: Tuple[int, int] = None,
        font_size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255)
    ) -> Image.Image:
        """Add text to image."""
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()

        if position is None:
            bbox = draw.textbbox((0, 0), text, font=font)
            position = ((self.width - bbox[2]) // 2, 20)

        draw.text(position, text, fill=color, font=font)
        return img

    def apply_filter(
        self,
        img: Image.Image,
        filter_type: str = "blur"
    ) -> Image.Image:
        """Apply a filter to the image."""
        if filter_type == "blur":
            return img.filter(ImageFilter.BLUR)
        elif filter_type == "sharpen":
            return img.filter(ImageFilter.SHARPEN)
        elif filter_type == "edge_enhance":
            return img.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == "emboss":
            return img.filter(ImageFilter.EMBOSS)
        else:
            return img

    def to_base64(self, img: Image.Image, format: str = "PNG") -> str:
        """Convert image to base64 string."""
        buffer = io.BytesIO()
        img.save(buffer, format=format)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    def save_to_file(self, img: Image.Image, path: str, format: str = "PNG"):
        """Save image to file."""
        img.save(path, format=format)

    def generate_ascii_art(self, img: Image.Image, width: int = 80) -> str:
        """Convert image to ASCII art."""
        img = img.resize((width, int(width * img.height / img.width)))
        img = img.convert("L")

        ascii_chars = "@%#*+=-:. "

        result = ""
        for y in range(img.height):
            for x in range(img.width):
                pixel = img.getpixel((x, y))
                char_index = int(pixel / 256 * len(ascii_chars))
                result += ascii_chars[char_index]
            result += "\n"

        return result


def generate_fantasy_scene(
    generator: ImageGenerator,
    scene_type: str,
    seed: Optional[int] = None
) -> Tuple[Image.Image, str]:
    """Generate a complete fantasy scene with description."""
    img = generator.generate_landscape(terrain_type=scene_type, seed=seed)

    # Add atmospheric effects
    draw = ImageDraw.Draw(img)
    for _ in range(50):
        x = random.randint(0, generator.width)
        y = random.randint(0, generator.height // 2)
        size = random.randint(1, 3)
        draw.ellipse([x, y, x+size, y+size], fill=(255, 255, 200, 150))

    return img, f"Фэнтези ландшафт: {scene_type}"


# Quick utility functions
def quick_generate(
    mode: str = "abstract",
    width: int = 800,
    height: int = 600,
    **kwargs
) -> Image.Image:
    """Quick one-line image generation."""
    gen = ImageGenerator(width, height)

    if mode == "abstract":
        return gen.generate_abstract_art(**kwargs)
    elif mode == "landscape":
        return gen.generate_landscape(**kwargs)
    else:
        return gen.create_canvas()


def image_to_base64_data_url(img: Image.Image, format: str = "PNG") -> str:
    """Convert image to data URL for embedding."""
    base64_str = quick_generate().to_base64(img, format)
    mime_type = "image/png" if format.upper() == "PNG" else "image/jpeg"
    return f"data:{mime_type};base64,{base64_str}"
