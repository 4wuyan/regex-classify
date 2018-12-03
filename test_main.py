from classify import main
import os
from pathlib import Path


def test_basic(tmp_path):
    os.chdir(tmp_path)

    files = ['A000VOI123ZH_00.pdf',
             'E100VOI123ZH_00.pdf',
             'E100PIN105ZH_00.pdf',
             'A100PIN105ZH_00.pdf',
             ]

    paths = [Path(f) for f in files]
    for p in paths:
        p.touch()

    main(*rf'....(......).....\.pdf'.split())

    for p in paths:
        assert not p.is_file()

    assert (tmp_path / 'VOI123' / 'A000VOI123ZH_00.pdf').is_file()
    assert (tmp_path / 'VOI123' / 'E100VOI123ZH_00.pdf').is_file()
    assert (tmp_path / 'PIN105' / 'E100PIN105ZH_00.pdf').is_file()
    assert (tmp_path / 'PIN105' / 'A100PIN105ZH_00.pdf').is_file()


def test_files_in_nested_folders(tmp_path):
    files = ['none/A000VOI123ZH_00.pdf',
             'null/E100VOI123ZH_00.pdf',
             'nil/test/aha/E100PIN105ZH_00.pdf',
             'A100PIN105ZH_00.pdf',
             ]

    paths = [tmp_path / f for f in files]
    for p in paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()

    main(*rf'....(......).....\.pdf -i {tmp_path} -o {tmp_path}'.split())

    for p in paths:
        assert not p.is_file()

    assert (tmp_path / 'VOI123' / 'A000VOI123ZH_00.pdf').is_file()
    assert (tmp_path / 'VOI123' / 'E100VOI123ZH_00.pdf').is_file()
    assert (tmp_path / 'PIN105' / 'E100PIN105ZH_00.pdf').is_file()
    assert (tmp_path / 'PIN105' / 'A100PIN105ZH_00.pdf').is_file()


def test_rename_file(tmp_path):
    files = ['A000VOI123ZH.00.pdf',
             'E100VOI123ZH.01.pdf',
             'E100PIN105ZH.00.pdf',
             'A100PIN105ZH_00.pdf',
             ]

    paths = [tmp_path / f for f in files]
    for p in paths:
        p.touch()

    main(*rf'(....(......)..).(..\.pdf) -i {tmp_path} -o {tmp_path} -d \2 -f \1_\3 '.split())

    for p in paths:
        assert not p.is_file()

    assert (tmp_path / 'VOI123' / 'A000VOI123ZH_00.pdf').is_file()
    assert (tmp_path / 'VOI123' / 'E100VOI123ZH_01.pdf').is_file()
    assert (tmp_path / 'PIN105' / 'E100PIN105ZH_00.pdf').is_file()
    assert (tmp_path / 'PIN105' / 'A100PIN105ZH_00.pdf').is_file()


def test_multiple_extensions(tmp_path):
    os.chdir(tmp_path)

    files = ['A000VOI123ZH_00.doc',
             'E100VOI123ZH_00.pdf',
             'E100PIN105ZH_00.docx',
             'A100PIN105ZH_00.pdf',
             ]

    paths = [Path(f) for f in files]
    for p in paths:
        p.touch()

    main(*rf'....(......).....\.(pdf|docx)'.split())

    assert Path('A000VOI123ZH_00.doc').is_file()
    assert not Path('E100VOI123ZH_00.pdf').is_file()
    assert not Path('E100PIN105ZH_00.docx').is_file()
    assert not Path('A100PIN105ZH_00.pdf').is_file()

    assert not Path('VOI123/A000VOI123ZH_00.doc').exists()
    assert Path('VOI123/E100VOI123ZH_00.pdf').is_file()
    assert Path('PIN105/E100PIN105ZH_00.docx').is_file()
    assert Path('PIN105/A100PIN105ZH_00.pdf').is_file()


def test_folders_wont_be_matched(tmp_path):
    os.chdir(tmp_path)

    Path('A000VOI123ZH_00.pdf').touch()
    Path('E100VOI123ZH_00.pdf').touch()
    Path('E100PIN105ZH_00.pdf').mkdir()
    Path('E100PIN105ZH_00.pdf/E100PIN105ZH_00.pdf').touch()
    Path('A100PIN105ZH_00.pdf').mkdir()
    Path('A100PIN105ZH_00.pdf/aaa').touch()
    Path('A100PIN105ZH_00.pdf/bbb').touch()

    main(*rf'....(......).....\.pdf'.split())

    assert not Path('A000VOI123ZH_00.pdf').is_file()
    assert not Path('E100VOI123ZH_00.pdf').is_file()
    assert Path('E100PIN105ZH_00.pdf').is_dir()
    assert not Path('E100PIN105ZH_00.pdf/E100PIN105ZH_00.pdf').is_file()
    assert Path('A100PIN105ZH_00.pdf').is_dir()
    assert Path('A100PIN105ZH_00.pdf/aaa').is_file()
    assert Path('A100PIN105ZH_00.pdf/bbb').is_file()

    assert Path('VOI123/A000VOI123ZH_00.pdf').is_file()
    assert Path('VOI123/E100VOI123ZH_00.pdf').is_file()
    assert Path('PIN105/E100PIN105ZH_00.pdf').is_file()
    assert not Path('PIN105/A100PIN105ZH_00.pdf').exists()


def test_duplicate_files_not_moved(tmp_path):
    os.chdir(tmp_path)

    Path('a').mkdir()
    Path('a/A000VOI123ZH_00.pdf').touch()

    Path('b').mkdir()
    Path('b/A000VOI123ZH_00.pdf').touch()

    main(*rf'....(......).....\.pdf'.split())

    one_file_moved = Path('VOI123/A000VOI123ZH_00.pdf').is_file()
    one_file_not_moved = Path('a/A000VOI123ZH_00.pdf').is_file() or Path('b/A000VOI123ZH_00.pdf').is_file()

    assert one_file_moved and one_file_not_moved
