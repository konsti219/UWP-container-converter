import os
import shutil
import pathlib
from glob import iglob

for result in iglob(os.environ["LOCALAPPDATA"] + "\\Packages\\SystemEraSoftworks*"):
    SES_path = result
print(f"SES path found in appadata: {result}")
decode_path = os.path.join(SES_path, "SystemAppData-decode")

for result in iglob(SES_path + "\\SystemAppData\\wgs\\*"):
	if os.path.basename(result) != "t":
		container_path = result
print(f'container path found: {container_path}')

def decodeFolder(name, origin, destination):
	# name: name of the folder
	# origin: path to the folder (with encoded hex folder id) (the dir where container.* can be found)
	# destination: path where the folder is supposed to go (without folder name)

	print(f"decoding {origin}")

	# create folder
	os.mkdir(os.path.join(decode_path, name))

	# parse containers.index
	if os.path.isfile(os.path.join(origin, "containers.index")):
		print("folder with container.index")

		with open(os.path.join(origin, "containers.index"), mode="rb") as container_file:
			file_content = container_file.read()
			print(file_content)
	# recursion

	# parse container.*
	# create files

	pass

if __name__ == "__main__":
	# clean up
	try:
		shutil.rmtree(decode_path)
	except:
		pass

	pathlib.Path(decode_path).mkdir(parents=True, exist_ok=True) 

	decodeFolder("root", container_path, decode_path)