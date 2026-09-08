#!/usr/bin/env python3
"""Audit a workshop PPTX against the EquipGTM presentation preferences.

Adapted from the user's Tech Presentations audit_pptx.py.
This catches structural problems and flags wording for review. It does not replace full-size visual
inspection or native PowerPoint playback.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import struct
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "adec": "http://schemas.microsoft.com/office/drawing/2017/decorative",
}
EMU_PER_INCH = 914400

JARGON_PATTERNS = {
    "delve": r"\bdelve\b",
    "foster": r"\bfoster(?:s|ed|ing)?\b",
    "leverage": r"\bleverag(?:e|es|ed|ing)\b",
    "utilize": r"\butiliz(?:e|es|ed|ing)\b",
    "facilitate": r"\bfacilitat(?:e|es|ed|ing)\b",
    "empower": r"\bempower(?:s|ed|ing)?\b",
    "streamline": r"\bstreamlin(?:e|es|ed|ing)\b",
    "robust": r"\brobust\b",
    "cutting-edge": r"\bcutting[- ]edge\b",
    "paradigm shift": r"\bparadigm shift\b",
    "game changer": r"\bgame[- ]changer\b",
    "transformative": r"\btransformative\b",
    "elevate": r"\belevat(?:e|es|ed|ing)\b",
    "supercharge": r"\bsupercharg(?:e|es|ed|ing)\b",
    "ever-evolving": r"\bever[- ]evolving\b",
    "at its core": r"\bat its core\b",
    "in today's world": r"\bin today['’]s world\b",
    "in the age of": r"\bin the age of\b",
    "it's worth noting": r"\bit['’]s worth noting\b",
    "not just": r"\bnot just\b",
    "this is not": r"\bthis is not\b",
    "taste chooses": r"\btaste chooses\b",
    "judgment ships": r"\bjudg(?:e)?ment ships\b",
    "rules/transforms/checks": r"rules\s*[·•|/]\s*transforms\s*[·•|/]\s*checks",
    "bounded interpretation": r"\bbounded interpretation\b",
    "room supplies": r"\bthe room supplies\b",
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    slide: int | None = None


def xml_text(node: ET.Element) -> str:
    return " ".join((item.text or "").strip() for item in node.findall(".//a:t", NS) if (item.text or "").strip())


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def parse_slide_set(value: str) -> set[int]:
    result: set[int] = set()
    if not value:
        return result
    for part in value.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start, end = int(start_text), int(end_text)
            if end < start:
                raise argparse.ArgumentTypeError(f"Invalid slide range: {token}")
            result.update(range(start, end + 1))
        else:
            result.add(int(token))
    if any(number < 1 for number in result):
        raise argparse.ArgumentTypeError("Slide numbers must be positive")
    return result


def relationship_map(archive: zipfile.ZipFile, slide_path: str) -> dict[str, str]:
    rel_path = posixpath.join(posixpath.dirname(slide_path), "_rels", posixpath.basename(slide_path) + ".rels")
    if rel_path not in archive.namelist():
        return {}
    root = ET.fromstring(archive.read(rel_path))
    mapping: dict[str, str] = {}
    for rel in root.findall("pr:Relationship", NS):
        rel_id = rel.get("Id")
        target = rel.get("Target")
        if not rel_id or not target:
            continue
        if target.startswith("/"):
            resolved = target.lstrip("/")
        else:
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(slide_path), target))
        mapping[rel_id] = resolved
    return mapping


def jpeg_size(data: bytes) -> tuple[int, int] | None:
    if not data.startswith(b"\xff\xd8"):
        return None
    i = 2
    sof_markers = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in {0xD8, 0xD9}:
            continue
        if i + 2 > len(data):
            break
        segment_length = struct.unpack(">H", data[i : i + 2])[0]
        if segment_length < 2 or i + segment_length > len(data):
            break
        if marker in sof_markers and segment_length >= 7:
            height = struct.unpack(">H", data[i + 3 : i + 5])[0]
            width = struct.unpack(">H", data[i + 5 : i + 7])[0]
            return width, height
        i += segment_length
    return None


def image_size(data: bytes) -> tuple[int, int] | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:6] in {b"GIF87a", b"GIF89a"} and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if data.startswith(b"BM") and len(data) >= 26:
        width, height = struct.unpack("<ii", data[18:26])
        return abs(width), abs(height)
    return jpeg_size(data)


def is_decorative(pic: ET.Element) -> bool:
    return any(node.get("val") in {None, "1", "true"} for node in pic.findall(".//adec:decorative", NS))


def title_from_slide(root: ET.Element) -> str | None:
    for shape in root.findall(".//p:sp", NS):
        placeholder = shape.find("./p:nvSpPr/p:nvPr/p:ph", NS)
        if placeholder is not None and placeholder.get("type") in {"title", "ctrTitle"}:
            title = xml_text(shape).strip()
            return title or None
    return None


def crop_fraction(pic: ET.Element, side: str) -> float:
    src = pic.find("./p:blipFill/a:srcRect", NS)
    if src is None:
        return 0.0
    try:
        return max(0.0, min(1.0, int(src.get(side, "0")) / 100000.0))
    except ValueError:
        return 0.0


def click_entrance_targets(root: ET.Element) -> tuple[set[str], set[str]]:
    """Find declared click entrance targets, not proof of correct playback.

    A transition or empty timing tree must not count as a content reveal. Native
    entrance effects use presetClass="entr" and a clickEffect timing node; the
    shape target must exist on the slide. Grouped effects may inherit the click
    node from an ancestor. Initial visibility and timing order require playback.
    """
    timing = root.find("p:timing", NS)
    if timing is None:
        return set(), set()
    shape_ids = {node.get("id") for node in root.findall(".//p:cNvPr", NS)}
    parents = {child: parent for parent in timing.iter() for child in parent}
    targets: set[str] = set()
    invalid: set[str] = set()
    for effect in timing.findall(".//p:cTn[@presetClass='entr']", NS):
        node: ET.Element | None = effect
        on_click = False
        while node is not None:
            if node.get("nodeType") == "clickEffect":
                on_click = True
                break
            node = parents.get(node)
        if not on_click:
            continue
        for target in effect.findall(".//p:spTgt", NS):
            shape_id = target.get("spid", "")
            if shape_id and shape_id in shape_ids:
                targets.add(shape_id)
            else:
                invalid.add(shape_id or "(missing)")
    return targets, invalid


def audit(args: argparse.Namespace) -> tuple[dict, list[Finding]]:
    deck = Path(args.deck).expanduser().resolve()
    findings: list[Finding] = []
    if not deck.exists():
        return {"deck": str(deck)}, [Finding("error", "file-missing", f"Deck does not exist: {deck}")]

    allowed_over = args.allow_over
    required_reveals = args.require_reveals
    allowed_jargon = {item.casefold() for item in args.allow_jargon}
    stats = {
        "deck": str(deck),
        "slides": 0,
        "notes": 0,
        "slides_with_sources": 0,
        "slides_with_titles": 0,
        "slides_with_transitions": 0,
        "slides_with_timing": 0,
        "slides_with_click_entrances": 0,
        "click_entrance_targets": 0,
        "pictures": 0,
        "pictures_with_alt_or_decorative": 0,
        "max_visible_words": 0,
        "max_visible_words_slide": None,
        "slides_with_picture_or_chart": 0,
        "minimum_effective_image_ppi": None,
    }

    try:
        archive = zipfile.ZipFile(deck)
    except zipfile.BadZipFile:
        return stats, [Finding("error", "bad-package", "File is not a valid PPTX ZIP package")]

    with archive:
        broken = archive.testzip()
        if broken:
            findings.append(Finding("error", "zip-integrity", f"Corrupt package entry: {broken}"))

        names = set(archive.namelist())
        # Presentation order and notes relationships need not match file suffixes.
        # Slide numbers reported below are the positions the audience will see.
        presentation_path = "ppt/presentation.xml"
        if presentation_path not in names:
            return stats, [Finding("error", "missing-presentation", "Package has no presentation.xml")]
        presentation = ET.fromstring(archive.read(presentation_path))
        presentation_rels = relationship_map(archive, presentation_path)
        slides = []
        for item in presentation.findall("./p:sldIdLst/p:sldId", NS):
            rel_id = item.get(f"{{{NS['r']}}}id", "")
            slide_path = presentation_rels.get(rel_id)
            if not slide_path or slide_path not in names:
                findings.append(Finding("error", "broken-slide-rel", "Presentation references a missing slide"))
                continue
            slides.append(slide_path)
        stats["slides"] = len(slides)

        missing_reveal_slides = required_reveals - set(range(1, len(slides) + 1))
        for slide_number in sorted(missing_reveal_slides):
            findings.append(Finding("error", "reveal-slide-missing", "Required reveal slide does not exist", slide_number))

        if not slides:
            findings.append(Finding("error", "no-slides", "No slides found in the package"))
            return stats, findings

        seen_titles: dict[str, int] = {}
        minimum_ppi: float | None = None

        for slide_number, slide_path in enumerate(slides, start=1):
            root = ET.fromstring(archive.read(slide_path))
            text = xml_text(root)
            count = word_count(text)
            if count > stats["max_visible_words"]:
                stats["max_visible_words"] = count
                stats["max_visible_words_slide"] = slide_number
            if count > args.max_words and slide_number not in allowed_over:
                findings.append(
                    Finding(
                        "error",
                        "word-limit",
                        f"{count} visible words exceeds the {args.max_words}-word house limit",
                        slide_number,
                    )
                )

            title = title_from_slide(root)
            if not title:
                findings.append(Finding("error", "missing-title", "Missing semantic title placeholder", slide_number))
            else:
                stats["slides_with_titles"] += 1
                key = re.sub(r"\s+", " ", title.strip()).casefold()
                if key in seen_titles:
                    findings.append(
                        Finding(
                            "error",
                            "duplicate-title",
                            f"Semantic title duplicates slide {seen_titles[key]}: {title!r}",
                            slide_number,
                        )
                    )
                else:
                    seen_titles[key] = slide_number

            for label, pattern in JARGON_PATTERNS.items():
                if label.casefold() in allowed_jargon:
                    continue
                if re.search(pattern, text, flags=re.IGNORECASE):
                    findings.append(Finding("warning", "wording-review", f"Review phrase in context: {label!r}", slide_number))

            has_transition = root.find("p:transition", NS) is not None
            has_timing = root.find("p:timing", NS) is not None
            stats["slides_with_transitions"] += int(has_transition)
            stats["slides_with_timing"] += int(has_timing)
            reveal_targets, invalid_targets = click_entrance_targets(root)
            stats["slides_with_click_entrances"] += int(bool(reveal_targets))
            stats["click_entrance_targets"] += len(reveal_targets)
            if invalid_targets:
                findings.append(
                    Finding("error", "broken-reveal-target", f"Click entrance effects reference missing shapes: {', '.join(sorted(invalid_targets))}", slide_number)
                )
            if slide_number in required_reveals and not reveal_targets:
                findings.append(
                    Finding(
                        "error",
                        "missing-click-reveal",
                        "No click entrance effect targets an existing shape; slide transitions and timing elements alone do not reveal content",
                        slide_number,
                    )
                )

            pics = root.findall(".//p:pic", NS)
            graphic_frames = root.findall(".//p:graphicFrame", NS)
            stats["pictures"] += len(pics)
            if pics or graphic_frames:
                stats["slides_with_picture_or_chart"] += 1
            elif count > 20:
                findings.append(
                    Finding(
                        "warning",
                        "text-only",
                        "Text-heavy slide has no embedded picture or chart; confirm that the visual treatment is intentional",
                        slide_number,
                    )
                )

            rels = relationship_map(archive, slide_path)
            for pic in pics:
                c_nv_pr = pic.find("./p:nvPicPr/p:cNvPr", NS)
                description = "" if c_nv_pr is None else (c_nv_pr.get("descr") or c_nv_pr.get("title") or "").strip()
                if description or is_decorative(pic):
                    stats["pictures_with_alt_or_decorative"] += 1
                else:
                    name = "image" if c_nv_pr is None else c_nv_pr.get("name", "image")
                    findings.append(Finding("error", "missing-alt", f"Picture {name!r} lacks alt text and is not marked decorative", slide_number))

                blip = pic.find("./p:blipFill/a:blip", NS)
                rel_id = None if blip is None else blip.get(f"{{{NS['r']}}}embed")
                if not rel_id or rel_id not in rels:
                    findings.append(Finding("error", "broken-image-rel", "Picture has no resolvable media relationship", slide_number))
                    continue
                media_path = rels[rel_id]
                if media_path not in names:
                    findings.append(Finding("error", "missing-media", f"Missing embedded media: {media_path}", slide_number))
                    continue
                dimensions = image_size(archive.read(media_path))
                if dimensions is None:
                    findings.append(Finding("warning", "image-size-unknown", f"Could not read pixel dimensions for {media_path}", slide_number))
                    continue
                extent = pic.find("./p:spPr/a:xfrm/a:ext", NS)
                if extent is None:
                    continue
                try:
                    width_in = int(extent.get("cx", "0")) / EMU_PER_INCH
                    height_in = int(extent.get("cy", "0")) / EMU_PER_INCH
                except ValueError:
                    continue
                if width_in <= 0 or height_in <= 0:
                    continue
                left = crop_fraction(pic, "l")
                right = crop_fraction(pic, "r")
                top = crop_fraction(pic, "t")
                bottom = crop_fraction(pic, "b")
                used_width = dimensions[0] * max(0.01, 1.0 - left - right)
                used_height = dimensions[1] * max(0.01, 1.0 - top - bottom)
                effective_ppi = min(used_width / width_in, used_height / height_in)
                minimum_ppi = effective_ppi if minimum_ppi is None else min(minimum_ppi, effective_ppi)
                if effective_ppi < args.min_image_ppi:
                    findings.append(
                        Finding(
                            "error",
                            "low-image-resolution",
                            f"Effective image resolution is about {effective_ppi:.0f} PPI; minimum is {args.min_image_ppi:.0f}",
                            slide_number,
                        )
                    )
                elif effective_ppi < args.preferred_image_ppi:
                    findings.append(
                        Finding(
                            "warning",
                            "image-resolution",
                            f"Effective image resolution is about {effective_ppi:.0f} PPI; inspect at full size",
                            slide_number,
                        )
                    )

            note_path = next((path for path in rels.values()
                              if path.startswith("ppt/notesSlides/") and path in names), None)
            if not note_path:
                findings.append(Finding("error", "missing-notes", "Missing speaker notes", slide_number))
            else:
                stats["notes"] += 1
                note_text = xml_text(ET.fromstring(archive.read(note_path)))
                if "[Sources]" in note_text and "[/Sources]" in note_text:
                    stats["slides_with_sources"] += 1
                else:
                    findings.append(Finding("error", "missing-sources", "Speaker notes lack a complete [Sources] block", slide_number))

        stats["minimum_effective_image_ppi"] = None if minimum_ppi is None else round(minimum_ppi, 1)

    return stats, findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit a workshop PPTX against the EquipGTM presentation preferences.")
    parser.add_argument("deck", help="Path to the .pptx file")
    parser.add_argument("--max-words", type=int, default=40, help="Maximum visible words per slide (default: 40)")
    parser.add_argument("--allow-over", type=parse_slide_set, default=set(), help="Comma-separated slides or ranges allowed over the word limit")
    parser.add_argument("--allow-jargon", action="append", default=[], help="Allow one named jargon label from the built-in list")
    parser.add_argument("--require-reveals", type=parse_slide_set, default=set(), help="Slides or ranges that require native click entrance targets, e.g. 3,5-7; playback must still be inspected")
    parser.add_argument("--min-image-ppi", type=float, default=100.0, help="Minimum effective image PPI (default: 100)")
    parser.add_argument("--preferred-image-ppi", type=float, default=150.0, help="Preferred image PPI; lower values warn (default: 150)")
    parser.add_argument("--json", action="store_true", help="Write machine-readable JSON")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.max_words < 1:
        parser.error("--max-words must be positive")
    if args.min_image_ppi < 1 or args.preferred_image_ppi < args.min_image_ppi:
        parser.error("Image PPI thresholds are invalid")
    try:
        stats, findings = audit(args)
    except (ET.ParseError, OSError, RuntimeError, KeyError) as error:
        stats = {"deck": str(Path(args.deck).expanduser().resolve())}
        findings = [Finding("error", "unreadable-package", f"Could not inspect package: {error}")]
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]

    if args.json:
        print(json.dumps({"stats": stats, "findings": [asdict(item) for item in findings]}, indent=2))
    else:
        status = "PASS" if not errors else "FAIL"
        print(f"EquipGTM presentation audit: {status}")
        print(f"Deck: {stats.get('deck')}")
        print(
            "Summary: "
            f"{stats.get('slides', 0)} slides; "
            f"max {stats.get('max_visible_words', 0)} visible words on slide {stats.get('max_visible_words_slide')}; "
            f"{stats.get('slides_with_titles', 0)} titles; "
            f"{stats.get('slides_with_sources', 0)} source blocks; "
            f"{stats.get('pictures_with_alt_or_decorative', 0)}/{stats.get('pictures', 0)} pictures described or decorative"
        )
        if stats.get("minimum_effective_image_ppi") is not None:
            print(f"Minimum effective image resolution: {stats['minimum_effective_image_ppi']} PPI")
        print(
            "Animation structure: "
            f"{stats.get('slides_with_transitions', 0)} slides with transitions; "
            f"{stats.get('slides_with_timing', 0)} with timing; "
            f"{stats.get('slides_with_click_entrances', 0)} with declared click entrances "
            f"targeting {stats.get('click_entrance_targets', 0)} shapes"
        )
        for item in findings:
            location = f" slide {item.slide}" if item.slide is not None else ""
            print(f"[{item.severity.upper()}]{location} {item.code}: {item.message}")
        print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s)")
        print("Reminder: this script cannot approve crops, composition, story, or native PowerPoint playback.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
