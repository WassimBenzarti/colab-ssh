import requests
import re

def get_tunnel_config():
	output = requests.get("http://localhost:4040/api/tunnels").json()
	public_url = output["tunnels"][0]["public_url"]
	groups = re.match(r'(.*?)://(.*?):(\d+)', public_url)
	protocol = groups.group(1)
	domain = groups.group(2)
	port = groups.group(3)
	return {
		"domain":domain,
		"protocol":protocol,
		"port":port
	}