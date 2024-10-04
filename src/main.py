import requests
import argparse
from config_loader import ConfigLoader
from slack_notify import SlackNotify
from telegram_notify import TelegramNotify
from discord_notify import DiscordNotify
from dateutil import parser

def parse_args():
    # Parse positional parameters using argparse
    parser = argparse.ArgumentParser(description="Fetch and parse proposals from the ZetaChain API.")
    parser.add_argument('-o', '--outage', action='store_true')
    parser.add_argument('-m')
    parser.add_argument('-p', '--proposal', type=int)
    parser.add_argument('-e', '--env', type=str, required=True, choices=['mainnet', 'athens'])
    return parser.parse_args()

def fetch_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {api_url}: {e}")
        return None
    
def read_pending_proposals(file_path):
    try:
        with open(file_path, 'r') as file:
            proposal_ids = file.read().splitlines()  # Read all IDs as a list of strings
        return proposal_ids
    except FileNotFoundError:
        # If the file does not exist, create it and return an empty list
        print(f"File {file_path} not found. Creating an empty file.")
        with open(file_path, 'w') as file:
            pass
        return []


def main():
    #Parse positional arguments
    args = parse_args()

    # Initialize ConfigLoader to load config.yaml
    config_loader = ConfigLoader(config_file="config/config.yaml")
    slack_webhook = config_loader.get("slack", "webhook_url")
    telegram_bot_token = config_loader.get("telegram", "bot_token")
    telegram_chat_id = config_loader.get("telegram", "chat_id")
    discord_webhook = config_loader.get("discord", "webhook_url")
    status_components_api = config_loader.get("status", "components_api")
    status_incidents_api = config_loader.get("status", "incidents_api")

    if args.proposal:
        proposal_id=args.proposal
        # Fetch API URL from the config using ConfigLoader
        api_url = config_loader.get("api", args.env) + f"/{proposal_id}"
        # Fetch JSON data from the API
        proposal_json = fetch_from_api(api_url)
        proposal_status = proposal_json["proposal"]["status"]


        if proposal_json["proposal"]["messages"] and "MsgSoftwareUpgrade" in proposal_json["proposal"]["messages"][0]['@type']:
            if proposal_status == "PROPOSAL_STATUS_VOTING_PERIOD": 
                voting_start_time = parser.parse(proposal_json["proposal"]["voting_start_time"]).strftime("%Y-%m-%d %H:%M:%S") 
                voting_end_time = parser.parse(proposal_json["proposal"]["voting_end_time"]).strftime("%Y-%m-%d %H:%M:%S")
                proposal_title = proposal_json["proposal"]["title"]

                voting_message = f"Hello from ZetaChain. The proposal ID {proposal_id} {proposal_title}, is live. Voting is open from {voting_start_time} UTC to {voting_end_time} UTC"

                slack_notifier = SlackNotify(webhook_url=slack_webhook)
                slack_notifier.send_message(message=voting_message, username="ZetaChain Updates Notifier")

                telegram_notifier = TelegramNotify(telegram_bot_token, telegram_chat_id)
                telegram_notifier.send_message(message=voting_message)

                discord_notifier = DiscordNotify(webhook_url=discord_webhook)
                discord_notifier.send_message(message=voting_message, username="ZetaChain SRE Notifier", embed_title="Passed Proposal Notification")

            elif proposal_status == "PROPOSAL_STATUS_PASSED": 
                proposal_title = proposal_json["proposal"]["title"]
                upgrade_height = proposal_json["proposal"]["messages"][0]["plan"]["height"]

                passed_message = f"Hello from ZetaChain. The proposal ID {proposal_id} {proposal_title}, has passed. The Upgrade will be applied at block height {upgrade_height}"

                slack_notifier = SlackNotify(webhook_url=slack_webhook)
                slack_notifier.send_message(message=passed_message, username="ZetaChain Updates Notifier")

                telegram_notifier = TelegramNotify(telegram_bot_token, telegram_chat_id)
                telegram_notifier.send_message(message=passed_message)

                discord_notifier = DiscordNotify(webhook_url=discord_webhook)
                discord_notifier.send_message(message=passed_message, username="ZetaChain SRE Notifier", embed_title="Passed Proposal Notification")

            else:
                print(f"WARNING: Proposal ID {proposal_id} is in status {proposal_status}. No notifications have been sent.")
        else: print(f"WARNING: Proposal ID {proposal_id} is not of type MsgSoftwareUpgrade. No notifications have been sent.")

    elif args.outage:
        components_json = fetch_from_api(status_components_api)
        incidents_json = fetch_from_api(status_incidents_api)

        components = components_json.get("components", [])
        incidents = incidents_json.get("incidents", [])

        all_operational = True

        for component in components:
            if component['status'] != 'operational':
                all_operational = False
                print(f"Component: {component['name']} is not operational.")
                
                # Check for incidents affecting this component
                incident_found = False
                for incident in incidents:
                    affected_components = [comp["id"] for comp in incident.get('components', [])]  # Get all affected component IDs
                    if component['id'] in affected_components:
                        latest_incident_status = incident['status']
                        latest_incident_body = incident['incident_updates'][0]['body'] if incident.get('incident_updates') else "No updates available"
                        print(f"Latest incident update: {latest_incident_status} - {latest_incident_body}")
                        incident_found = True
                        break
                    
                if not incident_found:
                    print(f"No incident found for component: {component['name']}.")
    
        if all_operational:
            print("All components are operational. Skipping notifications.")
            

#        outage_message = "We are currently experience a 
#
#        slack_notifier = SlackNotify(webhook_url=slack_webhook)
#        slack_notifier.send_message(message=voting_message, username="ZetaChain Updates Notifier")
#
#        telegram_notifier = TelegramNotify(telegram_bot_token, telegram_chat_id)
#        telegram_notifier.send_message(message=voting_message)
#
#        discord_notifier = DiscordNotify(webhook_url=discord_webhook)
#        discord_notifier.send_message(message=voting_message, username="ZetaChain SRE Notifier", embed_title="Passed Proposal Notification")
        


if __name__ == "__main__":
    main()
