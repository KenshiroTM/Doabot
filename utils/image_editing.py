import io
import os
from PIL import Image

async def speechify(image_bytes: bytes, bubble_index: int, bubble_height_ratio: float) -> io.BytesIO:
    media_dir = "media/speechbubbles"
    bubble_path = os.path.join(media_dir, f"{bubble_index}.png")

    # Load image and bubble
    original_img = Image.open(io.BytesIO(image_bytes))
    with open(bubble_path, "rb") as bubble_file:
        bubble_img = Image.open(bubble_file)
        bubble_img = bubble_img.copy()

    # Keep all RGBA to merge
    if original_img.mode != 'RGBA':
        original_img = original_img.convert('RGBA')
    if bubble_img.mode != 'RGBA':
        bubble_img = bubble_img.convert('RGBA')

    # Resize bubble to fit desired ratios to match on the target
    new_bubble_width = original_img.width
    new_bubble_height = int(original_img.height * bubble_height_ratio)
    bubble_resized = bubble_img.resize((new_bubble_width, new_bubble_height), Image.LANCZOS)

    # Create new image that works as new canvas, we will put both here
    overlay = Image.new('RGBA', original_img.size, (0, 0, 0, 0))

    # Paste the resized bubble onto the overlay (center top offset so it appears on the top inside)
    x_offset = (original_img.width - new_bubble_width) // 2
    y_offset = 0
    overlay.paste(bubble_resized, (x_offset, y_offset), bubble_resized)  # Use alpha as mask
    combined_img = Image.alpha_composite(original_img, overlay) # combine with alpha so it puts with transparency

    combined_img = combined_img.convert('RGB') # convert to rgb and then gif
    buffer = io.BytesIO()
    combined_img.save(buffer, format="GIF")
    buffer.seek(0)

    return buffer
