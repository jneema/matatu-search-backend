from app.services.stage_resolver import CONFIRM_THRESHOLD, SUGGEST_THRESHOLD


def test_confirm_threshold_value():
    assert CONFIRM_THRESHOLD == 85


def test_suggest_threshold_value():
    assert SUGGEST_THRESHOLD == 75


def test_cheapest_tag_logic():
    fares = [100, 60, 80]
    assert min(fares) == 60


def test_fuzzy_score_below_suggest():
    from rapidfuzz import fuzz
    score = fuzz.token_sort_ratio("xyznonexistent", "Juja Stage")
    assert score < SUGGEST_THRESHOLD


def test_fuzzy_exact_string_scores_100():
    from rapidfuzz import fuzz
    score = fuzz.token_sort_ratio("juja stage", "juja stage")
    assert score == 100


def test_fuzzy_area_exact_scores_100():
    from rapidfuzz import fuzz
    score = fuzz.token_sort_ratio("juja", "juja")
    assert score == 100


def test_fuzzy_nonsense_scores_below_suggest():
    from rapidfuzz import fuzz
    score = fuzz.token_sort_ratio("random123", "Roysambu Stage")
    assert score < SUGGEST_THRESHOLD


# token_sort_ratio penalises length difference — "juja" vs "Juja Stage"
# scores ~43, well below SUGGEST_THRESHOLD. The resolver must use
# partial_ratio for short area-name queries so "juja" still matches
# "Juja Stage", "Juja Town Stage", etc.
def test_fuzzy_area_partial_matches_stage_name():
    from rapidfuzz import fuzz
    score = fuzz.partial_ratio("juja", "Juja Stage")
    assert score >= SUGGEST_THRESHOLD


def test_fuzzy_area_token_sort_fails_for_short_names():
    """
    Documents a known limitation: token_sort_ratio should NOT be used
    when the query is a short area name and the candidate is a full
    stage name. partial_ratio handles this correctly instead.
    """
    from rapidfuzz import fuzz
    score = fuzz.token_sort_ratio("juja", "Juja Stage")
    assert score < SUGGEST_THRESHOLD  # ~43, intentionally below threshold
