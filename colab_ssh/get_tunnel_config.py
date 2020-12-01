import requests
import re
import time

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

def get_argo_tunnel_config():
	hostname = None
	for i in range(10):
		output = requests.get("http://127.0.0.1:45678/metrics").text
		result = re.search('cloudflared_tunnel_user_hostnames_counts{userHostname="https://(.+?)"}', output)
		if result is None:
			time.sleep(2)
			continue
		hostname = result.group(1)
		break

	if hostname is None:
		raise Exception("Cannot get the hostname from cloudflared, it looks like the connection has failed.")

	return {
		"domain":hostname,
		"protocol":"",
		"port":22
	}