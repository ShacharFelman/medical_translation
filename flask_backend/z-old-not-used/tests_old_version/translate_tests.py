"""TODO - doc it.
"""
import unittest

# from logger import logger
from engine.engine import translation_engine
from utils.exceptions import InvalidUserInputError
from tests_old_version.utils import DataCache, TestStatus


class TranslationTestCase(unittest.TestCase):
    def __init__(self, method_name: str):
        super().__init__(method_name)
        self.data = DataCache()

    @classmethod
    def setUpClass(cls):
        if not translation_engine.is_initialized():
            translation_engine.initialize()

    @classmethod
    def tearDownClass(cls):
        DataCache().commit()

    @property
    def book_relpath(self) -> str:
        return "translation.xlsx"

    @staticmethod
    def _translate(text_input: str, html_input: str):
        return translation_engine.translate("DUMMY", "DUMMY", "DUMMY", text_input=text_input, html_input=html_input)

    def test_invalid_prompt(self):
        sheet_names = ["invalid"]

        sheets = [self.data.get_sheet(self.book_relpath, name) for name in sheet_names]

        for sheet in sheets:
            for index, test_input in sheet.inputs():
                with self.subTest(f"Testing invalid prompt", **test_input):
                    status = TestStatus.PASS
                    reason = "Expected InvalidUserInputError, but "
                    output = ""

                    try:
                        output = self._translate(**test_input)

                        status = TestStatus.FAIL
                        reason = "Expected InvalidUserInputError, but translated successfuly."
                    except Exception as e:
                        if not isinstance(e, InvalidUserInputError):
                            status = TestStatus.FAIL
                            reason = f"Expected InvalidUserInputError, but got {e}"

                    sheet.update(index, status, output=output, reason=reason)
                    self.assertEqual(status, TestStatus.PASS, msg=reason)

    def test_valid_prompt(self):
        sheet_names = ["valid", "valid_tagged"]

        sheets = [self.data.get_sheet(self.book_relpath, name) for name in sheet_names]

        for sheet in sheets:
            for index, test_input in sheet.inputs():
                with self.subTest(f"Testing valid prompt", **test_input):
                    status = TestStatus.PASS
                    reason = ""
                    output = ""

                    try:
                        output = self._translate(**test_input)
                    except Exception as e:
                        status = TestStatus.FAIL
                        reason = f"Translation failed, raised {e}"

                    sheet.update(index, status, output=output, reason=reason)
                    self.assertEqual(status, TestStatus.PASS, msg=reason + f"\nOn input: {test_input}")


if __name__ == "__main__":
    unittest.main()
