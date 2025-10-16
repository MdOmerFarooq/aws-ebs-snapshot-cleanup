import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

# Get all EBS data 
    ebs_response = ec2.describe_snapshots(OwnerIds=['self'])
    for snapshot in ebs_response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

# deleting snapshots which are not attached to any volumes

        if not volume_id:
            ec2.delete_snapshot( SnapshotId= snapshot_id )
            print(f"Deleted EBS snapshot {snapshot_id} as it was not attached to any volume.")

# all the snapshots without volume are deleted 
# now we have to check if the snapshots attached to volumes are the volumes actually attached to instances
        else :
            try :
# making api call to aws requesting all the details of the volume id
                volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
# if volume exists aws will send response in json with all the details
# check if volume is attached to any instance
                if not volume_response['Volumes'][0]['Attachments']: # exceutes if list is empty of attachments
                    ec2.delete_snapshot( SnapshotId= snapshot_id )
                    print(f"Deleted EBS snapshot {snapshot_id} as it was taken from a volume not attached to any running instance.")
            except ec2.exceptions.ClientError as e:
# We landed here because describe_volumes failed.
# Now we check for the specific reason it failed.
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
# The volume is gone. The snapshot is an orphan.
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS snapshot {snapshot_id} as its associated volume was not found.")



