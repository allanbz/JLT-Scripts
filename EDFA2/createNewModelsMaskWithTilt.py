'''
	This script reads all EDFA_2STG mask files, get only the 'new_models' attributes
	(Gset, Pin[40], Pout[40], NF[40]) and adds tilt value to each signal.
	It then save all data in a single file, in random order.
'''

import numpy as np

path = "EDFA_2STG/result_allMask_40channels_EDFA2STG_In_Tilt_"
dB = "dB"
extension = ".txt"
flat_label = "Flat"
output_file = "masks/mask-edfa2-padtec-new-models-with-tilt.txt"

tilts = [2, 5, 8]
number_of_channels = 40

def read_files_for_each_tilt(data, tilts):
	for i in range(len(tilts)):
		# Positive mask
		input_file = path + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			line = [0] * 122
			line[0] = float(auxiliary[6])				# G_set
			line[41] = float(tilts[i])					# Tilt
			for k in range(0, number_of_channels):
				line[1+k] = float(auxiliary[9+k])		# P_in (channel)
				line[42+k] = float(auxiliary[49+k])		# P_out (channel)
				line[82+k] = float(auxiliary[129+k])	# NF (channel)
			data.append(line)

		# Negative mask
		input_file = path + '-' + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			line = [0] * 122
			line[0] = float(auxiliary[6])				# G_set
			line[41] = float('-' + str(tilts[i]))		# Tilt
			for k in range(0, number_of_channels):
				line[1+k] = float(auxiliary[9+k])		# P_in (channel)
				line[42+k] = float(auxiliary[49+k])		# P_out (channel)
				line[82+k] = float(auxiliary[129+k])	# NF (channel)
			data.append(line)

def include_flat_mask(data):
	input_file = path + flat_label + extension
	with open(input_file, 'r') as f_in:
		entries = f_in.readlines()
	for j in range(0, len(entries)):
		auxiliary = entries[j].split()
		line = [0] * 122
		line[0] = float(auxiliary[6])				# G_set
		line[41] = float(0)							# Tilt
		for k in range(0, number_of_channels):
			line[1+k] = float(auxiliary[9+k])		# P_in (channel)
			line[42+k] = float(auxiliary[49+k])		# P_out (channel)
			line[82+k] = float(auxiliary[129+k])	# NF (channel)
		data.append(line)

# Reading all files
data = []
read_files_for_each_tilt(data, tilts)
include_flat_mask(data)

# Randomize signals
np.random.shuffle(data)

# Write data in output file
with open(output_file, 'w') as f_out:
	for line in data:
		f_out.write("".join([str(value) + " " for value in line]))
		f_out.write('\n')