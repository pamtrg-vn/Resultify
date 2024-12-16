import unittest
from resultify import IRResult  

class TestResult(unittest.TestCase):

    def test_success_creation(self):
        result = IRResult.success(42)
        self.assertTrue(result.is_success())
        self.assertEqual(result.value, 42)
        self.assertIsNone(result.error)

    def test_error_creation(self):
        error = ValueError("An error occurred")
        result = IRResult.error(error)
        self.assertTrue(result.is_error())
        self.assertIsNone(result.value)
        self.assertEqual(result.error, error)

    def test_map_success(self):
        result = IRResult.success(10)
        mapped_result = result.map(lambda x: x * 2)
        self.assertTrue(mapped_result.is_success())
        self.assertEqual(mapped_result.value, 20)

    def test_map_failure(self):
        error = ValueError("An error occurred")
        result = IRResult.error(error)
        mapped_result = result.map(lambda x: x * 2)
        self.assertTrue(mapped_result.is_error())
        self.assertEqual(mapped_result.error, error)

    def test_map_err_success(self):
        result = IRResult.success(10)
        mapped_result = result.map_err(lambda e: str(e))
        self.assertTrue(mapped_result.is_success())
        self.assertEqual(mapped_result.value, 10)

    def test_map_err_failure(self):
        error = ValueError("An error occurred")
        result = IRResult.error(error)
        mapped_result = result.map_err(lambda e: str(e))
        self.assertTrue(mapped_result.is_error())
        self.assertEqual(mapped_result.error, "An error occurred")

    def test_and_then_success(self):
        result = IRResult.success(10)
        chained_result = result.and_then(lambda x: IRResult.success(x + 5))
        self.assertTrue(chained_result.is_success())
        self.assertEqual(chained_result.value, 15)

    def test_and_then_failure(self):
        error = ValueError("An error occurred")
        result = IRResult.error(error)
        chained_result = result.and_then(lambda x: IRResult.success(x + 5))
        self.assertTrue(chained_result.is_error())
        self.assertEqual(chained_result.error, error)

    def test_or_else_success(self):
        result = IRResult.success(10)
        fallback_result = result.or_else(lambda e: IRResult.success(20))
        self.assertTrue(fallback_result.is_success())
        self.assertEqual(fallback_result.value, 10)

    def test_or_else_failure(self):
        error = ValueError("An error occurred")
        result = IRResult.error(error)
        fallback_result = result.or_else(lambda e: IRResult.success(20))
        self.assertTrue(fallback_result.is_success())
        self.assertEqual(fallback_result.value, 20)

    def test_unwrap_success(self):
        result = IRResult.success(42)
        value = result.unwrap()
        self.assertEqual(value, 42)

    def test_unwrap_error(self):
        error = ValueError("An error occurred")
        result = IRResult.error(error)
        with self.assertRaises(ValueError):
            result.unwrap()

    def test_unwrap_or(self):
        result_success = IRResult.success(42)
        self.assertEqual(result_success.unwrap_or(0), 42)
        
        result_error = IRResult.error(ValueError("An error occurred"))
        self.assertEqual(result_error.unwrap_or(0), 0)

    def test_unwrap_or_else(self):
        result_success = IRResult.success(42)
        self.assertEqual(result_success.unwrap_or_else(lambda: 0), 42)
        
        result_error = IRResult.error(ValueError("An error occurred"))
        self.assertEqual(result_error.unwrap_or_else(lambda: 0), 0)


if __name__ == "__main__":
    unittest.main()
