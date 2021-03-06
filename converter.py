import os
import shutil
import sys
import pathlib
import struct
import secrets
from glob import iglob

containers_version = 14
container_version = 4

# pylint: disable=unused-variable

for result in iglob(os.environ["LOCALAPPDATA"] + "\\Packages\\SystemEraSoftworks*"):
    SES_path = result
print(f"SES path found in appadata: {result}")
decode_path = os.path.join(SES_path, "SystemAppData-decode")

for result in iglob(SES_path + "\\SystemAppData\\wgs\\*"):
	if os.path.basename(result) != "t":
		container_path = result
print(f'Container path found: {container_path}')

def decodeFolder(name, origin, destination):
	print(f"Decoding folder {origin}")

	# create folder
	folder_path = os.path.join(destination, name)
	os.mkdir(folder_path)

	# parse container.*
	for result in iglob(origin + "\\container.*"):
		print("Folder with container.*")
		
		with open(result, mode="rb") as container_file:
			# parse header
			header_data = struct.unpack("ll", container_file.read(8))

			version = header_data[0]
			print(f"Format version: {version}, {'matches' if version == container_version else 'VERSION MISMATCH'}")

			file_count = header_data[1]
			print(f"Found {file_count} file entries")

			# read entries
			for i in range(0, file_count):
				entry_name = (container_file.read(144).split(b"\x00" * 2)[0] + b"\x00").decode("utf16")
				print(f"File entry {i}: {entry_name}")

				entry_filename = encodeName(container_file.read(16).hex().upper())

				with open(os.path.join(origin, entry_filename), mode="rb") as origin_file:
					with open(os.path.join(folder_path, entry_name), "wb") as dest_file:
						dest_file.write(origin_file.read())


def encodeFolder(origin, destination, container_num):
	print(f"encoding {origin}")

	# create folder
	os.mkdir(destination)

	# check for files and encode
	files = [name for name in os.listdir(origin) if os.path.isfile(os.path.join(origin, name))]
	print(files)
	
	with open(os.path.join(destination, "container." + str(int.from_bytes(container_num, "big"))), mode="ab") as container_file:
		# create header
		container_file.write(struct.pack("ll", container_version, len(files)))

		# write entries
		for file_name in files:
			entry_name = file_name.encode("utf16")[2:]

			container_file.write(entry_name)
			container_file.write(b"\00" * (144 - len(entry_name)))

			file_key = secrets.token_bytes(16)
			container_file.write(file_key)

			with open(os.path.join(origin, file_name), mode="rb") as origin_file:
				with open(os.path.join(destination, encodeName(file_key.hex().upper())), "wb") as dest_file:
					dest_file.write(origin_file.read())

def readContainers(folder_name):
	# parse containers.index
	print("Parsing containers.index")

	with open(os.path.join(container_path, "containers.index"), mode="rb") as container_file:
		# parse header
		header_data = struct.unpack("ll216s", container_file.read(224))

		version = header_data[0]
		print(f"Format version: {version}, {'matches' if version == containers_version else 'VERSION MISMATCH'}")

		folder_count = header_data[1]
		print(f"Found {folder_count} folder entries")

		# read entries
		for i in range(0, folder_count):
			# get length of entry name
			name_length = struct.unpack("i", container_file.read(4))[0] * 2

			# read entry with length of name + remainder
			entry_data = struct.unpack(f"{name_length}s46xs4x16s24x", container_file.read(name_length + 91))
			entry_name = entry_data[0].decode("utf16")

			print(f"Folder entry {i}: {entry_name}")

			if (entry_name == folder_name):
				return (encodeName(entry_data[2].hex().upper()), entry_data[1])
	
def encodeName(name):
	result = ""

	result = result + name[6:8]
	result = result + name[4:6]
	result = result + name[2:4]
	result = result + name[0:2]
	result = result + name[10:12]
	result = result + name[8:10]
	result = result + name[14:16]
	result = result + name[12:14]
	result = result + name[16:32]

	return result

if __name__ == "__main__":
	pathlib.Path(decode_path).mkdir(parents=True, exist_ok=True)

	container_data = readContainers("UE4SaveGameFileContainer")
	saves_path = os.path.join(container_path, container_data[0])
	container_num = container_data[1]
	
	if len(sys.argv) > 1:
		if sys.argv[1] == "-d":
			try:
				shutil.rmtree(os.path.join(decode_path, "saves"))
			except:
				pass

			decodeFolder("saves", saves_path, decode_path)

		elif sys.argv[1] == "-e":
			try:
				shutil.rmtree(saves_path)
			except:
				pass

			encodeFolder(os.path.join(decode_path, "saves"), saves_path, container_num)
		else:
			print("specify -d or -e")
	else:
		print("specify -d or -e")

