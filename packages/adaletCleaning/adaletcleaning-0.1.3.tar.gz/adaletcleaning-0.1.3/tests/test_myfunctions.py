from adaletCleaning import Cleaning


def test_clean():
    text = "T.C. Av. Mehmet Kadıköy'den10 İstanbul'a geçti."
    expected = "tc avukat mehmet den geçti"
    print(Cleaning(text).clean())
    assert Cleaning(text).clean() == expected
