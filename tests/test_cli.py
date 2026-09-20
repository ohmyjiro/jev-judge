import io
import json
import runpy
import unittest
from pathlib import Path


cli = runpy.run_path(str(Path(__file__).resolve().parents[1] / "bin/jev-judge"))
validate = cli["validate"]
evaluate = cli["evaluate"]


class JevJudgeTests(unittest.TestCase):
    def setUp(self):
        self.request = {
            "state": "private evidence that must not appear in output",
            "questions": {"relevant": {"type": "noul", "instructions": "Is this relevant?"}},
        }

    def test_validates_question_contract_before_network(self):
        self.assertIn(b"jev-latest", validate(self.request))
        invalid = {**self.request, "questions": {"topic": {"type": "choice", "instructions": "Pick", "criteria": {"only": None}}}}
        with self.assertRaisesRegex(ValueError, "2-255 options"):
            validate(invalid)
        with self.assertRaisesRegex(ValueError, "state"):
            validate({**self.request, "state": None})

    def test_sends_key_but_returns_only_answers_and_metrics(self):
        response = {"model": "jev-test", "answers": {"relevant": {"type": "noul", "noul": 0.8}}, "usage": {"input_tokens": 10, "output_tokens": 2}}
        observed = {}

        def opener(http, timeout):
            observed["key"] = http.get_header("Authorization")
            observed["timeout"] = timeout
            observed["request"] = json.loads(http.data)
            return io.BytesIO(json.dumps(response).encode())

        result = evaluate(self.request, "test-key", opener=opener)
        self.assertEqual(observed["key"], "Bearer test-key")
        self.assertEqual(observed["timeout"], 15)
        self.assertEqual(observed["request"]["state"], self.request["state"])
        self.assertEqual(result["answers"], response["answers"])
        self.assertNotIn(self.request["state"], json.dumps(result))
        self.assertNotIn("test-key", json.dumps(result))

    def test_rejects_missing_or_mismatched_answers(self):
        def opener(http, timeout):
            return io.BytesIO(b'{"answers":{"wrong":{"type":"noul","noul":0.5}}}')

        with self.assertRaisesRegex(ValueError, "different question IDs"):
            evaluate(self.request, "test-key", opener=opener)
        with self.assertRaisesRegex(ValueError, "TYPESAFE_API_KEY"):
            evaluate(self.request, "", opener=opener)


if __name__ == "__main__":
    unittest.main()
