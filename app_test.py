from app import process_query


def test_knows_about_dinosaurs():
    assert (process_query("dinosaurs") ==
            "Dinosaurs ruled the Earth 200 million years ago")


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_name_returns_name():
    assert process_query("What is your name?") == "ajc24"


def test_addition_returns_sum():
    assert process_query("What is 97 plus 6?") == "103"


def test_returns_greatest_num():
    assert process_query("Which of the following numbers is the largest: 71, "
                         "39, 38") == "71"
