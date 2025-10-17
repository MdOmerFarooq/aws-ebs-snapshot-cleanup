# AWS Cloud Cost Optimization - EBS Snapshot Cleanup Lambda

This is a small project I built to automate the cleanup of **orphaned EBS snapshots** in AWS. Over time, snapshots pile up from old volumes and can quietly rack up unnecessary storage costs. This Lambda function identifies unused snapshots and deletes them automatically, saving both time and money.

## What I Used 🧰 

- **Python + Boto3** – for interacting with AWS services
- **AWS Lambda** – to run the cleanup logic  
- **Amazon EC2 / EBS** – to list and check snapshot/volume details  
- **CloudWatch Logs** – to view execution logs and track deletions  


## ⚙️ How It Works

1. The Lambda lists all snapshots owned by the account.  
2. It checks if each snapshot is linked to a valid volume.  
3. If the snapshot isn’t attached to any existing volume (basically an orphan), it deletes it.  
4. Each action (found/deleted) is logged to **CloudWatch** for reference.

You can run it manually by testing in the Lambda console or set up an **EventBridge rule** to run it on a schedule (e.g., daily).




