from pathlib import Path
from ahis.evidence import digest_json, write_manifest, verify_manifest


def test_json_digest_is_order_independent():
    assert digest_json({"a":1,"b":2}) == digest_json({"b":2,"a":1})


def test_manifest_round_trip(tmp_path: Path):
    (tmp_path/"a.txt").write_text("a")
    (tmp_path/"b.txt").write_text("b")
    write_manifest(tmp_path,tmp_path/"MANIFEST.sha256")
    assert verify_manifest(tmp_path,tmp_path/"MANIFEST.sha256") == ()


def test_manifest_detects_mutation(tmp_path: Path):
    (tmp_path/"a.txt").write_text("a")
    write_manifest(tmp_path,tmp_path/"MANIFEST.sha256")
    (tmp_path/"a.txt").write_text("x")
    assert verify_manifest(tmp_path,tmp_path/"MANIFEST.sha256")

def test_manifest_detects_unmanifested_file(tmp_path: Path):
    (tmp_path/"a.txt").write_text("a")
    write_manifest(tmp_path,tmp_path/"MANIFEST.sha256")
    (tmp_path/"b.txt").write_text("b")
    assert "unmanifested file: b.txt" in verify_manifest(tmp_path,tmp_path/"MANIFEST.sha256")
