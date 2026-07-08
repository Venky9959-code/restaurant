from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File

from ordering.models import Category, MenuItem
from ordering.seed_data import MENU_DATA


class Command(BaseCommand):
    help = "Seed Restaurant Menu"


    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.SUCCESS("Creating Categories..."))

        categories = {}

        for item in MENU_DATA:

            category, _ = Category.objects.get_or_create(
                name=item["category"],
                defaults={"icon": self._category_icon(item["category"])},
            )

            categories[item["category"]] = category

        self.stdout.write(self.style.SUCCESS("Creating Menu Items..."))

        # Static images directory — git-tracked, served by WhiteNoise on Render
        static_foods_dir = (
            Path(settings.BASE_DIR) / "ordering" / "static" / "images" / "foods"
        )

        for item in MENU_DATA:

            category = categories[item["category"]]

            menu, created = MenuItem.objects.update_or_create(

                name=item["name"],

                defaults={

                    "category": category,

                    "description": item["description"],

                    "price": item["price"],

                    "preparation_time": item["prep"],

                    "rating": item["rating"],

                    "is_vegetarian": item["veg"],

                    "is_available": True,

                }

            )

            # -------------------------------------------------------
            # Image resolution strategy (in order of preference):
            #
            # 1. Static file already committed to git → save to ImageField
            #    (copies into media/foods/ which is fine for the current run)
            # 2. Already has a saved image → keep it
            # 3. No image available → leave blank (image_url property
            #    will return the static path directly at render time)
            # -------------------------------------------------------

            if not menu.image:
                image_name = item["name"].replace(" ", "_") + ".jpg"
                static_image_path = static_foods_dir / image_name

                if static_image_path.exists():
                    with open(static_image_path, "rb") as img:
                        menu.image.save(
                            image_name,
                            File(img),
                            save=False,
                        )
                    self.stdout.write(f"  Saved image for {menu.name}")

            menu.save()

            if created:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Added {menu.name}"
                    )
                )

            else:

                self.stdout.write(
                    f"Updated {menu.name}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Restaurant Menu Seeded Successfully!"
            )
        )

    def _category_icon(self, category_name):
        """Return a Bootstrap icon class for each category."""
        icons = {
            "Appetizers":   "bi bi-egg-fried",
            "Burgers":      "bi bi-bag-fill",
            "Pizza":        "bi bi-circle-fill",
            "Pasta":        "bi bi-moisture",
            "Main Course":  "bi bi-bowl-hot-fill",
            "Salads":       "bi bi-flower1",
            "Desserts":     "bi bi-cake2-fill",
            "Beverages":    "bi bi-cup-straw",
        }
        return icons.get(category_name, "bi bi-grid-fill")