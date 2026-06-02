from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


CLASS_STEREOTYPES = [
    "Category",
    "Mixin",
    "PhaseMixin",
    "RoleMixin",
    "Collective",
    "Kind",
    "Mode",
    "Quality",
    "Quantity",
    "Relator",
    "Phase",
    "Role",
    "Subkind",
    "Event",
    "HistoricalRoleMixin",
    "HistoricalRole",
    "Situation",
    "Type",
    "Abstract",
    "Datatype",
    "Enumeration",
]

RELATION_STEREOTYPES = [
    "Characterization",
    "Comparative",
    "ExternalDependence",
    "Material",
    "Mediation",
    "ComponentOf",
    "MemberOf",
    "SubCollectionOf",
    "SubQuantityOf",
    "BringsAbout",
    "Creation",
    "HistoricalDependence",
    "Manifestation",
    "Participation",
    "Participational",
    "Termination",
    "Triggers",
    "Instantiation",
]


def to_kebab_case(name: str) -> str:
    """Convert OntoUML stereotype names to stable Markdown filenames."""
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", name)
    name = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "-", name)
    return name.lower()


def write_file(path: Path, content: str, overwrite: bool) -> bool:
    """Write a file if missing, or overwrite when requested."""
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and not overwrite:
        return False

    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def stereotype_page_template(
    *,
    name: str,
    stereotype_group: str,
    agent: str,
    action_date: str,
) -> str:
    return f"""# {name}

## Description

## Stereotype Profile

## Examples

## References

### Direct Citations

### Consulted Sources

## Generation and Review Log

"""


def card(name: str, relative_path: str, group_label: str) -> str:
    return f"""-   **{name}**

    {group_label} stereotype placeholder.

    [Open page]({relative_path})
"""


def index_page_template() -> str:
    class_cards = "\n".join(
        card(
            name=name,
            relative_path=f"classes/{to_kebab_case(name)}.md",
            group_label="Class",
        )
        for name in CLASS_STEREOTYPES
    )

    relation_cards = "\n".join(
        card(
            name=name,
            relative_path=f"relations/{to_kebab_case(name)}.md",
            group_label="Relation",
        )
        for name in RELATION_STEREOTYPES
    )

    return f"""# OntoUML Stereotypes

This section contains placeholder pages for OntoUML stereotypes available in the OntoUML VP plugin.

## Class Stereotypes

<div class="grid cards" markdown>

{class_cards}

</div>

## Relation Stereotypes

<div class="grid cards" markdown>

{relation_cards}

</div>
"""


def group_index_page_template(
    *,
    title: str,
    description: str,
    stereotypes: list[str],
    folder_name: str,
    group_label: str,
) -> str:
    cards = "\n".join(
        card(
            name=name,
            relative_path=f"{to_kebab_case(name)}.md",
            group_label=group_label,
        )
        for name in stereotypes
    )

    return f"""# {title}

{description}

<div class="grid cards" markdown>

{cards}

</div>
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create placeholder MkDocs pages for OntoUML VP plugin stereotypes."
    )
    parser.add_argument(
        "--docs-dir",
        default="docs",
        help="Path to the MkDocs docs directory. Default: docs",
    )
    parser.add_argument(
        "--agent",
        default="GPT-5.5 Thinking",
        help="Agent name/version to record in the generation log.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing Markdown files.",
    )

    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    stereotypes_dir = docs_dir / "stereotypes"
    class_dir = stereotypes_dir / "classes"
    relation_dir = stereotypes_dir / "relations"
    action_date = date.today().isoformat()

    created = []
    skipped = []

    files = {
        stereotypes_dir / "index.md": index_page_template(),
        class_dir / "index.md": group_index_page_template(
            title="Class Stereotypes",
            description="This section contains placeholder pages for OntoUML class stereotypes.",
            stereotypes=CLASS_STEREOTYPES,
            folder_name="classes",
            group_label="Class",
        ),
        relation_dir / "index.md": group_index_page_template(
            title="Relation Stereotypes",
            description="This section contains placeholder pages for OntoUML relation stereotypes.",
            stereotypes=RELATION_STEREOTYPES,
            folder_name="relations",
            group_label="Relation",
        ),
    }

    for name in CLASS_STEREOTYPES:
        files[class_dir / f"{to_kebab_case(name)}.md"] = stereotype_page_template(
            name=name,
            stereotype_group="Class",
            agent=args.agent,
            action_date=action_date,
        )

    for name in RELATION_STEREOTYPES:
        files[relation_dir / f"{to_kebab_case(name)}.md"] = stereotype_page_template(
            name=name,
            stereotype_group="Relation",
            agent=args.agent,
            action_date=action_date,
        )

    for path, content in files.items():
        was_written = write_file(path, content, overwrite=args.overwrite)
        if was_written:
            created.append(path)
        else:
            skipped.append(path)

    print(f"Created or updated: {len(created)} file(s)")
    print(f"Skipped existing: {len(skipped)} file(s)")

    if skipped:
        print("\nSkipped files:")
        for path in skipped:
            print(f"  - {path}")


if __name__ == "__main__":
    main()