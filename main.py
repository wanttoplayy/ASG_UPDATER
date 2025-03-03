# main.py

from asg_updater import ASGUpdater

def main():
    print("\n=== Auto Scaling Group Update Tool ===")
    try:
        updater = ASGUpdater()
        # Use default image from config
        updater.apply_new_configuration()
        
        # Or specify a new image ID:
        # updater.apply_new_configuration(new_image_id="your-new-image-id")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()