import netrc
import os


class NetrcExporter:
    def export(self, path, host, username, password):
        print("Updating [%s]..." % path, end="")
        netrc_file_path = os.path.expanduser(path)
        if os.path.exists(netrc_file_path):
            netrc_file = netrc.netrc(netrc_file_path)
        else:
            netrc_file = netrc.netrc()
        netrc_file.hosts[host] = (username, None, password)
        with open(os.path.expanduser(path), "w+") as file:
            file.write(netrc_file.__repr__())
        print("Done!")
