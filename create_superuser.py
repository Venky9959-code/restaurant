import os
import sys

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

try:
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    from django.db import connections
except Exception as e:
    print(f"[-] Django setup failed: {e}")
    sys.exit(1)

def create_admin():
    User = get_user_model()
    # Default credentials (can be overridden using environment variables in Render Dashboard)
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'venky995982@gmail.com')
    password = os.environ.get('ADMIN_PASSWORD', 'restaurant@123')

    print("=" * 60)
    print("[*] AUTOMATIC ADMIN SUPERUSER CHECK & CREATION")
    print("=" * 60)

    # 1. Check and create in default database (SQLite)
    try:
        if not User.objects.using('default').filter(username=username).exists():
            User.objects.db_manager('default').create_superuser(username=username, email=email, password=password)
            print(f"[+] Superuser '{username}' created successfully in 'default' (SQLite) database!")
            print(f"    -> Login Username: {username}")
            print(f"    -> Login Password: {password}")
        else:
            print(f"[*] Superuser '{username}' already exists in 'default' database.")
    except Exception as e:
        print(f"[-] Could not create superuser in 'default' db: {e}")

    # 2. Check and create in MySQL database (if configured and connected)
    try:
        conn = connections['mysql_db']
        conn.ensure_connection()
        if not User.objects.using('mysql_db').filter(username=username).exists():
            User.objects.db_manager('mysql_db').create_superuser(username=username, email=email, password=password)
            print(f"[+] Superuser '{username}' created successfully in 'mysql_db' (MySQL) database!")
        else:
            print(f"[*] Superuser '{username}' already exists in 'mysql_db' database.")
    except Exception as e:
        print(f"[*] Note: 'mysql_db' skipped (server offline or tables not migrated): {e}")

    print("=" * 60)

if __name__ == '__main__':
    create_admin()