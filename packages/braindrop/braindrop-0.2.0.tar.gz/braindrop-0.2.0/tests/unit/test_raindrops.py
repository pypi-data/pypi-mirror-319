"""Tests for the Raindrops class."""

##############################################################################
# Local imports.
from braindrop.app.data import Raindrops
from braindrop.raindrop import Raindrop, Tag, TagData


##############################################################################
def test_empty_raindrops_length() -> None:
    """An empty Raindrops should have no length."""
    assert len(Raindrops()) == 0


##############################################################################
def test_populated_raindrops_length() -> None:
    """Raindrops with content should have the correct length."""
    assert len(Raindrops().set_to([Raindrop()])) == 1


##############################################################################
def test_no_filters() -> None:
    """A Raindrops with no filters should report as such."""
    assert not Raindrops().is_filtered


##############################################################################
def test_with_tags_looks_filtered() -> None:
    """A Raindrops with a tag filter should look filtered."""
    assert Raindrops().tagged(Tag("test")).is_filtered


##############################################################################
def test_with_search_looks_filtered() -> None:
    """A Raindrops with a search filter should look filtered."""
    assert Raindrops().containing("test").is_filtered


##############################################################################
def test_found_tags() -> None:
    """A Raindrops with tags within should report back the tags correctly."""
    expecting = "abcdefg"
    repeat = 2
    assert Raindrops(
        raindrops=[Raindrop(tags=[Tag(tag)]) for tag in expecting * repeat]
    ).tags == list(TagData(Tag(tag), repeat) for tag in expecting)


##############################################################################
def test_filter_with_tags() -> None:
    """Applying a tag filter should have the expected result."""
    raindrop_a = Raindrop(tags=[Tag("a")])
    raindrop_b = Raindrop(tags=[Tag("b")])
    raindrops = Raindrops(raindrops=[raindrop_a, raindrop_b])
    assert len(raindrops) == 2
    assert len(raindrops.tagged(Tag("a"))) == 1
    assert next(iter(raindrops.tagged(Tag("a")))) == raindrop_a
    assert len(raindrops.tagged(Tag("b"))) == 1
    assert next(iter(raindrops.tagged(Tag("b")))) == raindrop_b


##############################################################################
def test_filter_with_text() -> None:
    """Applying a test filter should have the expected result."""
    needle = "needle"
    find_these = [
        Raindrop(title=needle),
        Raindrop(excerpt=needle),
        Raindrop(note=needle),
        Raindrop(tags=[Tag(needle)]),
    ]
    not_these = [
        Raindrop(title="title"),
        Raindrop(excerpt="excerpt"),
        Raindrop(note="note"),
        Raindrop(tags=[Tag("tag")]),
    ]
    haystack = find_these + not_these
    raindrops = Raindrops(raindrops=haystack)
    assert len(raindrops) == len(haystack)
    assert list(raindrops.containing(needle)) == find_these


##############################################################################
def test_unfiltering() -> None:
    """We should be able to unfilter a Raidrops."""
    filter_down_to = [
        Raindrop(title="find-this-text", tags=[Tag("find-this-tag")]),
    ]
    originals = filter_down_to + [
        Raindrop(tags=[Tag("find-this-tag")]),
        Raindrop(title="Never find this"),
    ]
    raindrops = Raindrops(raindrops=originals)
    assert len(raindrops) == len(originals)
    assert list(raindrops) == originals
    filters_applied = raindrops.tagged(Tag("find-this-tag")).containing(
        "find-this-text"
    )
    assert list(filters_applied) == filter_down_to
    assert list(filters_applied.unfiltered) == originals


##############################################################################
def test_raindrop_in_raindrops() -> None:
    """We should be able to check if a raindrop is in a Raindrops instance."""
    raindrop = Raindrop(identity=(find_me := 42))
    is_in = Raindrops(
        raindrops=[Raindrop(identity=identity) for identity in range(find_me)]
    ).push(raindrop)
    is_not_in = Raindrops(
        raindrops=[Raindrop(identity=identity) for identity in range(find_me)]
    )
    assert raindrop in is_in
    assert raindrop not in is_not_in


### test_raindrops.py ends here
