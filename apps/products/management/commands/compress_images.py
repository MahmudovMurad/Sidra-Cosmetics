import os
from django.core.management.base import BaseCommand
from apps.products.models import ProductImage
from apps.utils.image import compress_image


class Command(BaseCommand):
    help = 'Compress all existing product images (converts to WebP, resizes to 1200px max)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be compressed without actually doing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        images = ProductImage.objects.all()
        total = images.count()

        self.stdout.write(f"Found {total} product images to process...")

        compressed = 0
        skipped = 0
        total_saved = 0

        for i, product_image in enumerate(images, 1):
            try:
                if not product_image.image:
                    skipped += 1
                    continue

                # Skip already-compressed WebP files
                if product_image.image.name.lower().endswith('.webp'):
                    self.stdout.write(f"  [{i}/{total}] SKIP (already WebP): {product_image.image.name}")
                    skipped += 1
                    continue

                old_size = product_image.image.size
                old_name = product_image.image.name

                if dry_run:
                    self.stdout.write(
                        f"  [{i}/{total}] WOULD COMPRESS: {old_name} "
                        f"({old_size / 1024 / 1024:.1f} MB)"
                    )
                    compressed += 1
                    continue

                # Open and compress the image
                product_image.image.open('rb')
                new_image = compress_image(product_image.image)
                product_image.image.close()

                # Save the compressed image (triggers upload_to)
                product_image.image.save(new_image.name, new_image, save=False)
                product_image.save_base(raw=True)  # Skip the save() override

                new_size = product_image.image.size
                saved = old_size - new_size
                total_saved += saved

                self.stdout.write(
                    self.style.SUCCESS(
                        f"  [{i}/{total}] COMPRESSED: {old_name} → {product_image.image.name} "
                        f"({old_size / 1024 / 1024:.1f} MB → {new_size / 1024:.0f} KB, "
                        f"saved {saved / 1024 / 1024:.1f} MB)"
                    )
                )
                compressed += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  [{i}/{total}] ERROR: {product_image.image.name} — {e}")
                )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Done! Compressed: {compressed}, Skipped: {skipped}"))
        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f"Total space saved: {total_saved / 1024 / 1024:.1f} MB"))
