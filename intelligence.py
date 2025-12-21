def generate_recommendations(detections, image_height):
    eye_level_min = image_height * 0.4
    eye_level_max = image_height * 0.6

    eye_level_products = []
    combo_products = []
    clearance_products = []

    for det in detections:
        label = det["label"]
        y_center = det["y_center"]

        # Eye level logic
        if eye_level_min <= y_center <= eye_level_max:
            eye_level_products.append(label)

        # Combo logic
        if label in ["backpack", "handbag", "bottle"]:
            combo_products.append(label)

        # Clearance logic
        if label in ["umbrella"]:
            clearance_products.append(label)

    tips = []

    if eye_level_products:
        tips.append(
            f"Place {set(eye_level_products)} at eye level for higher sales."
        )

    if combo_products:
        tips.append(
            f"Create combo offers using {set(combo_products)}."
        )

    if clearance_products:
        tips.append(
            f"Apply discounts to {set(clearance_products)} to clear stock."
        )

    return tips
