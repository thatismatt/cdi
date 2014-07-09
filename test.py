from nose.tools import assert_equal

from cdi import score_match, filter_dir, FileStat

def test_single_ch_contained_in_dir_name():
    listing = [
        FileStat("node", is_file=False, is_dir=True),
        FileStat("mode", is_file=False, is_dir=True)
    ]
    result = filter_dir(listing, ["n"])
    assert_equal(["node"], result.dirs)

def test_score_match_is_1_for_empty_filter():
    result = score_match([], "cat")
    assert result > 0

def test_score_match_is_0_for_ch_not_in_name():
    result = score_match(["b"], "cat")
    assert_equal(0, result)

def test_score_match_is_1_for_ch_in_name():
    result = score_match(["c"], "cat")
    assert result > 0

def test_score_match_is_1_for_all_chs_in_name_consecutive():
    result = score_match(["c", "a"], "cat")
    assert result > 0

def test_score_match_is_1_for_all_chs_in_name_non_consecutive():
    result = score_match(["c", "t"], "cat")
    assert result > 0

def test_score_match_is_0_for_some_chs_not_in_name():
    result = score_match(["c", "b"], "cat")
    assert_equal(0, result)

def test_score_match_is_0_for_chs_not_in_order_in_name():
    result = score_match(["a", "c"], "cat")
    assert_equal(0, result)

def test_score_is_greater_if_ch_is_at_start_of_name():
    chs = ["c"]
    assert score_match(chs, "cat") > score_match(chs, "act")

def test_score_is_zero_if_name_does_not_contain_duplicates_in_ch():
    chs = ["a", "a"]
    assert_equal(0, score_match(chs, "a"))

def test_score_is_greater_if_ch_is_at_start_of_name():
    chs = ["c", "a", "t"]
    assert score_match(chs, "carrot") < score_match(chs, "cat")

def test_score_is_greater_if_ch_occurs_after_word_boundary():
    chs = ["c", "a"]
    assert score_match(chs, "c-at") > score_match(chs, "cat")
