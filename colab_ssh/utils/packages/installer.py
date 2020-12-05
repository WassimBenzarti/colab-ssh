import apt, os

def create_deb_installer():
	os.system("apt-get -qq update")
	return install_deb_package

def install_deb_package(package_name):
	if not package_name:
		raise Exception("Package name not provided")

	cache = apt.Cache()
	if cache[package_name].is_installed:
		print("DEBUG: Skipping installation of {package_name}, package already installed")

	os.system(f"apt-get -qq install {package_name} > /dev/null")