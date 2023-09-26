# README

## Instructions on How to Run the Source Code Locally

### 1. **Dependencies**:

Before running, ensure the following are installed:

- **Python 3**
- **pandas**: Run `pip install pandas`
- **xlrd**: Run `pip install xlrd` (Required for reading Excel files with pandas)

### 2. **Clone the Repository**:

```bash
git clone https://github.com/WXUXIN/Data-Engineer-Internship-Tech-Test-.git
cd Data-Engineer-Internship-Tech-Test-
```

### 3. **Place Data Files in Directory**:

Ensure `restaurant_data.json` and `Country-Code.xlsx` are in the main directory. Adjust paths in the code if placed differently.

### 4. **Run the Code**:

```bash
python govtech.py
```

Upon successful execution, the following output files will be generated:

1. restaurants.csv: A comprehensive list of restaurants.
2. restaurant_events.csv: A list of restaurants that have past event in the month of April 2019.
   If the restaraunt has more than 1 photo for the event, each photo URL will be stored in a separate row.

All empty values are populated with "NA"

Additionally, the terminal will display threshold values for the different ratings text:

- **min**: The lowest aggregate score qualifying for a rating text.

- **max**: The highest aggregate score that a rating text have.

## Assumptions & Interpretations

### Assumptions:

1. An event qualifies as a "Past event in April 2019" if the event's start date is within April 2019, regardless of the end date.
2. Event dates will always follow the "YYYY-MM-DD" format.
3. Zomato's country code remains consistent.
4. There are 20 restaurants located in the city labeled "Dummy" with the Country Code 17. These entries appear anomalous given that their country code is absent from the valid list in Country-Code.xlsx and the placeholder nature of the city name. Despite their irregularity, these entries will be retained to ensure the integrity and completeness of the dataset.

### Interpretations:

1. Keys like "results_found” and “results_start" aren't crucial for restaurant data extraction.
2. The restaurant's ID is represented as `"R": { "res_id": ... }`.
3. The "zomato_events" key holds a list of dictionaries detailing all events for a given restaurant.
4. Events can have multiple associated photos. Each photo will be stored in individual rows in the output restaurant_events.csv.

## Cloud Deployment and Design

### **Design & Deployment:**

I will use three main AWS services: Amazon S3, AWS Lambda, and Amazon RDS. I will store both the raw data in Amazon S3 because it's reliable and easy to work with. When a new file is uploaded to S3, AWS Lambda automatically processes it due to a set trigger. This setup is both scalable and cost-effective, as I only pay for the time Lambda runs. After processing, the data goes into Amazon RDS, which is a database service made for easy data access.

To set this up, I will first create an S3 bucket. Next, I will set up an AWS Lambda function and establish a trigger and set up an S3 event notification on the bucket to trigger the Lambda function whenever new data is added, and lastly make sure that Lambda can access both S3 and RDS. After I've set the rules for how Lambda should process the data, I will create an RDS database and make sure Lambda can save data to it.

In summary, the whole process starts when I upload data to S3, which then gets processed by Lambda to produce the intended CSV files, and they are finally stored in RDS for future access.

### **Decisions & Considerations:**

I chose AWS Lambda because it works automatically when data is added to S3. This approach is simple, scales as needed, and AWS Lambda is not only cost-effective, ensuring I only pay for the actual compute time I consume, but it's also inherently scalable. As the data grows, Lambda can handle increased loads without any manual intervention. For the type of datasets I'am working with, primarily restaurant data that requires periodic, not constant, updates, this serverless model is exceptionally efficient. Lastly, with AWS Lambda's built-in error checks and S3's notifications, I can quickly know if something goes wrong, keeping the data safe.

