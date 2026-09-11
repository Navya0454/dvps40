from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"


def apply_package_fix(package_name):
    """
    Add a missing Python package to requirements.txt.
    """

    package_name = package_name.strip()

    if not package_name:
        raise ValueError("Package name is empty.")

    # Create requirements.txt if it doesn't exist
    if not REQUIREMENTS_FILE.exists():
        REQUIREMENTS_FILE.write_text("", encoding="utf-8")

    existing = REQUIREMENTS_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    # Check whether package already exists
    package_exists = False

    for line in existing:
        clean_line = line.strip()

        if not clean_line or clean_line.startswith("#"):
            continue

        installed_name = re.split(
            r"[<>=!~]", clean_line
        )[0].strip()

        if installed_name.lower() == package_name.lower():
            package_exists = True
            break

    if package_exists:
        print(f"\nPackage '{package_name}' already exists.")
        return False

    with REQUIREMENTS_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        if existing and existing[-1].strip():
            file.write("\n")

        file.write(package_name + "\n")

    print(
        f"\nAI FIX APPLIED: Added '{package_name}' "
        f"to requirements.txt"
    )

    return True


def apply_fix(fix_type, package_name=None):

    fix_type = fix_type.strip().upper()

    if fix_type == "INSTALL_PACKAGE":

        if not package_name:
            raise ValueError(
                "INSTALL_PACKAGE requires a package name."
            )

        return apply_package_fix(package_name)

    print(
        f"\nFix type '{fix_type}' is not supported yet."
    )

    return False


if __name__ == "__main__":

    print("=" * 55)
    print("DVPS40 AI FIX APPLIER")
    print("=" * 55)

    try:

        changed = apply_fix(
            "INSTALL_PACKAGE",
            "requests"
        )

        if changed:
            print("\nFix application successful.")
        else:
            print("\nNo changes were required.")

    except Exception as e:

        print("\nFix application failed.")
        print("Error:", e)