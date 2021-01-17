import os
import shutil
import sys
import pathlib
import struct
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
print(f'container path found: {container_path}')

def decodeFolder(name, origin, destination):
	# name: name of the folder
	# origin: path to the folder (with hex folder) (the dir where container.* can be found)
	# destination: path where the folder is supposed to go (without folder name)

	print(f"decoding {origin}")

	# create folder
	folder_path = os.path.join(destination, name)
	os.mkdir(folder_path)

	# parse containers.index
	if os.path.isfile(os.path.join(origin, "containers.index")):
		print("Folder with containers.index")

		with open(os.path.join(origin, "containers.index"), mode="rb") as container_file:
			# parse header
			header_data = struct.unpack("ll216s", container_file.read(224))

			version = header_data[0]
			print(f"Format version: {version}, {'matches' if version == containers_version else 'VERSION MISMATCH'}")

			folder_count = header_data[1]
			print(f"Found {folder_count} folder entries")

			print(f"Header: {header_data[2].decode('utf16')}")
			with open(os.path.join(folder_path, "header.bin"), "wb") as header_file:
				header_file.write(header_data[2])

			# read entries
			for i in range(0, folder_count):
				# get length of entry name
				name_length = struct.unpack("i", container_file.read(4))[0] * 2

				# read entry wit length of name + reminder
				entry_data = struct.unpack(f"{name_length}s51x16s24x", container_file.read(name_length + 91))
				entry_name = entry_data[0].decode("utf16")

				print(f"Folder entry {i}: {entry_name}")

				# recursion
				decodeFolder(entry_name, os.path.join(origin, decodeFolderName(entry_data[1].hex().upper())), folder_path)

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

				entry_filename = decodeFolderName(container_file.read(16).hex().upper())

				with open(os.path.join(origin, entry_filename), mode="rb") as origin_file:
					with open(os.path.join(folder_path, entry_name), "wb") as dest_file:
						dest_file.write(origin_file.read())





def encodeFolder(origin, destination):
	# origin: path to the folder (with folder name)
	# destination: path where the folder is supposed to go (with hex folder name)

	print(f"encoding {origin}")

	# create folder
	os.mkdir(destination)

	# check for subfolders and encode
	sub_folders = [ name for name in os.listdir(origin) if os.path.isdir(os.path.join(origin, name)) ]
	print(sub_folders)
	if len(sub_folders) > 0:
		print("Folder with subfolders")

		# create containers.index
		with open(os.path.join(destination, "containers.index"), mode="ab") as container_file:
			with open(os.path.join(origin, "header.bin"), "rb") as header_file:
				container_file.write(struct.pack("ll216s", containers_version, len(sub_folders), header_file.read(216)))

			print(f"Creating {len(sub_folders)} folders")

			# read entries
			for i in range(0, len(sub_folders)):
				pass
				# get length of entry name
				#name_length = struct.unpack("i", container_file.read(4))[0] * 2

				# read entry wit length of name + reminder
				#entry_data = struct.unpack(f"{name_length}s51x16s24x", container_file.read(name_length + 91))
				#entry_name = entry_data[0].decode("utf16")

				#print(f"Folder entry {i}: {entry_name}")

				# recursion
				#decodeFolder(entry_name, os.path.join(origin, decodeFolderName(entry_data[1].hex().upper())), folder_path)

	# check for files and encode
	files = [name for name in os.listdir(origin) if os.path.isfile(os.path.join(origin, name)) and name != "header.bin"]
	print(files)
	if len(files) > 0:
		print("Folder with files")
	
def decodeFolderName(name):
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
	
	if len(sys.argv) > 1:
		if sys.argv[1] == "-d":
			# decode

			# clean up
			try:
				shutil.rmtree(os.path.join(decode_path, "root"))
			except:
				pass

			decodeFolder("root", container_path, decode_path)

		elif sys.argv[1] == "-e":
			# encode

			# clean up
			try:
				shutil.rmtree(container_path)
			except:
				pass

			encodeFolder(os.path.join(decode_path, "root"), container_path)
		else:
			print("specify -d or -e")
	else:
		print("specify -d or -e")

# ....U.E.4.C.o.n.f.i.g.F.i.l.e.C.o.n.t.a.i.n.e.r.U.W.P.........".0.x.8.D.8.B.A.4.0.D.B.5.E.A.4.F.2.".+....*Në..8`E¤qÃ..-.. .”¯)ìÖ.........Ï.......
# ....U.E.4.S.a.v.e.G.a.m.e.F.i.l.e.C.o.n.t.a.i.n.e.r.........".0.x.8.D.8.B.A.3.C.1.A.9.B.D.1.C.2."......)òÜrYˆ]Lºã¨.I..¨ Á:U$ìÖ..........õ......
# 19 00 00 00 55 00 45 00 34 00 43 00 6F 00 6E 00 66 00 69 00 67 00 46 00 69 00 6C 00 65 00 43 00 6F 00 6E 00 74 00 61 00 69 00 6E 00 65 00 72 00 55 00 57 00 50 
# 18 00 00 00 55 00 45 00 34 00 53 00 61 00 76 00 65 00 47 00 61 00 6D 00 65 00 46 00 69 00 6C 00 65 00 43 00 6F 00 6E 00 74 00 61 00 69 00 6E 00 65 00 72
# 00 00 00 00 00 13 00 00 00 22 00 30 00 78 00 38 00 44 00 38 00 42 00 41 00 34 00 30 00 44 00 42 00 35 00 45 00 41 00 34 00 46 00 32 00 22 00 2B 01 00 00 00 2A 4E EB 1E 15 38 60 45 A4 71 C3 7F 15 2D 17 09 A0 14 94 AF 29 EC D6 01 00 00 00 00 00 00 00 00 CF 17 00 00 00 00 00 00
# 00 00 00 00 00 13 00 00 00 22 00 30 00 78 00 38 00 44 00 38 00 42 00 41 00 33 00 43 00 31 00 41 00 39 00 42 00 44 00 31 00 43 00 32 00 22 00 09 01 00 00 00 29 F2 DC 72 59 88 5D 4C BA E3 A8 2E 49 14 0B A8 20 C1 3A 55 24 EC D6 01 00 00 00 00 00 00 00 00 90 F5 02 00 00 00 00 00

# containers.index
# 1E EB 4E 2A   38 15   45 60   A4 71 C3 7F 15 2D 17 09 decoded
# 2A 4E EB 1E   15 38   60 45   A4 71 C3 7F 15 2D 17 09 encoded

# container.index
# 8932F30E 7583 4A37 986D352A5160E516 decoded
# 0EF33289 8375 374A 986D352A5160E516 encoded
