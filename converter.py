import os
import shutil
import pathlib
import struct
from glob import iglob

format_version = 14

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
			# parse header
			header_data = struct.unpack("ll216s", container_file.read(224))

			version = header_data[0]
			print(f"Format version: {version}, {'matches' if version == format_version else 'VERSION MISMATCH'}")

			folder_count = header_data[1]
			print(f"Found {folder_count} folder entries")

			print(f"Header: {header_data[2].decode('utf16')}")
			with open(os.path.join(folder_path, "header.bin"), "wb") as header_file:
				header_file.write(header_data[2])

			# read entries
			for i in range(0, folder_count):
				name_length = struct.unpack("i", container_file.read(4))[0] * 2
				# print(f"Name of entry {i} has length {name_length}")

				entry_name = container_file.read(name_length).decode("utf16")
				print(f"Entry {i}: {entry_name}")

				# skip 4 random bytes
				container_file.read(4)

				# x: unknown data
				x_length = struct.unpack("i", container_file.read(4))[0] * 2
				x_data = container_file.read(x_length)

				# skip 5 random bytes
				container_file.read(5)

				entry_path = decodeFolderName(container_file.read(16).hex().upper())
				print(entry_path)

				container_file.read(24)

	# recursion

	# parse container.*
	# create files

	pass

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
	# clean up
	try:
		shutil.rmtree(decode_path)
	except:
		pass

	pathlib.Path(decode_path).mkdir(parents=True, exist_ok=True) 

	decodeFolder("root", container_path, decode_path)

# ....U.E.4.C.o.n.f.i.g.F.i.l.e.C.o.n.t.a.i.n.e.r.U.W.P.........".0.x.8.D.8.B.A.4.0.D.B.5.E.A.4.F.2.".+....*Në..8`E¤qÃ..-.. .”¯)ìÖ.........Ï.......
# ....U.E.4.S.a.v.e.G.a.m.e.F.i.l.e.C.o.n.t.a.i.n.e.r.........".0.x.8.D.8.B.A.3.C.1.A.9.B.D.1.C.2."......)òÜrYˆ]Lºã¨.I..¨ Á:U$ìÖ..........õ......
# 19 00 00 00 55 00 45 00 34 00 43 00 6F 00 6E 00 66 00 69 00 67 00 46 00 69 00 6C 00 65 00 43 00 6F 00 6E 00 74 00 61 00 69 00 6E 00 65 00 72 00 55 00 57 00 50 
# 18 00 00 00 55 00 45 00 34 00 53 00 61 00 76 00 65 00 47 00 61 00 6D 00 65 00 46 00 69 00 6C 00 65 00 43 00 6F 00 6E 00 74 00 61 00 69 00 6E 00 65 00 72
# 00 00 00 00 00 13 00 00 00 22 00 30 00 78 00 38 00 44 00 38 00 42 00 41 00 34 00 30 00 44 00 42 00 35 00 45 00 41 00 34 00 46 00 32 00 22 00 2B 01 00 00 00 2A 4E EB 1E 15 38 60 45 A4 71 C3 7F 15 2D 17 09 A0 14 94 AF 29 EC D6 01 00 00 00 00 00 00 00 00 CF 17 00 00 00 00 00 00
# 00 00 00 00 00 13 00 00 00 22 00 30 00 78 00 38 00 44 00 38 00 42 00 41 00 33 00 43 00 31 00 41 00 39 00 42 00 44 00 31 00 43 00 32 00 22 00 09 01 00 00 00 29 F2 DC 72 59 88 5D 4C BA E3 A8 2E 49 14 0B A8 20 C1 3A 55 24 EC D6 01 00 00 00 00 00 00 00 00 90 F5 02 00 00 00 00 00

# containers.index
# 1E EB 4E 2A   38 15   45 60   A4 71 C3 7F 15 2D 17 09 decoded
# 2A 4E EB 1E   15 38   60 45   A4 71 C3 7F 15 2D 17 09 encoded
