# gui/rating_calculator.py
import math


def calculate_recommended_rating(categories, visible_categories, selected_options, audience_vars):
    total_score = 0
    count = 0

    def get_score(index, n_options):
        return 10 - index * (9 / (n_options - 1))

    for cat, options in categories.items():
        if not visible_categories[cat].get():
            continue

        if cat == "Audience":
            selected_scores = []
            for option in options:
                if option in audience_vars and audience_vars[option].get():
                    idx = options.index(option)
                    score = get_score(idx, len(options))
                    selected_scores.append(score)
            cat_score = sum(selected_scores) / len(selected_scores) if selected_scores else 5
        else:
            selected_option = selected_options.get(cat, None)
            if selected_option is None or selected_option.get() == "":
                cat_score = 5
            else:
                sel_text = selected_option.get()
                if sel_text in options:
                    idx = options.index(sel_text)
                    cat_score = get_score(idx, len(options))
                else:
                    cat_score = 5

        total_score += cat_score
        count += 1

    if count == 0:
        return 5
    recommended = total_score / count
    recommended = max(1, min(10, recommended))
    return math.floor(recommended)
