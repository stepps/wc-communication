import yaml
import os

class ConfigLoader:
    def __init__(self, config_file="config/config.yaml"):
        """
        Initialize the ConfigLoader with the path to the configuration file.
        
        :param config_file: Path to the YAML configuration file (default: "config/config.yaml")
        """
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """
        Load the configuration from the YAML file.
        
        :return: A dictionary containing the configuration data
        :raises: FileNotFoundError if the config file doesn't exist
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

        with open(self.config_file, 'r') as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise RuntimeError(f"Error parsing the configuration file: {e}")

    def get(self, section, key=None, default=None):
        """
        Retrieve a configuration value.
        
        :param section: The section of the config (e.g., "vault", "slack")
        :param key: The specific key within the section (optional)
        :param default: The default value to return if the key is not found
        :return: The configuration value or None if not found
        """
        section_data = self.config.get(section, {})
        if key:
            return section_data.get(key, default)
        return section_data

if __name__ == "__main__":
    # Example usage
    config_loader = ConfigLoader(config_file="config.yaml")
    
    # Fetch Vault configuration
    vault_address = config_loader.get("vault", "address")
    vault_token = config_loader.get("vault", "token")
    
    print(f"Vault Address: {vault_address}")
    print(f"Vault Token: {vault_token}")

