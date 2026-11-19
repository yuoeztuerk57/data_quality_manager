class TestReport:
    __test__ = False

    def __init__(self):
        self.results = []
        self.duration = 0.0

    def load_results(self, results):
        self.results = results

        self.duration = sum(
            item.get("duration", 0)
            for item in results
        )

    def get_summary(self):
        total = len(self.results)

        passed = sum(
            item["status"] == "PASS"
            for item in self.results
        )

        failed = sum(
            item["status"] == "FAIL"
            for item in self.results
        )

        skipped = sum(
            item["status"] == "SKIPPED"
            for item in self.results
        )

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration": round(self.duration, 3),
            "status": "FAILED" if failed else "PASSED"
        }
        