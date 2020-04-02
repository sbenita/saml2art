import netrc
import os
from pathlib import Path


class NetrcExporter:
    def export(self, path, host, username, password):
        print("Updating [%s]..." % path, end="")
        netrc_file_path = os.path.expanduser(path)
        if not os.path.exists(netrc_file_path):
            Path(netrc_file_path).touch()
        netrc_file = netrc.netrc(netrc_file_path)
        netrc_file.hosts[host] = (username, None, password)
        with open(os.path.expanduser(path), "w+") as file:
            file.write(netrc_file.__repr__())
        print("Done!")
