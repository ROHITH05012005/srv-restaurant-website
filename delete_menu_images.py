import os
import glob

keep_list = {
    'about_main_premium.png',
    'about_sec_premium.png',
    'south_indian_meals_premium.png',
    'dosa_special_premium.png',
    'filter_coffee_premium.png',
    'hero_bg_premium.png',
    'idli_premium.png',
    'paneer_tikka_masala_premium.png',
    'gallery_snacks_premium.png',
    'avatar_ramesh_premium.png',
    'avatar_priya_premium.png',
    'avatar_suresh_premium.png',
}

images_dir = 'assets/images'
all_images = glob.glob(os.path.join(images_dir, '*'))

deleted_count = 0
for img_path in all_images:
    basename = os.path.basename(img_path)
    if basename not in keep_list:
        try:
            os.remove(img_path)
            deleted_count += 1
        except Exception as e:
            print(f"Failed to delete {basename}: {e}")

print(f"Deleted {deleted_count} menu images from assets/images.")
