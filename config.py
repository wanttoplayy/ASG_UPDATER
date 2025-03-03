# config.py

# Huawei Cloud 
CREDENTIALS = {
    "ak": "BYJ15CSXRF44ONZK1HAG",
    "sk": "u4DdWpG7pU59DCjOHCsOvzOI9HQcq22OqnV1HbUG",
    "region": "ap-southeast-2" 
}

# Auto Scaling Group 
ASG_CONFIG = {
    "group_id": "cc569c6d-2fbc-4f6a-bfd7-2db1fa28c1ee", 
    "min_size": 1,
    "desired_capacity": 2,
    "max_size": 3
}

# Instance Config
INSTANCE_CONFIG = {
    "flavor_id": "s6.small.1",
    "key_name": "KeyPair-best",
    "security_group_id": "f6c94959-7c58-4e68-ab08-cd6d395a3846",  
    "vpc_id": "fd2d2046-b275-40d7-9cfc-839c7db1f084",  
    "subnet_id": "5c96e622-cd8c-424d-9716-cec65273d49f",
    "disk_config": {
        "system_disk_size": 40,  
        "system_disk_type": "SAS" 
    }
}
# Terraform Config
TERRAFORM_CONFIG = {
    "image_id": "b4165541-51fa-485d-8466-db95aa7e00ac",  
    "template_version": "v2"
}