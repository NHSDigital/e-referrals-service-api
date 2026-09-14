#!/usr/bin/env python3
"""
resolve_example_refs.py

Reads a bundled OpenAPI spec on stdin and resolves any remaining $ref
objects found inside example 'value' fields. This is needed because
Redocly CLI v2 no longer dereferences $ref inside example values
during bundling.

The script walks the entire spec looking for objects of the form:
    {"$ref": "some/path/to/file.json"}

that appear inside example value contexts, loads the referenced JSON
file from disk relative to the specification directory, and replaces
the $ref object with the actual file content.

Prints the resolved spec on stdout.
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SPEC_COMPONENTS_DIR = os.path.join(REPO_ROOT, "specification", "components")


def resolve_ref_path(ref_path):
    """
    Resolve a relative $ref path from the bundled output to an
    absolute file path on disk.

    In the source YAML, $refs are relative to the file they appear in:
    - From schemas/endpoints/:  ../../examples/...  (up 2 = stu3/)
    - From schemas/responses/:  ../../../examples/... (up 3 = stu3/)

    All paths contain 'examples/' which maps to
    specification/components/{stu3,r4}/examples/.

    We extract the part starting from 'examples/' and look for it
    under both stu3 and r4 component directories.
    """
    # Find the 'examples/' segment in the path
    examples_idx = ref_path.find("examples/")
    if examples_idx == -1:
        return None

    relative_from_examples = ref_path[examples_idx:]

    # Try both stu3 and r4 directories
    for subdir in ["stu3", "r4"]:
        candidate = os.path.join(SPEC_COMPONENTS_DIR, subdir, relative_from_examples)
        if os.path.isfile(candidate):
            return candidate

    return None


def resolve_refs(obj):
    """
    Recursively walk the parsed JSON object. When we find a dict that
    is exactly {"$ref": "<path>"} where the path points to a .json
    file, load that file and return its content instead.
    """
    if isinstance(obj, dict):
        if list(obj.keys()) == ["$ref"] and obj["$ref"].endswith(".json"):
            ref_path = obj["$ref"]
            abs_path = resolve_ref_path(ref_path)
            if abs_path:
                with open(abs_path, "r") as f:
                    return json.load(f)
            else:
                print(
                    f"Warning: Could not resolve $ref: {ref_path}",
                    file=sys.stderr,
                )
                return obj
        else:
            return {k: resolve_refs(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_refs(item) for item in obj]
    else:
        return obj


def main():
    """Main entrypoint"""
    data = json.loads(sys.stdin.read())
    resolved = resolve_refs(data)
    sys.stdout.write(json.dumps(resolved, indent=2))
    sys.stdout.close()


if __name__ == "__main__":
    main()
