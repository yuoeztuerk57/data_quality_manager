import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from pathlib import Path


class TestRunner:
    __test__ = False

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent

    def run_tests(self, test_path=None):

        with tempfile.TemporaryDirectory() as temp_dir:

            xml_path = Path(temp_dir) / "test_results.xml"

            command = [
                sys.executable,
                "-m",
                "pytest",
                "-v",
                "--tb=short",
                f"--junitxml={xml_path}"
            ]

            if test_path:
                command.append(str(test_path))

            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True
            )

            results = []

            if xml_path.exists():
                root = ET.parse(xml_path).getroot()

                for case in root.iter("testcase"):

                    status = "PASS"
                    message = ""

                    failure = case.find("failure")
                    error = case.find("error")
                    skipped = case.find("skipped")

                    if failure is not None or error is not None:
                        status = "FAIL"
                        message = (
                            failure.get("message", "")
                            if failure is not None
                            else error.get("message", "")
                        )

                    elif skipped is not None:
                        status = "SKIPPED"
                        message = skipped.get("message", "")

                    results.append({
                        "test": case.get("name", ""),
                        "module": case.get("classname", ""),
                        "status": status,
                        "message": message,
                        "duration": float(case.get("time", 0))
                    })

            return {
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "results": results
            }