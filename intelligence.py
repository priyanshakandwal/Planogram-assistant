def generate_recommendations(detections, image_height):
    eye_min = image_height * 0.35
    eye_max = image_height * 0.6

    eye_level = []
    bottom_shelf = []
    top_shelf = []

    product_count = {}

    # Retail category priority
    premium_items = {"perfume", "cosmetics", "cream", "skincare"}
    daily_use_items = {"soap", "shampoo", "bottle", "lotion"}

    for det in detections:
        label = det["label"]
        y = det["y_center"]

        product_count[label] = product_count.get(label, 0) + 1

        if eye_min <= y <= eye_max:
            eye_level.append(label)
        elif y > eye_max:
            bottom_shelf.append(label)
        else:
            top_shelf.append(label)

    tips = []

    # Eye-level strategy
    for item in premium_items:
        if item in product_count and item not in eye_level:
            tips.append(
                f"Place premium product '{item}' at eye level to increase impulse purchases."
            )

    # Bottom shelf logic
    if bottom_shelf:
        tips.append(
            f"Low-visibility products {set(bottom_shelf)} should be moved upward for better reach."
        )

    # Overcrowding detection
    for product, count in product_count.items():
        if count > 5:
            tips.append(
                f"Overcrowding detected for '{product}'. Reduce facings to improve shelf clarity."
            )

    # Assortment balance
    if len(product_count) < 3:
        tips.append(
            "Shelf assortment is limited. Add product variety to increase customer engagement."
        )

    return tips
