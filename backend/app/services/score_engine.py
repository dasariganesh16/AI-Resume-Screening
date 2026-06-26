def calculate_final_score(
    similarity_score,
    skill_match_score,
    bonus_skill_count
):

    bonus_score = min(
        bonus_skill_count * 2,
        10
    )

    final_score = (
        0.6 * skill_match_score
        +
        0.3 * similarity_score
        +
        0.1 * bonus_score
    )

    return float(round(final_score, 2))