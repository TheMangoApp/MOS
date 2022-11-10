import gc
import requests
import hashlib


class Updater:
    raw = "https://raw.githubusercontent.com"
    github = "https://github.com"
    def __init__(self, user, repo, url=None, branch="master", working_dir="app", files=["boot.py", "main.py"], headers={}):
        self.base_url = "{}/{}/{}".format(self.raw, user,repo) if user else url.replace(self.github, self.raw)
        self.url = url if url is not None else "{}/{}/{}".format(self.base_url, branch, working_dir)
        self.headers = headers
        self.files = files
    def _check_hash(self, x, y):
        x_hash = hashlib.sha1(x.encode())
        y_hash = hashlib.sha1(y.encode())
        x = x_hash.digest()
        y = y_hash.digest()
        if str(x) == str(y):
            return True
        else:
            return False
    def _get_file(self, url):
        payload = requests.get(url, headers=self.headers)
        code = payload.status_code
        if code == 200:
            return payload.text
        else:
            return None
    def _check_all(self):
        changes = []
        for file in self.files:
            latest_version = self._get_file(self.url + "/" + file)
            if latest_version is None:
                continue
            try:
                with open(file, "r") as local_file:
                    local_version = local_file.read()
            except:
                local_version = ""
            if not self._check_hash(latest_version, local_version):
                changes.append(file)
        return changes
    def fetch(self):
        if not self._check_all():
            return False
        else:
            return True
    def update(self):
        changes = self._check_all()
        for file in changes:
            with open(file, "w") as local_file:
                local_file.write(self._get_file(self.url + "/" + file))
        if changes:
            return True
        else:
            return False

def ota():
    """Main function. Runs after boot, before main.py
    Checks for latest OTA version.
    """

    gc.collect()
    gc.enable()
    OTA = Updater(user="", repo="", branch="stable", working_dir="src", files=[
                          "main.py", "boot.py", "boot_lib.py"])

    if OTA.fetch():
        print("A newer version is available!")
        print("Do you want to update? (Y/N)")
        if input("$ ").lower() == "y":
            OTA.update()
            print("Updated to the latest version! Reloading the OS")
            return "RELOAD"
    else:
        print("Up to date!")
        return "OTA__OK"
