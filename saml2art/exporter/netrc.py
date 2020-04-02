import netrc
import os


class NetrcExporter:
    def export(self, path, host, username, password):
        print("Updating [%s]..." % path, end="")
        netrc_file = netrc.netrc(os.path.expanduser(path))
        netrc_file.hosts[host] = (username, None, password)
        with open(os.path.expanduser(path), "w") as file:
            file.write(netrc_file.__repr__())
        print("Done!")
