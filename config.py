# config.py

# Huawei Cloud 
CREDENTIALS = {
    "ak": "your ak",
    "sk": "your sk",
    "region": "ap-southeast-2" 
}

# Auto Scaling Group 
ASG_CONFIG = {
    "group_id": "", 
    "min_size": 1,
    "desired_capacity": 2,
    "max_size": 3
}

# Instance Config
INSTANCE_CONFIG = {
    "flavor_id": "s6.small.1",
    "key_name": "KeyPair-best",
    "security_group_id": "",  
    "vpc_id": "",  
    "subnet_id": ""  
}

# Terraform Config
TERRAFORM_CONFIG = {
    "image_id": "",  
    "template_version": ""
}