import pytest

from bible_music.domain.scripture import ScriptureRange


@pytest.mark.parametrize("offsets", [(-1, 1), (2, 2), (3, 2)])
def test_scripture_range_requires_a_nonempty_range_of_word_offsets(offsets):
    with pytest.raises(ValueError, match="ordered nonnegative"):
        ScriptureRange("edition", *offsets)


def test_scripture_range_can_start_at_the_edition_first_word():
    scripture = ScriptureRange("edition", 0, 1)
    assert scripture.contains(ScriptureRange("edition", 0, 1))
    assert scripture.contains(ScriptureRange(b"edition".decode(), 0, 1))
    assert not scripture.contains(ScriptureRange("earlier", 0, 1))
    assert not scripture.contains(ScriptureRange("other", 0, 1))


def test_scripture_range_contains_only_spans_inside_its_edition_bounds():
    scripture = ScriptureRange("edition", 5, 9)
    assert scripture.contains(ScriptureRange("edition", 6, 8))
    assert not scripture.contains(ScriptureRange("edition", 4, 8))
    assert not scripture.contains(ScriptureRange("edition", 6, 10))
