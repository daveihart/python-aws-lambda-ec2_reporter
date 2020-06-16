# EC2 Reports - serverless

This script has been developed to produce a csv format report on ec2 instances across multiple accounts utlising aws roles. The output file will be a single csv which contains all instances across the accounts provided. The csv file will be uploaded to s3. The report will only retrieve attributes and tags defined in the Lambda environment variables

## Getting Started


### Permissions
All of the accounts you are assuming the role in will require the roll defined. They must all use the same role name



The role must trust the account which the assume is being performed

For this script you only need read-only access to EC2

Create a role which can be used by Lambda. The role applied to Lambda must at a minimum have;

#### Assume Role across accounts;
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam::account_number:role/role_name"
        }
    ]
}
```
*The Resource can be made into a list to define multiple accounts*

#### AmazonEC2ReadOnlyAccess     AWS Managed Policy to allow you to describe the EC2 instances

#### For logging to cloudWatch (useful for audit and troubleshooting);
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```
#### Ability to upload to S3 bucket
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListAllMyBuckets",
                "s3:GetBucketLocation"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": [
                "arn:aws:s3:::bucket_name",
                "arn:aws:s3:::bucket_name/*"
            ]
        }
    ]
}
```

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