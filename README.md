# EC2 Reports - serverless - Formatted

This script has been developed to produce a csv format report on EC2 instances across multiple accounts utilising AWS roles. The output file will be a single csv which contains all instances across the accounts provided. The csv file will be automatically uploaded to S3. The report will only retrieve attributes and tags defined in the Lambda environment variables

## Getting Started
### Permissions

All of the accounts you are assuming the role in will require the roll defined. They must all use the same role name

The role must trust the account which the assume is being performed and have at a minimum Read Only EC2 access

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

The code has been deployed as Python 3.8 (latest at time of writing) within Lambda

The timeout value will depend on the number of accounts and EC2 instances you are reporting on. I started with 10 seconds which was sufficient.

#### Testing

Configure a test event and have nothing define in the json, e.g.
```json
{}
```

#### Environment variables

To ensure the code can easily be re-used I have set all the key elements as variables.
These can then be updated by anyone without having to get involved in the coding side. e.g. adding a new account or 
tag can easily be done by updating the comma separated list for the item within the Lambda environment variables.

Key                  | Value
---------------------|----------------------
arole | role name to assume
attributes | **(comma separated list)** e.g. OwnerId,InstanceId,InstanceType
tags | **(comma separated list)** e.g. Name,Project,Release,Environment,CostCentre
aws_accounts | **(comma separated list)** e.g. 1111111111111,2222222222222,3333333333333
bucket_name | name of bucket e.g. reporting_test_bucket
output_path | folder within the bucket where the report will be held. E.g. ec2_reports

### Trigger : CloudWatch Events

Please use the following steps to define a schedule trigger to generate the log files

1. On the AWS Console, navigate to CloudWatch. Then select the Events | Rules
2. Select the Create Rule button
3. Select the schedule radio button and define your schedule. We used a cron expression 
    00 03 ? * * *
    This executed the code at 3am everyday of the week
4. Select the add target button
5. Choose Lambda function and then select your function from the drop down list
6. Select the Configure details button
7. Give the rule a meaningful name and description
7. Select the Create rule button

### S3 considerations

Unless you have any contractual or regulatory requirements to retain x amount of logs, you could introduce a 
Lifecycle rule to the s3 bucket to remove objects older than x days.

### Known issues
None

## Author

**Dave Hart**