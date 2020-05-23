import boto3
import paramiko
import time

def lambda_handler(event, context):

    ec2 = boto3.resource('ec2', region_name='eu-central-1')
    instance_id = 'i-06dbdde8de0e4a203'
    instance = ec2.Instance(instance_id)
    time.sleep(1)

    # Print few details of the instance
    print("Instance id - ", instance.id)
    print("Instance public IP - ", instance.public_ip_address)
    print("Instance private IP - ", instance.private_ip_address)
    print("Public dns name - ", instance.public_dns_name)
    print("----------------------------------------------------")

    # Connect to S3, we will use it get the pem key file of your ec2 instance
    s3_client = boto3.client('s3')

    # Download private key file from secure S3 bucket and save it inside /tmp/ folder of lambda event
    s3_client.download_file('ssh-key', 'v2.pem', '/tmp/v2.pem')

    # Allowing few seconds for the download to complete
    time.sleep(1)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file('/tmp/v2.pem')
    # username depending upon yor ec2 AMI
    ssh.connect(instance.public_ip_address, username='loginuser', pkey=privkey, port='14422' )
    stdin, stdout, stderr = ssh.exec_command("sudo confd-client.plx get_ipsec_status | grep -E \"\'established\'|REF_|expected\" | xargs \n sudo confd-client.plx get_ipsec_status | grep -E \"all_established|REF_|\'rightsubnet\'\" | xargs")
    #(" df -h \n du -h")
    opt =stdout.readlines()
    opt = "".join(opt)
    print(opt)

#-----------Tests---------------
#    stdin.flush()
#    data = stdout.read().splitlines()
#    for line in data:
#         print(line)
#    ssh.close()

#        exit_code = stdout.read().decode('ascii').strip("\n")
