import os
import shutil
import pathlib
import struct
from glob import iglob

format_version = 14

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
	folder_path = os.path.join(decode_path, name)
	os.mkdir(folder_path)

	# parse containers.index
	if os.path.isfile(os.path.join(origin, "containers.index")):
		print("folder with container.index")

		with open(os.path.join(origin, "containers.index"), mode="rb") as container_file:
			header_data = struct.unpack("ll216s", container_file.read(224))

			version = header_data[0]
			print(f"Format version: {version}, {'matches' if version == format_version else 'VERSION MISMATCH'}")

			folder_count = header_data[1]
			print(f"Found {folder_count} folder entries")

			print(f"Header: {header_data[2].decode('ansi')}")
			with open(os.path.join(folder_path, "header.bin"), "wb") as header_file:
				header_file.write(header_data[2])
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