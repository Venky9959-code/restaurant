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
                name=item["category"]
            )

            categories[item["category"]] = category

        self.stdout.write(self.style.SUCCESS("Creating Menu Items..."))

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

            image_name = item["name"].replace(" ", "_") + ".jpg"

            image_path = Path(settings.MEDIA_ROOT) / "foods" / image_name

            if image_path.exists():

                with open(image_path, "rb") as img:

                    menu.image.save(
                        image_name,
                        File(img),
                        save=False
                    )

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