For storing the data, Amazon RDS stood out as the clear choice. The data is structured, and I need a reliable database service that could not only store this data but also facilitate easy retrieval. RDS is inherently scalable, ensuring that as the datasets grow, it can effortlessly handle increased storage and access requests. Additionally, RDS is also extremely flexible, whether I need to change the instance type or adjust storage, RDS provides that leeway. Security is paramount, and RDS delivers on this front with robust security features, ensuring the data remains protected. Moreover, RDS's automatic backup and disaster recovery features mean that the data is safeguarded against unforeseen incidents. Given the focus on restaurant data, which requires structured storage and efficient retrieval mechanisms, RDS emerges as the ideal choice.

In short, my setup is made to handle the restaurant data in a reliable, scalable, and cost-effective way, showing how using cloud services can make data tasks easier.

## Architecture diagram:

![Architecture diagram](architecture_diagram.png)

## Test Script Summary

The `testing.py` script evaluates the behavior of `govtech.py` by subjecting it to several test cases.

### Test Cases Covered:

1. **Empty JSON file**: Determines how the system copes with the absence of data.
2. **Invalid Country Codes**: Assesses behavior when restaurants have country codes not found in `Country-Code.xlsx`.
3. **Absent Photo URLs**: Reviews how restaurants with missing photo URLs are processed.

Each test is designed to test that the data processing adapts gracefully to these cases, ensuring data integrity and robust system behavior.

### Setup:

Before each test, the testing script sets up some prerequisites, including file paths to specific JSON files, each containing the first 20 restaurants from the original dataset with the modifications to be tested, except for empty_restaurant_data.json, which is empty. All JSON files are to be in the main directory:

1. empty_restaurant_data.json: For the test involving an empty JSON.
2. invalid_country_code.json: For the test checking invalid country codes.
3. empty_photo_url.json: For the test verifying the behavior with empty photo URLs.

### **Run the testing script**:

```bash
python testing.py
```

### Expected Output:

Upon successful execution of the tests, the following messages will be displayed:

#### Successful Tests:

- **Empty JSON Test**: "Passed Empty JSON Test"

- **Invalid Country Code Test**: "Passed Invalid Country Code Test"

- **Empty Photo URL Test**: "Passed Empty Photo URL Test"

#### Failed Tests:

- **Empty JSON Test**: "Failed Empty JSON Test"

- **Invalid Country Code Test**: "Failed Invalid Country Code Test"

- **Empty Photo URL Test**: "Failed Empty Photo URL Test"

## **Test Cases:**

#### **1. `test_empty_json`**

- **Purpose**:

  - This test ensures the system's resilience when encountering an empty JSON dataset.

- **Expected Outcome**:
  - The `process_data` function in govtech.py should raise an exception when given an empty JSON. This is to ensure the function doesn't process invalid or empty datasets, which could lead to unexpected behaviors or errors later on.

---

#### **2. `test_invalid_country_code`**

- **Purpose**:

  - Evaluates how the function handles restaurants with country codes not present in Country-Code.xlsx.

- **Execution**:

  - Restaurant with id 18537536 has a country code of 100, which is not present in the list of valid country codes, is used to test the function's behavior.
  - The `warnings` module captures any warnings thrown during the processing of the dataset.
  - The test asserts that a warning has been issued.

- **Expected Outcome**:
  - A warning should be raised by the `process_data` function when it encounters an invalid country code.
  - The warning message should specifically state: "Invalid country code detected!" to ensure clear communication of the issue.
  - This allows for graceful degradation; rather than stopping the entire process due to a single entry's invalid country code, the function sends a warning and continues processing.

---

#### **3. `test_empty_photo_url`**

- **Purpose**:

  - Ensures that restaurants with missing photo URLs are handled correctly.

- **Execution**:

  - The function processes the dataset.
  - The resultant CSV is read to verify how empty photo URLs have been processed.

- **Expected Outcome**:
  - Restaurants with missing photo URLs should be included in the output CSV, demonstrating the function's resilience against incomplete data.
  - Specifically, there should be 9 such restaurants. This ensures that missing data points aren't simply dropped but are instead filled in with 'NA' and retained.

---
