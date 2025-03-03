# config.py

# Huawei Cloud Credentials
CREDENTIALS = {
    "ak": "",  # Access Key ID from Huawei Cloud
    "sk": "",  # Secret Access Key from Huawei Cloud
    "region": ""  # Huawei Cloud region
}

# Auto Scaling Group Configuration
ASG_CONFIG = {
    "group_id": "",  # Your ASG ID
    "min_size": 1,  # Minimum number of instances in the ASG
    "desired_capacity": 2,  # Desired number of instances in the ASG
    "max_size": 3  # Maximum number of instances in the ASG
}

# Instance Configuration
INSTANCE_CONFIG = {
    "flavor_id": "",  # Example: "s6.small.1" - Instance type/flavor
    "key_name": "",  # Example: "KeyPair-name" - SSH key pair name
    "security_group_id": "",  # Example: "f6c94959-xxxx-xxxx-xxxx-cd6d395a3846" - Security group ID
    "vpc_id": "",  # Example: "fd2d2046-xxxx-xxxx-xxxx-839c7db1f084" - VPC ID
    "subnet_id": "",  # Example: "5c96e622-xxxx-xxxx-xxxx-cec65273d49f" - Subnet ID
    "disk_config": {
        "system_disk_size": 40,  # System disk size in GB
        "system_disk_type": "SAS"  # Disk type: SAS, SSD, etc.
    }
}

# Image Configuration
IMAGE_CONFIG = {
    "image_id": "",  # Example: "aa4ad3d8-xxxx-xxxx-xxxx-e158f8722ab2" - Your custom image ID
    "template_version": ""  # Example: "v2" - Version tag for your template
}