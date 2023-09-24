# README

## Instructions on How to Run the Source Code Locally
1. ### **Dependencies:**

Before you start, ensure that you have the following installed:

Python 3

pandas: `pip install pandas`<br>

xlrd: `pip install xlrd` (required for reading Excel files with pandas)

2. ### **Clone the Repository:** 

git clone https://github.com/WXUXIN/Data-Engineer-Internship-Tech-Test-.git

cd https://github.com/WXUXIN/Data-Engineer-Internship-Tech-Test-.git

3. ### **Place Data Files in Directory:**
Make sure you have `restaurant_data.json` and `Country-Code.xlsx` in the main directory (or adjust the paths in the code accordingly).

4. ### **Run the Code:**
python govtech.py

## Cloud Deployment and Design
### **Design & Deployment:**

I will use three main AWS services: Amazon S3, AWS Lambda, and Amazon RDS. I will store both the raw and processed data in Amazon S3 because it's reliable and easy to work with. When a new file is uploaded to S3, AWS Lambda automatically processes it due to a set trigger. This setup is both scalable and cost-effective, as I only pay for the time Lambda runs. After processing, the data goes into Amazon RDS, which is a database service made for easy data access.

To set this up, I will first first create an S3 bucket to hold the raw data and set it to notify Lambda when new data comes in. Next, I will set up AWS Lambda, making sure it can access both S3 and RDS. After I've set the rules for how Lambda should process the data, I will create an RDS database and make sure Lambda can save data to it. 

In summary, the whole process starts when I upload data to S3, which then gets processed by Lambda to produce the intended CSV files, and they are finally stored in RDS for future access.



### **Decisions & Considerations:**

I chose AWS Lambda because it works automatically when data is added to S3. This approach is simple, scales as needed, and is cost-effective since you only pay for what you use. For the kind of data we have, Lambda is a good choice.

For storing our data, we picked Amazon RDS because the data is organized and RDS is made for that kind of data. RDS is easy to scale, flexible, and secure. It makes sure the data is saved in a way that's easy to access later. It also has features like automatic backups and strong security.

With AWS Lambda's built-in error checks and S3's notifications, I can quickly know if something goes wrong, keeping our data safe.

Thinking about the future, both Lambda and RDS can handle more work if needed,keeping things running smoothly when there are more data or more requests.

Cost is also an important factor to consider. By using services like Lambda, I only pay for what I actually use, which saves money in the long run.

In short, my setup is made to handle the restaurant data in a reliable, scalable, and cost-effective way, showing how using cloud services can make data tasks easier.

## Architecture diagram:
![Architecture diagram](architecture_diagram.png)