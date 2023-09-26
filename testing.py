import unittest
import os
import pandas as pd
from govtech import process_data  # Assuming you saved your script as 'govtech.py'
import warnings

class CustomTestResult(unittest.TextTestResult):

    # def addSuccess(self, test):
    #     super().addSuccess(test)
    #     # Use self.stream.write to print the desired character
    #     self.stream.write('Passed\n')
    #     self.stream.flush()


    def addSuccess(self, test):
        if test._testMethodName == "test_empty_json":
            self.stream.write("Passed Empty JSON Test\n")
        elif test._testMethodName == "test_invalid_country_code":
            self.stream.write("Passed Invalid Country Code Test\n")
        elif test._testMethodName == "test_empty_photo_url":
            self.stream.write("Passed Empty Photo URL Test\n")
        else:
            self.stream.write('Passed\n')
        self.stream.flush()

    def addFailure(self, test, err):
        if test._testMethodName == "test_empty_json":
            self.stream.write("Failed Empty JSON Test\n")
        elif test._testMethodName == "test_invalid_country_code":
            self.stream.write("Failed Invalid Country Code Test\n")
        elif test._testMethodName == "test_empty_photo_url":
            self.stream.write("Failed Empty Photo URL Test\n")
        else:
            self.stream.write("Failed\n")
        self.stream.flush()

class CustomTestRunner(unittest.TextTestRunner):
    resultclass = CustomTestResult

class TestRestaurantDataProcessing(unittest.TestCase):
    
    def setUp(self):
        # This will run before each test to set up any prerequisites
        self.empty_restaurant_data = 'empty_restaurant_data.json'
        self.invalid_country_code = 'invalid_country_code.json'
        self.empty_photo_url = 'empty_photo_url.json'

    # Evaluates how the function handles restaurants with country codes not present in a predefined list or excel sheet.   
    def test_empty_json(self):        
        with self.assertRaises(Exception):
            process_data(self.empty_restaurant_data)

    # If there are restaurants with country code not in the excel sheet provided and their city is not Dummy, raise exception
    # res_id 18537536

    # Evaluates how the function handles restaurants with country codes not present in a predefined list or excel sheet.
    def test_invalid_country_code(self):
        with warnings.catch_warnings(record=True) as w:
            # Trigger a warning.
            process_data(self.invalid_country_code)
            # Ensure some warnings were issued.
            self.assertTrue(len(w) > 0)
            # Check that the message of the first warning matches your expectation.
            self.assertEqual(str(w[0].message), "Invalid country code detected!")

    # Empty Photo URLS must be populated with NA, and work as per normal
    # There are 9 restaurants with events within the month of April with empty photo urls 
    def test_empty_photo_url(self):
        # You can write a malformed JSON file here similar to how the empty json is written above
        process_data(self.empty_photo_url)
        main_df = pd.read_csv('restaurant_events.csv')

        # Check that there are 9 restaurants with empty photo urls
        self.assertEqual(len(main_df[pd.isna(main_df['Photo URL'])]), 9)
        
if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())

    
