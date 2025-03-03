import time
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkas.v1.region.as_region import AsRegion
from huaweicloudsdkas.v1 import *
from config import CREDENTIALS, ASG_CONFIG, INSTANCE_CONFIG, IMAGE_CONFIG

class ASGUpdater:
    def __init__(self):
        self.credentials = BasicCredentials(
            ak=CREDENTIALS["ak"],
            sk=CREDENTIALS["sk"]
        )
        self.client = AsClient.new_builder() \
            .with_credentials(self.credentials) \
            .with_region(AsRegion.value_of(CREDENTIALS["region"])) \
            .build()

    def wait_for_asg_unlock(self, group_id, max_attempts=5):
        """Wait for ASG to be unlocked"""
        for attempt in range(max_attempts):
            try:
                request = ShowScalingGroupRequest()
                request.scaling_group_id = group_id
                response = self.client.show_scaling_group(request)
                if response.scaling_group.is_scaling != True:
                    return True
            except Exception as e:
                print(f"Error checking ASG status: {e}")
            
            print(f"ASG is locked, waiting... (attempt {attempt + 1}/{max_attempts})")
            time.sleep(30)
        
        return False

    def get_instance_list(self, group_id):
        try:
            request = ListScalingInstancesRequest()
            request.scaling_group_id = group_id
            response = self.client.list_scaling_instances(request)
            return response.scaling_group_instances
        except Exception as e:
            print(f"Error getting instance list: {e}")
            return []

    def get_asg_name(self, group_id):
        """Get ASG name from group ID"""
        try:
            request = ShowScalingGroupRequest()
            request.scaling_group_id = group_id
            response = self.client.show_scaling_group(request)
            return response.scaling_group.scaling_group_name
        except Exception as e:
            print(f"Error getting ASG name: {e}")
            return None

    def wait_for_instances_removed(self, group_id, instance_ids, max_attempts=10):
        """Wait for instances to be fully removed"""
        for attempt in range(max_attempts):
            try:
                current_instances = self.get_instance_list(group_id)
                remaining_instances = [inst for inst in current_instances if inst.instance_id in instance_ids]
                if not remaining_instances:
                    return True
                print(f"Waiting for instances to be removed... (attempt {attempt + 1}/{max_attempts})")
                time.sleep(30)
            except Exception as e:
                print(f"Error checking instances: {e}")
        return False

    def update_scaling_configuration(self, group_id, image_id):
        """Update scaling configuration with the specified image ID"""
        try:
            print(f"\nUpdating scaling configuration with image ID: {image_id}")
            
     
            asg_name = self.get_asg_name(group_id)
            if not asg_name:
                raise Exception("Failed to get ASG name")
     
            current_version = IMAGE_CONFIG["template_version"]
            config_name = f"{asg_name}_{current_version}"
            
          
            list_config_request = ListScalingConfigsRequest()
            list_config_request.scaling_group_id = group_id
            existing_configs = self.client.list_scaling_configs(list_config_request)
            
        
            create_config_request = CreateScalingConfigRequest()
            create_config_request.body = CreateScalingConfigOption(
                scaling_configuration_name=config_name,
                instance_config={
                    "flavorRef": INSTANCE_CONFIG["flavor_id"],
                    "imageRef": image_id,
                    "key_name": INSTANCE_CONFIG["key_name"],
                    "vpcid": INSTANCE_CONFIG["vpc_id"],
                    "networks": [{
                        "id": INSTANCE_CONFIG["subnet_id"]
                    }],
                    "disk": [
                        {
                            "size": 40,
                            "volume_type": "SAS",
                            "disk_type": "SYS"
                        }
                    ]
                }
            )
            
            if INSTANCE_CONFIG["security_group_id"]:
                create_config_request.body.instance_config["security_groups"] = [{
                    "id": INSTANCE_CONFIG["security_group_id"]
                }]
            
            config_response = self.client.create_scaling_config(create_config_request)
            new_config_id = config_response.scaling_configuration_id
            print(f"Created new scaling configuration: {config_name}")

          
            update_request = UpdateScalingGroupRequest()
            update_request.scaling_group_id = group_id
            update_request.body = UpdateScalingGroupOption(
                scaling_configuration_id=new_config_id
            )
            self.client.update_scaling_group(update_request)
            print("Updated ASG with new configuration")

            time.sleep(10)

   
            if existing_configs and existing_configs.scaling_configurations:
                for config in existing_configs.scaling_configurations:
       
                    if (config.scaling_configuration_id != new_config_id and 
                        config.scaling_configuration_name.startswith(asg_name)):
                        try:
                            delete_request = DeleteScalingConfigRequest()
                            delete_request.scaling_configuration_id = config.scaling_configuration_id
                            self.client.delete_scaling_config(delete_request)
                            print(f"Deleted old configuration: {config.scaling_configuration_name}")
                        except Exception as e:
                            print(f"Warning: Could not delete old configuration {config.scaling_configuration_name}: {e}")
                            continue

            return new_config_id

        except Exception as e:
            print(f"Error updating scaling configuration: {e}")
            raise
    def force_instance_refresh(self, group_id):
        try:
            print("\n=== Starting Instance Refresh ===")
            
            if not self.wait_for_asg_unlock(group_id):
                raise Exception("ASG is locked and didn't unlock within timeout period")

            current_instances = self.get_instance_list(group_id)
            current_instance_ids = []
            if current_instances:
                current_instance_ids = [inst.instance_id for inst in current_instances]
                print(f"Found {len(current_instances)} current instances")
            else:
                print("No current instances found")

   
            modify_request = UpdateScalingGroupRequest()
            modify_request.scaling_group_id = group_id
            modify_request.body = UpdateScalingGroupOption(
                min_instance_number=0,
                desire_instance_number=0
            )
            self.client.update_scaling_group(modify_request)
            print("Group capacity modified to 0")

           
            if current_instance_ids:
                print("Waiting for instances to be fully removed...")
                if not self.wait_for_instances_removed(group_id, current_instance_ids):
                    raise Exception("Timeout waiting for instances to be removed")
                print("All instances have been removed")

    
            print("Resetting group capacity...")
            reset_request = UpdateScalingGroupRequest()
            reset_request.scaling_group_id = group_id
            reset_request.body = UpdateScalingGroupOption(
                min_instance_number=ASG_CONFIG["min_size"],
                desire_instance_number=ASG_CONFIG["desired_capacity"]
            )
            self.client.update_scaling_group(reset_request)
            print("Group capacity reset to original values")
       
            print("Waiting for new instances to be created...")
            time.sleep(60)
            
            new_instances = self.get_instance_list(group_id)
            if new_instances:
                print(f"New instances created: {len(new_instances)}")
            else:
                print("No new instances found yet")
            
            print("\n=== Instance Refresh Completed ===")
            
        except Exception as e:
            print(f"\nError during instance refresh: {e}")
            raise

    def apply_new_configuration(self, new_image_id=None):
        try:
            print("\n=== Starting Configuration Update Process ===")
            
   
            image_id = new_image_id or IMAGE_CONFIG["image_id"]
            group_id = ASG_CONFIG["group_id"]

            print(f"\nUpdating ASG configuration with image: {image_id}")
            
      
            self.update_scaling_configuration(group_id, image_id)
            
    
            self.force_instance_refresh(group_id)
            
            print("\n=== Configuration Update Process Completed Successfully! ===")
            
        except Exception as e:
            print(f"\nError during configuration update: {e}")
            raiseK