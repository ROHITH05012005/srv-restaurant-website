import urllib.request
import urllib.parse
import os
import time

# Only the FAILED/MISSING images
menu_images = {
    # TAWA & SANDWICH
    "paneer_pav_bhaji_premium.png": "A premium, realistic, mouth-watering close-up photography of Paneer Pav Bhaji, spicy vegetable bhaji generously covered with grated fresh paneer and butter, served with two butter-toasted soft pavs on a dark plate. Dark background, dramatic lighting, food photography.",
    "cheese_pav_bhaji_premium.png": "A premium, realistic, mouth-watering close-up photography of Cheese Pav Bhaji, rich vegetable mash topped with a melted thick layer of grated cheddar cheese, served with butter pavs on a dark platter. Dark background, cinematic lighting, food photography.",
    "kadai_pav_bhaji_premium.png": "A premium, realistic, mouth-watering close-up photography of Kadai Pav Bhaji, vegetable bhaji cooked in a rustic kadai with diced green capsicum, coriander, and freshly roasted spices, served with butter-toasted buns. Dark background, food photography.",
    "paneer_tawa_pulav_premium.png": "A premium, realistic, mouth-watering close-up photography of Paneer Tawa Pulav, spicy tawa-fried rice loaded with capsicum, tomatoes, and golden sauteed paneer cubes, served with raita in a dark plate. Dark background, cinematic lighting, food photography.",
    "cheese_tawa_pulav_premium.png": "A premium, realistic, mouth-watering close-up photography of Cheese Tawa Pulav, street-style tawa pulav topped with a generous melting layer of shredded cheese and fresh coriander, served in a dark plate. Dark background, dramatic lighting, food photography.",
    "veg_grill_sandwich_premium.png": "A premium, realistic, mouth-watering close-up photography of Grilled Veg Sandwich, toasted bread with golden grill lines, cut in half showing layered cucumber, tomato, potato, and green chutney, served on a slate board. Dark background, food photography.",
    "veg_paneer_grill_sandwich_premium.png": "A premium, realistic, mouth-watering close-up photography of Veg Paneer Grill Sandwich, crispy grilled sandwich filled with spiced paneer tikka cubes, onions, and green chutney, cut diagonally. Dark background, dramatic lighting, food photography.",
    "veg_cheese_paneer_grill_sandwich_premium.png": "A premium, realistic, mouth-watering close-up photography of Grilled Veg Cheese Paneer Sandwich, sliced showing layers of paneer, bell peppers, green chutney, and stringy melted mozzarella cheese inside golden grilled bread. Dark background, food photography.",
    "veg_mushroom_grill_sandwich_premium.png": "A premium, realistic, mouth-watering close-up photography of Grilled Mushroom Sandwich, golden brown grilled bread filled with creamy garlic sauteed mushrooms and herbs, cut in half. Dark background, cinematic lighting, food photography.",
    "paneer_grill_sandwich_premium.png": "A premium, realistic, mouth-watering close-up photography of Paneer Grill Sandwich, grilled sandwich stuffed with thick marinated paneer slices, capsicum, and dry spices, cut in half on a dark platter. Dark background, food photography.",
    "cheese_grill_sandwich_premium.png": "A premium, realistic, mouth-watering close-up photography of a Cheese Grill Sandwich, perfectly grilled golden-brown bread showing a rich, gooey melted cheese pull as it is sliced, served on a dark board. Dark background, dramatic lighting, food photography.",

    # BEVERAGES
    "mosambi_juice_premium.png": "A premium, realistic close-up photography of fresh Mosambi Juice sweet lime, served in a tall chilled glass with a lime slice on the rim, drops of condensation on the glass. Dark background, elegant setup, backlighting, food photography.",
    "orange_juice_premium.png": "A premium, realistic close-up photography of fresh Orange Juice, served in a tall transparent glass with ice cubes and an orange wedge, drops of water on the glass. Dark background, dramatic lighting, food photography.",
    "pineapple_juice_premium.png": "A premium, realistic close-up photography of Pineapple Juice, served in a tall glass garnished with a pineapple leaf and cherry, chilled with ice. Dark background, cinematic lighting, food photography.",
    "water_melon_juice_premium.png": "A premium, realistic close-up photography of fresh Watermelon Juice, vibrant red juice in a chilled glass with a small watermelon slice on the rim and fresh mint leaves. Dark background, backlighting, food photography.",
    "pomegranate_juice_premium.png": "A premium, realistic close-up photography of Pomegranate Juice, dark ruby-red juice in an elegant glass, garnished with pomegranate seeds at the base. Dark background, dramatic lighting, food photography.",
    "apple_shake_premium.png": "A premium, realistic close-up photography of Apple Milkshake, thick cream-colored shake in a glass, garnished with a sprinkle of cinnamon powder and apple slices on top. Dark background, cinematic lighting, food photography.",
    "cold_badam_premium.png": "A premium, realistic close-up photography of Cold Badam Milk, rich yellow milk in a glass, garnished with saffron strands and slivered almonds and pistachios. Dark background, luxury restaurant setting, food photography.",
    "chocolate_shake_premium.png": "A premium, realistic close-up photography of Chocolate Milkshake, rich dark chocolate shake in a glass, topped with whipped cream, chocolate shavings, and a straw. Dark background, cinematic lighting, food photography.",
    "sweet_lassi_premium.png": "A premium, realistic close-up photography of Sweet Punjabi Lassi, thick churned yogurt drink in a traditional clay kulhad glass, topped with a thick layer of malai cream and chopped pistachios. Dark background, food photography.",
    "dry_fruit_lassi_premium.png": "A premium, realistic close-up photography of Dry Fruit Lassi, creamy sweet yogurt lassi garnished heavily with chopped almonds, cashews, pistachios, and saffron. Dark background, dramatic lighting, food photography.",
    "masala_soda_premium.png": "A premium, realistic close-up photography of Indian Masala Soda, sparkling fizzy drink in a glass with lemon slices, mint leaves, spices, and rising bubbles. Dark background, backlighting, food photography.",

    # DESSERTS
    "holige_premium.png": "A premium, realistic, mouth-watering close-up photography of Holige Obbattu, traditional sweet flatbread served warm on a dark plate, with a golden pool of melting ghee poured on top. Dark background, rustic style, food photography.",
    "vanilla_ice_cream_premium.png": "A premium, realistic, mouth-watering close-up photography of Vanilla Ice Cream, a perfect round scoop of creamy vanilla bean ice cream served in a dark ceramic bowl, garnished with a single mint leaf. Dark background, food photography.",
    "strawberry_ice_cream_premium.png": "A premium, realistic, mouth-watering close-up photography of Strawberry Ice Cream, a scoop of creamy pink ice cream containing real strawberry chunks, served in a black bowl. Dark background, cinematic lighting, food photography.",
    "chocolate_ice_cream_premium.png": "A premium, realistic, mouth-watering close-up photography of Chocolate Ice Cream, a scoop of rich dark chocolate ice cream drizzled with chocolate fudge sauce, served in a dark bowl. Dark background, dramatic lighting, food photography.",
    "mango_ice_cream_premium.png": "A premium, realistic, mouth-watering close-up photography of Mango Ice Cream, a vibrant yellow scoop of Alphonso mango ice cream garnished with small diced mango pieces, served in a dark bowl. Dark background, food photography.",
    "fruit_salad_premium.png": "A premium, realistic, mouth-watering close-up photography of a Fruit Salad bowl, filled with diced apples, bananas, grapes, pineapple, and pomegranate seeds, glinting under soft light. Dark background, elegant bowl, food photography.",
    "fruit_salad_ice_cream_premium.png": "A premium, realistic, mouth-watering close-up photography of Fruit Salad with Ice Cream, diced colorful fresh fruits topped with a premium scoop of vanilla ice cream and cherry, served in an elegant glass bowl. Dark background, food photography.",
    "srv_special_ice_cream_premium.png": "A premium, realistic, mouth-watering close-up photography of a signature Ice Cream Sundae, three layers of different ice cream scoops topped with mixed dry fruits, colorful syrups, wafers, and a cherry. Dark background, food photography.",
    "chocolate_nut_sundae_premium.png": "A premium, realistic, mouth-watering close-up photography of Chocolate Nut Sundae, two scoops of chocolate ice cream layered with chocolate sauce, loaded with hot roasted cashew and almond bits in a glass bowl. Dark background, food photography.",
    "raja_rani_premium.png": "A premium, realistic, mouth-watering close-up photography of Raja Rani Ice Cream, a royal sundae with two scoops of contrasting ice creams, fruit cocktail, jelly cubes, rose syrup, and crushed nuts. Dark background, food photography.",
    "titanic_special_premium.png": "A premium, realistic, mouth-watering close-up photography of Titanic Special Ice Cream, three scoops of ice cream served in a long boat-shaped glass dish, layered with sliced bananas, apples, cherry, whipped cream, and chocolate sauce. Dark background, food photography.",

    # CHATS
    "sev_puri_premium.png": "A premium, realistic, mouth-watering close-up photography of Sev Puri, flat crispy puris loaded with potato mash, drizzled with sweet tamarind and spicy mint chutneys, covered with a mountain of yellow sev. Dark background, food photography.",
    "special_sev_puri_premium.png": "A premium, realistic, mouth-watering close-up photography of Special Sev Puri, sev puri enhanced with grated fresh paneer, finely chopped onions, pomegranate seeds, and chat masala, served on a black plate. Dark background, food photography.",
    "dry_bhel_puri_premium.png": "A premium, realistic, mouth-watering close-up photography of Dry Bhel Puri, puffed rice mixed with dry spices, sev, roasted peanuts, and finely chopped raw mango, onion, and coriander, served in a paper cone. Dark background, food photography.",
    "corn_bhel_puri_premium.png": "A premium, realistic, mouth-watering close-up photography of Corn Bhel, puffed rice mixed with sweet yellow corn kernels, sev, tomatoes, onions, and sweet tamarind chutney, served in a dark ceramic bowl. Dark background, food photography.",
    "samosa_masala_premium.png": "A premium, realistic, mouth-watering close-up photography of Samosa Masala, crushed hot crispy samosa covered in dark spiced peas gravy, topped with fine sev, onions, and coriander, served in a dark plate. Dark background, food photography.",
    "samosa_chat_premium.png": "A premium, realistic, mouth-watering close-up photography of Samosa Chat, broken samosas layered with thick yogurt, green mint chutney, red tamarind chutney, spices, sev, and pomegranate seeds. Dark background, dramatic lighting, food photography.",
    "cheese_vada_pav_premium.png": "A premium, realistic, mouth-watering close-up photography of Cheese Vada Pav, Mumbai vada pav with a slice of melting cheddar cheese draped over the hot potato dumpling inside the soft bun. Dark background, food photography.",
    "dahi_potato_premium.png": "A premium, realistic, mouth-watering close-up photography of Dahi Aloo, boiled potato cubes bathed in sweet whipped yogurt, sprinkled with red chili powder, cumin powder, and green chutney, in a dark bowl. Dark background, food photography.",
    "dahi_samosa_chat_premium.png": "A premium, realistic, mouth-watering close-up photography of Dahi Samosa, broken samosa pieces covered in a blanket of thick sweet chilled yogurt, sweet tamarind chutney, coriander, and fine sev. Dark background, food photography.",
    "dahi_aloo_puri_premium.png": "A premium, realistic, mouth-watering close-up photography of Dahi Puri, round hollow puris stuffed with potatoes, filled with chilled sweet yogurt, sweet and green chutneys, and topped with sev and fresh coriander. Dark background, food photography.",
    "dahi_papdi_premium.png": "A premium, realistic, mouth-watering close-up photography of Dahi Papdi Chat, flat crisp papdis topped with potato mash, sweet chilled curd, tamarind chutney, and a generous sprinkle of chat spices and sev. Dark background, food photography.",

    # BIRYANI & MEALS (remaining)
    "north_delux_meals_premium.png": "A premium, realistic, mouth-watering close-up photography of a Deluxe North Indian Thali, featuring butter naan, paneer curry, black dal makhani, veg pulao, raita, gulab jamun, and salad served in small metal bowls on a dark tray. Dark background, cinematic lighting, food photography.",
    "south_delux_meals_premium.png": "A premium, realistic, mouth-watering close-up photography of a Deluxe South Indian Thali, featuring white rice, sambar, rasam, kootu, poriyal, payasam, appalam papadum, and curd served on a banana leaf on a dark surface. Dark background, dramatic lighting, food photography.",
    "mudde_meals_premium.png": "A premium, realistic, mouth-watering close-up photography of Mudde Meals, a traditional healthy steaming Ragi Mudde finger millet ball topped with a dollop of ghee, served with hot bassaru vegetable broth curry in a dark plate. Dark background, rustic setup, food photography.",
    "veg_pulav_premium.png": "A premium, realistic, mouth-watering close-up photography of Veg Pulav, aromatic basmati rice cooked with whole spices, green peas, carrots, and french beans, served in a dark ceramic bowl. Dark background, cinematic lighting, food photography.",
    "ghee_rice_premium.png": "A premium, realistic, mouth-watering close-up photography of Ghee Rice, rich and aromatic basmati rice cooked in pure cow ghee, garnished with golden fried cashews and raisins, served in a black bowl. Dark background, luxury presentation, food photography.",
    "jeera_rice_premium.png": "A premium, realistic, mouth-watering close-up photography of Jeera Rice, fluffy steamed basmati rice tempered with roasted cumin seeds and fresh coriander, served in a dark dish. Dark background, cinematic lighting, food photography.",
    "dal_kichidi_premium.png": "A premium, realistic, mouth-watering close-up photography of Dal Khichdi, a comforting hot pot meal of mushy rice and yellow moong dal cooked with turmeric, cumin, and a ghee tadka on top, served in a dark clay bowl. Dark background, dramatic lighting, food photography.",
    "palak_kichidi_premium.png": "A premium, realistic, mouth-watering close-up photography of Palak Khichdi, comforting rice-lentil porridge blended with vibrant green spinach puree, topped with fried garlic and ghee, served in a black bowl. Dark background, cinematic lighting, food photography.",
    "kashmiri_pulav_premium.png": "A premium, realistic, mouth-watering close-up photography of Kashmiri Pulao, sweet saffron-flavored colorful rice loaded with fresh apple slices, pomegranate seeds, and roasted almonds, cashews, and pistachios, served in an elegant dark bowl. Dark background, food photography.",
    "mushroom_biryani_premium.png": "A premium, realistic, mouth-watering close-up photography of Mushroom Dum Biryani, fragrant basmati rice slow-cooked in dum style with spicy marinated button mushrooms, mint, and saffron, served in a dark clay pot. Dark background, dramatic lighting, food photography.",
    "kaju_paneer_mutter_pulav_premium.png": "A premium, realistic, mouth-watering close-up photography of Kaju Paneer Mutter Pulao, royal pulao with green peas, paneer cubes, and roasted cashews embedded in seasoned fluffy long-grain rice, served in a dark ceramic dish. Dark background, food photography.",

    # REMAINING RICE & NOODLES
    "schezwan_noodles_premium.png": "A premium, realistic, mouth-watering close-up photography of Schezwan Noodles, spicy red-orange noodles tossed in fiery Schezwan chili paste and spring onions, served in a dark bowl. Dark background, dramatic lighting, food photography.",
    "mushroom_noodles_premium.png": "A premium, realistic, mouth-watering close-up photography of Mushroom Noodles, wok-tossed noodles with tender sauteed button mushrooms, green onions, and light soy sauce, served in a black dish. Dark background, cinematic lighting, food photography.",
    "chow_mein_noodles_premium.png": "A premium, realistic, mouth-watering close-up photography of Chow Mein, traditional street-style fried noodles with crunchy cabbage, julienned carrots, onions, and dark soy sauce. Dark background, dramatic lighting, food photography.",
    "veg_triple_noodles_premium.png": "A premium, realistic, mouth-watering close-up photography of Veg Triple Schezwan, a layered combination of fried rice, noodles, and a rich red spicy vegetable Manchurian gravy served separately in a small dark bowl. Dark background, luxury food photography.",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def main():
    total = len(menu_images)
    print(f"[START] Anonymous mode downloader for {total} images (no API key)...")
    downloaded = skipped = failed = 0

    for i, (filename, prompt) in enumerate(menu_images.items(), 1):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            skipped += 1
            print(f"[{i}/{total}] Skipped: {filename}")
            continue

        print(f"[{i}/{total}] Downloading: {filename}...", end="", flush=True)
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&nologo=true&private=true&enhance=false&model=sana"
        req = urllib.request.Request(url, headers=headers)

        success = False
        retries = 3
        while retries > 0 and not success:
            try:
                with urllib.request.urlopen(req, timeout=120) as response:
                    with open(filename, "wb") as f:
                        f.write(response.read())
                print(" Done!")
                success = True
                downloaded += 1
                time.sleep(2.0)
            except Exception as e:
                retries -= 1
                if retries == 0:
                    print(f" FAILED! ({e})")
                    failed += 1
                else:
                    print(f" Retrying ({e})...", end="", flush=True)
                    time.sleep(6.0)

    print(f"\n[DONE] Total: {total} | Downloaded: {downloaded} | Skipped: {skipped} | Failed: {failed}")

if __name__ == "__main__":
    main()
