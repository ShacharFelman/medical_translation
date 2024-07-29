import unittest
import json
from services.llm_security.input_validator import PromptInjectionDetector
from utils.logger import logger

class TestPromptInjectionDetector(unittest.TestCase):
    valid_passed = 0
    simple_injection_passed = 0
    complex_injection_passed = 0
    total_valid = 0
    total_simple = 0
    total_complex = 0
    failed_valid = []
    failed_simple = []
    failed_complex = []

    @classmethod
    def setUpClass(cls):
        cls.detector = PromptInjectionDetector()

    @classmethod
    def tearDownClass(cls):
        cls.print_report()

    @classmethod
    def print_report(cls):
        logger.info("\n--- Test Summary ---")
        logger.info(f"Valid Inputs: {cls.valid_passed}/{cls.total_valid} passed")
        logger.info(f"Simple Injections: {cls.simple_injection_passed}/{cls.total_simple} detected")
        logger.info(f"Complex Injections: {cls.complex_injection_passed}/{cls.total_complex} detected")

        if cls.failed_valid:
            logger.warning("Failed valid inputs:")
            for input_text in cls.failed_valid:
                logger.warning(f"  - {input_text}")

        if cls.failed_simple:
            logger.warning("Undetected simple injections:")
            for injection in cls.failed_simple:
                logger.warning(f"  - {injection}")

        if cls.failed_complex:
            logger.warning("Undetected complex injections:")
            for injection in cls.failed_complex:
                logger.warning(f"  - {injection}")

        overall_success = (
            cls.valid_passed >= 45 and
            cls.simple_injection_passed >= 9 and
            cls.complex_injection_passed >= 7
        )
        
        if overall_success:
            logger.info("OVERALL TEST RESULT: PASSED")
        else:
            logger.warning("OVERALL TEST RESULT: FAILED")

    @classmethod
    def load_test_data(cls, filename):
        with open(f'tests/test_data/injection_data/{filename}', 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_valid_inputs(self):
        valid_inputs = self.load_test_data('valid_inputs.json')
        self.__class__.total_valid = len(valid_inputs)
        self.__class__.valid_passed = 0  # Reset counter

        for input_text in valid_inputs:
            logger.info(f"Testing valid input: {input_text}")
            is_valid, _ = self.detector.validate_input(input_text)
            if is_valid:
                self.__class__.valid_passed += 1
            else:
                self.__class__.failed_valid.append(input_text)

        self.assertGreaterEqual(self.__class__.valid_passed, 45, 
                                f"Expected at least 45 out of {self.__class__.total_valid} valid inputs to pass, but only {self.__class__.valid_passed} passed.")

    def test_standard_injection_attempts(self):
        standard_injections = self.load_test_data('standard_injections.json')
        self.__class__.total_simple = len(standard_injections)
        self.__class__.simple_injection_passed = 0  # Reset counter

        for injection in standard_injections:
            logger.info(f"Testing simple injection: {injection}")
            is_valid, _ = self.detector.validate_input(injection)
            if not is_valid:
                self.__class__.simple_injection_passed += 1
            else:
                self.__class__.failed_simple.append(injection)

        self.assertGreaterEqual(self.__class__.simple_injection_passed, 9, 
                                f"Expected at least 9 out of {self.__class__.total_simple} simple injections to be detected, but only {self.__class__.simple_injection_passed} were detected.")

    def test_complex_injection_attempts(self):
        complex_injections = self.load_test_data('complex_injections.json')
        self.__class__.total_complex = len(complex_injections)
        self.__class__.complex_injection_passed = 0  # Reset counter

        for injection in complex_injections:
            logger.info(f"Testing complex injection: {injection}")
            is_valid, _ = self.detector.validate_input(injection)
            if not is_valid:
                self.__class__.complex_injection_passed += 1
            else:
                self.__class__.failed_complex.append(injection)

        self.assertGreaterEqual(self.__class__.complex_injection_passed, 7, 
                                f"Expected at least 7 out of {self.__class__.total_complex} complex injections to be detected, but only {self.__class__.complex_injection_passed} were detected.")

if __name__ == '__main__':
    unittest.main()