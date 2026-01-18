# Get MODRINTH_PROJECTS list according to modrinth.index.json

# 1. Create new instance in Modrinth client
# 2. Add all the mods you want
# 3. Make sure everything is working correctly by running the game
# 4. Back to Modrinth client, export your instance as modpack
# 5. Unzip the exported file to get modrinth.index.json
# 6. Run this script with the path to your modrinth.index.json

import re
import sys
import json

from requests import request


MODRINTH_API_URL="https://api.modrinth.com/v2"

class ModrinthMod:

  def __init__(self, s):
    pattern = r"/data/([^/]+)/versions/([^/]+)/"
    match = re.search(pattern, s)
    self.project_id = match.group(1)
    self.version_id = match.group(2)

  def get_project_slug(self):
    return request(
      method="GET",
      url=f"{MODRINTH_API_URL}/project/{self.project_id}"
    ).json()["slug"]

  def get_version_number(self):
    return request(
      method="GET",
      url=f"{MODRINTH_API_URL}/version/{self.version_id}"
    ).json()["version_number"]

  def __str__(self):
    slug = self.get_project_slug()
    version_number = self.get_version_number()
    return f"{slug}:{version_number}"

  def __repr__(self):
    return str(self)


def modrinth_print(pathStart, prefix):
  print(f"# {pathStart.capitalize()}")
  data = json.load(open(sys.argv[1], "r"))
  downloads = [download for file in data["files"] for download in file["downloads"] if file["path"].startswith(pathStart)]
  mods = [prefix + str(ModrinthMod(s)) for s in downloads]
  for mod in sorted(mods):
    print(mod)

if __name__ == "__main__":
  modrinth_print("resourcepacks", "resourcepack:")
  modrinth_print("datapacks", "datapack:")
  modrinth_print("mods", "")
