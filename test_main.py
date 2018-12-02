from classify import main


def test_basic(tmp_path):
    files = ['A000VOI123ZH_00.pdf',
             'E100VOI123ZH_00.pdf',
             'E100PIN105ZH_00.pdf',
             'A100PIN105ZH_00.pdf',
             ]

    paths = [tmp_path / f for f in files]
    for p in paths:
        p.touch()

    main(*rf'....(......).....\.pdf -i {tmp_path} -o {tmp_path}'.split())

    for p in paths:
        assert not p.is_file()

    assert (tmp_path / 'VOI123' / 'A000VOI123ZH_00.pdf').is_file()
    assert (tmp_path / 'VOI123' / 'E100VOI123ZH_00.pdf').is_file()
    assert (tmp_path / 'PIN105' / 'E100PIN105ZH_00.pdf').is_file()
    assert (tmp_path / 'PIN105' / 'A100PIN105ZH_00.pdf').is_file()
