from log_analyzer import analyze_log
from ai_engine import diagnose_with_groq, generate_fix
from fix_applier import apply_fix
from git_autofix import commit_and_push

import re


def main():

    print("=" * 60)
    print("        DVPS40 - AUTONOMOUS AUTO-FIXING DEVOPS BOT")
    print("=" * 60)

    print("\nPaste your deployment/server error below.")
    print("Type END on a new line when finished.\n")

    lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    log = "\n".join(lines)

    if not log.strip():
        print("\nNo log provided.")
        return

    # --------------------------------------------------
    # STEP 1 - LOCAL ERROR ANALYSIS
    # --------------------------------------------------

    print("\n[1/5] Analyzing error...")

    try:

        result = analyze_log(log)

        print("\n--- ERROR ANALYSIS ---")
        print("Error Type  :", result["error_type"])
        print("Message     :", result["message"])
        print("Likely Cause:", result["likely_cause"])
        print("Severity    :", result["severity"])

    except Exception as e:

        print("\nLocal log analysis failed.")
        print("Error:", e)
        return

    # --------------------------------------------------
    # STEP 2 - GROQ AI DIAGNOSIS
    # --------------------------------------------------

    print("\n[2/5] Asking Groq AI to diagnose the problem...")

    try:

        groq_result = diagnose_with_groq(log)

        print("\n--- GROQ AI DIAGNOSIS ---")
        print(groq_result)

    except Exception as e:

        print("\nGroq AI diagnosis failed.")
        print("Error:", e)
        return

    # --------------------------------------------------
    # STEP 3 - AI FIX GENERATION
    # --------------------------------------------------

    print("\n[3/5] Generating AI fix...")

    try:

        fix_result = generate_fix(log, groq_result)

        print("\n--- AI FIX GENERATED ---")
        print(fix_result)

    except Exception as e:

        print("\nAI fix generation failed.")
        print("Error:", e)
        return

    # --------------------------------------------------
    # STEP 4 - APPLY AI FIX
    # --------------------------------------------------

    print("\n[4/5] Applying AI fix...")

    fix_applied = False

    try:

        # Detect missing Python package
        #
        # Example:
        # ModuleNotFoundError: No module named 'requests'

        if "ModuleNotFoundError" in log:

            match = re.search(
                r"No module named ['\"]([^'\"]+)['\"]",
                log
            )

            if match:

                package_name = match.group(1)

                print(
                    f"\nDetected missing package: {package_name}"
                )

                changed = apply_fix(
                    "INSTALL_PACKAGE",
                    package_name
                )

                if changed:

                    fix_applied = True

                    print(
                        f"\nSuccessfully added "
                        f"'{package_name}' to requirements.txt"
                    )

                else:

                    print(
                        "\nPackage already exists."
                    )

            else:

                print(
                    "\nCould not identify the missing package."
                )

        else:

            print(
                "\nNo supported automatic fix detected."
            )

    except Exception as e:

        print("\nAI fix application failed.")
        print("Error:", e)
        return

    # --------------------------------------------------
    # STEP 5 - GITHUB COMMIT & PUSH
    # --------------------------------------------------

    print("\n[5/5] Committing and pushing AI fix to GitHub...")

    if not fix_applied:

        print("\nNo new fix was applied.")
        print("Skipping GitHub commit.")

        print("\n----------------------------------------------")
        print("DVPS40 AUTO-FIX PROCESS")
        print("----------------------------------------------")

        print("✓ Error analyzed")
        print("✓ Groq AI diagnosis completed")
        print("✓ AI fix generated")
        print("✓ Fix analysis completed")
        print("→ No new file changes to commit")

        return

    try:

        branch_name = "dvps40-auto-fix"

        commit_message = (
            "DVPS40: Apply AI-generated auto-fix"
        )

        commit_and_push(
            branch_name,
            commit_message
        )

        print("\n✓ Git commit created")
        print("✓ AI fix pushed to GitHub")
        print(f"✓ Branch: {branch_name}")

    except Exception as e:

        print("\nGitHub auto-fix failed.")
        print("Error:", e)
        return

    # --------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------

    print("\n----------------------------------------------")
    print("DVPS40 AUTO-FIX PROCESS")
    print("----------------------------------------------")

    print("✓ Error analyzed")
    print("✓ Groq AI diagnosis completed")
    print("✓ AI fix generated")
    print("✓ AI fix applied")
    print("✓ Git commit created")
    print("✓ Fix pushed to GitHub")

    print("\n→ Automatic Pull Request coming next")
    print("→ Fix verification coming next")

    print("\nDVPS40 Step 4.3 completed successfully.")


if __name__ == "__main__":
    main()