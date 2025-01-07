import unittest
from sci_cases import cases_query, get_judgement

class TestSCICases(unittest.TestCase):
    
    def test_cases_query(self):
        data = cases_query(cause_title="union of india", page="1")
        self.assertIsInstance(data, dict)
    
    def test_get_judgement(self):
        # Replace with an actual judgment ID for testing
        judgement = get_judgement("MzEzODA=")
        self.assertIsInstance(judgement, str)

if __name__ == "__main__":
    unittest.main()