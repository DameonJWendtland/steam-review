def generate_review_text(rating, categories, visible_categories, selected_options, audience_vars, design_settings, insert_info):
    review_heading = design_settings.get("review_heading", 1)
    category_heading = design_settings.get("category_heading", 3)
    review_lines = [f"[h{review_heading}]{rating} / 10[/h{review_heading}]"]
    if design_settings.get("credits", False):
        review_lines.append("[url=https://github.com/DameonJWendtland/steam-review-generator]Want to generate reviews? Look here[/url]")
    review_lines.append("")
    for cat, options in categories.items():
        if not visible_categories[cat].get():
            continue
        review_lines.append(f"[h{category_heading}]{cat}[/h{category_heading}]")
        if cat != "Audience" and insert_info.get(cat, "").strip():
            review_lines.append(f"[code] {insert_info[cat]} [/code]")
        if cat == "Audience":
            for option in options:
                marker = "☑" if audience_vars.get(option, False) and audience_vars[option].get() else "☐"
                review_lines.append(f"{marker} {option}")
        else:
            selected = selected_options.get(cat, "")
            for option in options:
                marker = "☑" if option == selected.get() else "☐"
                review_lines.append(f"{marker} {option}")
        review_lines.append("")
    review_lines.append(f"[h{review_heading}]{rating} / 10[/h{review_heading}]")
    return "\n".join(review_lines)
