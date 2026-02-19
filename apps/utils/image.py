import io
from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile


def compress_image(image_field, max_width=1200, quality=82):
    """
    Compress and resize an ImageField's file.
    Converts PNGs to WebP for massive size reduction.
    Returns the processed image as an InMemoryUploadedFile.

    Typical results:
      - 17MB PNG → ~100-200KB WebP
      - 4MB PNG  → ~50-100KB WebP
    """
    img = PILImage.open(image_field)

    # Convert RGBA/P to RGB (WebP supports transparency but JPEG doesn't)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Resize if wider than max_width, preserving aspect ratio
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), PILImage.LANCZOS)

    # Save as WebP (much smaller than PNG/JPEG)
    buffer = io.BytesIO()
    img.save(buffer, format='WEBP', quality=quality, optimize=True)
    buffer.seek(0)

    # Generate new filename with .webp extension
    original_name = image_field.name
    if '.' in original_name:
        new_name = original_name.rsplit('.', 1)[0] + '.webp'
    else:
        new_name = original_name + '.webp'

    return InMemoryUploadedFile(
        file=buffer,
        field_name='image',
        name=new_name,
        content_type='image/webp',
        size=buffer.getbuffer().nbytes,
        charset=None,
    )
