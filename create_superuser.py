import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')

try:
    django.setup()
    from django.contrib.auth import get_user_model
except Exception as e:
    print(f"[-] Django setup failed: {e}")
    sys.exit(1)


def create_admin():
    User = get_user_model()

    # Credentials — override these via Render Environment Variables:
    #   ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email    = os.environ.get('ADMIN_EMAIL',    'admin@dineflow.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')

    print("=" * 60)
    print("[*] ADMIN SUPERUSER CHECK & CREATION")
    print("=" * 60)

    if User.objects.filter(username=username).exists():
        print(f"[+] Superuser '{username}' already exists — skipping.")
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        print(f"[+] Superuser '{username}' created successfully.")

    print("=" * 60)


if __name__ == '__main__':
    create_admin()
