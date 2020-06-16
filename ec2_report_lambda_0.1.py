#######################################################################
# report on ec2 instances retrieving a defined set of values and tags
# author: Dave Hart
# email:  daveihart@hotmail.com
# date: 29/05/2020
#######################################################################

import boto3
import csv
import os
import botocore
from datetime import date

output_file="/tmp/temp.csv"
output_path = os.environ['output_path']
report_format = "formatted"
accounts_list = os.environ['aws_accounts']
accounts = accounts_list.split(",")
arole = os.environ['arole']

values_list = os.environ['attributes']
formatting_values = values_list.split(",")

tags_list = os.environ['tags']
formatted_tags = tags_list.split(",")

bucket_name = os.environ['bucket_name']
dt=date.today()
dtstr=dt.strftime("%Y%m%d")
s3_output_file=output_path +"/"+"ec2_report_"+dtstr+".csv"

def assume_roles(acc,accounts,arole):
    global acc_key
    global sec_key
    global sess_tok
    global client
    print(f"Initating assume role for account : {acc}")
    sts_conn = boto3.client('sts')
    print(f"role defined :{arole}")
    print(f"account defined :{acc}")
    tmp_arn = f"{acc}:role/{arole}"
    print(tmp_arn)
    response = sts_conn.assume_role(DurationSeconds=900,RoleArn=f"arn:aws:iam::{tmp_arn}",RoleSessionName='Test')
    acc_key = response['Credentials']['AccessKeyId']
    sec_key = response['Credentials']['SecretAccessKey']
    sess_tok = response['Credentials']['SessionToken']
    print(f"Access key = {acc_key}")
    
def get_instances(process_acc,filters=[]):
    reservations = {}
    try:
        reservations = ec2.describe_instances(
            Filters=filters
        )
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
    instances = []
    for reservation in reservations.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instances.append(instance)
    return instances 

def formatted_report(instances,attrib_set,tag_set):
    #Build two lists. One for attributes and one for tags. These will be used to define the column values for the csv
    max=int(len(formatting_values))
    m=0
    for i in formatting_values:
        attrib_set.append(i)
    for t in formatted_tags:
        tag_set.append(t)
    tag_set = list(set(tag_set))
    attrib_set = list(set(attrib_set))
    print(attrib_set)

def report_writer(processing_acc,instances,attrib_set,tag_set):
    #used for the formatted report
    with open(output_file, 'a') as csvfile:
        fieldnames = attrib_set + tag_set
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)        
        if processing_acc == 1:
            print("writing header")
            writer.writeheader()
        for instance in instances:
            row = {}
            max=int(len(attrib_set))
            m=0
            for i in attrib_set:
                m +=1
                n = m-1
                if i == "State": #Its a list so needs more processing
                    tmpstate=instance.get(i)
                    row[attrib_set[n]] = tmpstate['Name']
                elif i == "Placement":
                    tmpplacement=instance.get(i)
                    row[attrib_set[n]] = tmpplacement['AvailabilityZone']
                elif i == "OwnerId":
                    nicinf=instance.get('NetworkInterfaces')
                    for val in nicinf:
                        for val2, val3 in val.items():
                            if val2 == "OwnerId":
                                row[attrib_set[n]] = str("'" + val3) + "'"
                elif i == "CoreCount":
                    vtype=instance.get('CpuOptions')
                    for vcore,cores in vtype.items():
                        if vcore == "CoreCount":
                            row[attrib_set[n]] = cores
                elif i == "ThreadsPerCore":
                    vtype=instance.get('CpuOptions')
                    for vcore,cores in vtype.items():
                        if vcore == "ThreadsPerCore":
                            row[attrib_set[n]] = cores
                else:
                    row[attrib_set[n]] = instance.get(i)
            for tag in instance.get('Tags', []):
                if tag.get('Key') in formatted_tags:
                    row[tag.get('Key')] = tag.get('Value')
            writer.writerow(row)

def lambda_handler(event, context):
    global ec2
    global attrib_set
    global tag_set
    global instances
    global session
    global client
    global processing_acc
    global headers
    global writer
    attrib_set = []
    tag_set = []  
    processing_acc = 0
    headers = 0
    
    #get account this is executing in so we know whether to assume a role in another account
    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]
    print(f"script is executing in {account_id}")
    
    #define s3
    s3=boto3.client("s3")
    
    #remove the old output file if exists
    print(f"Checking for file : {output_file}")
    for acc in accounts:
        processing_acc += 1
        print(f"Processing account : {processing_acc}")
        if acc != account_id:
            assume_roles(acc,accounts,arole)
            ec2 = boto3.client('ec2',aws_access_key_id=acc_key,aws_secret_access_key=sec_key,aws_session_token=sess_tok,region_name='eu-west-1')
            instances = get_instances(processing_acc)
            if processing_acc == 1:
                formatted_report(instances,attrib_set,tag_set)
            report_writer(processing_acc,instances,attrib_set,tag_set)
        else:
            print(f"account {acc}")
            ec2=boto3.client('ec2')
            instances = get_instances(processing_acc)
            if processing_acc == 1:
                formatted_report(instances,attrib_set,tag_set)
            report_writer(processing_acc,instances,attrib_set,tag_set)
            #upload to s3
    print(F"uploading {s3_output_file} to s3")
    s3.upload_file(output_file, bucket_name, s3_output_file)    
    print("finished")