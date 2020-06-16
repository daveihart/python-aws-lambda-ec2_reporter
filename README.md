# EC2 Reports serverless

This script has been developed to produce a csv format report on ec2 instances across multiple accounts utlising aws roles. The output file will be a single csv which contains all instances across the accounts provided. The csv file will be uploaded to s3. The report will only retrieve attributes and tags defined in the Lambda environment variables

## Getting Started


### Permissions


### Lambda configuration



#### Environment variables

Key                  | Value
---------------------|----------------------
arole | role name to assume
attributes | **(comma seperated list)** e.g. OwnerId,InstanceId,InstanceType
aws_accounts | **(comma seperated list)** e.g. 1111111111111,2222222222222,3333333333333


### 


### Prerequisites


## Author

* **Dave Hart**