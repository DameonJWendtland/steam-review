# gui/review_generator.py
def generate_review_text(rating, categories, visible_categories, selected_options, audience_vars):
    review_lines = [f"[h1]{rating} / 10[/h1]", ""]
    for cat, options in categories.items():
        if not visible_categories[cat].get():
            continue
        review_lines.append(f"[h3]{cat}[/h3]")
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
    review_lines.append(f"[h1]{rating} / 10[/h1]")
    return "\n".join(review_lines)
