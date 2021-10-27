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

def get_argo_tunnel_config(initial_path=""):
  hostname = None
  with open(initial_path+"cloudflared.log", "r") as f:
    output = "".join(f.readlines())
  result = re.search(':\"\| *https://(.+?.trycloudflare.com) *\|\"}', output)
  # result = re.search('cloudflared_tunnel_user_hostnames_counts{userHostname="https://(.+?)"}', output)
  if result is None:
    raise Exception("Cannot get any result from cloudflared metrics")
  hostname = result.group(1)
  if hostname is None:
    raise Exception("Cannot get the hostname from cloudflared, it looks like the connection has failed.")
  return {
    "domain":hostname.strip(),
    "protocol":"",
    "port":22
  }

# def get_argo_tunnel_config():
# 	hostname = None
# 	for i in range(8):
# 		output = requests.get("http://127.0.0.1:45678/metrics").text
# 		result = re.search('cloudflared_tunnel_user_hostnames_counts{userHostname="https://(.+?)"}', output)
# 		if result is None:
# 			retry_after = 12/(1.5**i)
# 			print(f"Waiting for cloudflare connection: Retrying after {retry_after:.2f}s", end="\r")
# 			time.sleep(retry_after)
# 			continue
# 		hostname = result.group(1)
# 		break

# 	if hostname is None:
# 		raise Exception("Cannot get the hostname from cloudflared, it looks like the connection has failed.")

# 	return {
# 		"domain":hostname,
# 		"protocol":"",
# 		"port":22
# 	}