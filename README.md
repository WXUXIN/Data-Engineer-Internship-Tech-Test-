# README

### Instructions on How to Run the Source Code Locally
**Dependencies:**

Before you start, ensure that you have the following installed:

Python 3
    - pandas: `pip install pandas`<br>
    - xlrd: `pip install xlrd` (required for reading Excel files with pandas)

**Clone the Repository:** 

git clone https://github.com/WXUXIN/Data-Engineer-Internship-Tech-Test-.git

cd https://github.com/WXUXIN/Data-Engineer-Internship-Tech-Test-.git

**Place Data Files in Directory:**
Make sure you have `restaurant_data.json` and `Country-Code.xlsx` in the main directory (or adjust the paths in the code accordingly).

**Run the Code:**
python govtech.py

	---
### Cloud Deployment and Design
**Design & Deployment:**
A cloud-based solution, ideally on AWS, can streamline this process:

Storage: Use Amazon S3 to store our data files (restaurant_data.json and Country-Code.xlsx) and output files (restaurants.csv and restaurant_events.csv).

Processing: Use AWS Lambda with triggered events. Whenever a new restaurant_data.json is uploaded to the S3 bucket, it automatically triggers the Lambda function to process the file.

Data Management: For more extensive querying and analysis, Amazon RDS or Amazon Redshift can be used to store restaurant and event data.

**Decisions & Considerations:**
Scalability: Lambda functions scale automatically by running code in response to triggers. With S3 and RDS/Redshift, we're also ensuring our storage scales.

Cost: Using AWS Lambda and S3 is cost-effective. You pay only for the compute time and storage you consume.

Maintenance: Serverless architectures reduce the need for system administration.

Flexibility: The architecture allows integration with other AWS services, like Amazon QuickSight for BI and visualizations.

Security: Ensure that the S3 buckets are private and only the Lambda function has the IAM role with permissions to access and process the data.
