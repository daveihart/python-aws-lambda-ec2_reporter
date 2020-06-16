# EC2 Reports serverless

This script is designed to allow reporting on AWS ec2 instances across multiple accounts using the assume role function. The output file will be a single csv which contains all instances across the accounts defined. The csv file will be uploaded to s3. The report will only retrieve attributes and tags defined in the Lambda environment variables




## Getting Started

### Permissions


### Lambda configuration

#### Environment variables

Key | Value

arole | role name to assume
attributes | (comma seperated list) e.g. OwnerId,InstanceId,InstanceType
aws_accounts | (comma seperated list) e.g. 1111111111111,2222222222222,3333333333333


### 


### Prerequisites


## Author

* **Dave Hart**