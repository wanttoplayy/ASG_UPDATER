# POCHWC

What You Need
Python 3.x installed on your computer
Your Huawei Cloud account
Access and Secret keys with ASG permissions
Quick Setup

1. Install Required Packages
   BASH

pip install -r requirements.txt

2. Update Configuration
   Open config.py and update it with your stuff:

Python

# Put your credentials here

CREDENTIALS = {
"ak": "your-access-key",
"sk": "your-secret-key",
"region": "your-region" # e.g., "ap-southeast-2"
}

# Your ASG details

ASG_CONFIG = {
"group_id": "your-asg-id", # The one you want to refresh # You can leave these as default if you're not sure
"min_size": 1,
"desired_capacity": 2,
"max_size": 3
}
How to Use
Just run:

BASH

python main.py
What the Script Does:
Check your current instances
Remove old ones safely
Create new ones
Keep you updated on what's happening
Need Help? 🤔
If you run into any issues or have questions:

Double-check your credentials in config.py
Make sure your ASG ID is correct
If you're still stuck, just shoot me an email
⚠️ Important Note
Make sure you have the right permissions set up in Huawei Cloud before running this. The script needs to be able to view and modify your ASG.
‣十彇偕䅄䕔൒