# Function to xor 2 hex strings a and b
def xor_hex_strings(a, b):
	new_a = a.decode("hex")
	new_b = b.decode("hex")
	return "".join([chr(ord(x)^ord(y)) for x,y in zip(new_a, new_b)]).encode("hex")

# Function to determine if a hex string represents an alphabet
def is_alpha(hex_str):
	if((ord(hex_str.decode("hex")) < ord("z") and ord(hex_str.decode("hex")) > ord("a")) or (ord(hex_str.decode("hex")) < ord("Z") and ord(hex_str.decode("hex")) > ord("A")) or hex_str.decode("hex") == " "):
		return 1
	return 0

# Taking hex string as input, convert the string into a character
# string consisting of alphabets, spaces or "*" to denote unidentified characters
def process_str(str_1):
	res = ""
	for i in range(0, len(str_1) - 1, 2):
		if(is_alpha(str_1[i : i + 2]) or str_1[i : i + 2] == " ".encode("hex")):
			res = res + str_1[i : i + 2].decode("hex")
		else:
			return "*" * (len(str_1)/2)
	return res

# Given a list of candidate keys, combine them to produce a final key
def reconstruct_key(key_list):
	final_key = ["00"] * 512
	for k in key_list:
		for i in range(0, 512):
			if final_key[i] == "00":
				final_key[i] = k[i]
	return "".join(final_key)

# Function to reconstruct the key used for message encryption
def get_key(inp_cipher_text):

	# Number of ciphertexts
	inp_len = len(inp_cipher_text)
	# List of characters/pairs that occur commonly in a sentence
	common_char_ls = [" ", "e", "t", "a", "o", "th", "he", "an", "."]
	
	# Store key candidates
	possible_keys = []

	# XOR every CT with the next 2 CT to get a strings 's1' and 's2'
	# XOR s1 and s2 with hex_common_char at every position
	# If one of the CT had the common phrase encoded in it, the resulting string will be a decoding of one of the CT
	for common_char in common_char_ls:
		# Since the key used is 1024 bytes long
		partial_key = ["00"] * 512

		# Hex encoding of common phrase
		hex_common_char = common_char.encode("hex")
		hex_char_len = len(hex_common_char)

		for i in range(0, inp_len):
			for j in range(0, inp_len - 2):

				xor_cipher_1 = xor_hex_strings(inp_cipher_text[(i % inp_len)], inp_cipher_text[(i + 1) % inp_len])
				xor_cipher_2 = xor_hex_strings(inp_cipher_text[i % inp_len], inp_cipher_text[(i + 2) % inp_len])

				len_1 = len(xor_cipher_1)
				len_2 = len(xor_cipher_2)

				#partial_str_1 = ""

				for j in range(0, min(len_1, len_2) - hex_char_len + 1, 2):
					xor_cipher_3 = xor_hex_strings(xor_cipher_1[j : ], hex_common_char)
					xor_cipher_4 = xor_hex_strings(xor_cipher_2[j : ], hex_common_char)
					processed_str_1 = process_str(xor_cipher_3)
					processed_str_2 = process_str(xor_cipher_4)

					for idx in range(len(processed_str_1)):
						if(is_alpha(processed_str_1[idx].encode("hex")) and is_alpha(processed_str_2[idx].encode("hex"))):
							#partial_str_1 = partial_str_1 + common_char
							partial_key[j/2] = xor_hex_strings(inp_cipher_text[i][(j + (idx * 2)) : (j + (idx * 2) + len(hex_common_char))], hex_common_char)

						# else:
						# 	partial_str_1 = partial_str_1 + "*" * len(hex_common_char)



			possible_keys.append(partial_key)

	new_key = reconstruct_key(possible_keys)

# Printing decrypted messages using new_key
##############################################################################
	# i = 1
	# for ct in inp_cipher_text:
	# 	print "i: " + str(i) + "\n"
	# 	print xor_hex_strings(ct, new_key).decode("hex")
	# 	a = raw_input()
	# 	i = i + 1
##############################################################################

# Checking output for each individual key candidate
##############################################################################
	# for k in possible_keys:
	# 	new_key = "".join(k)
	# 	for c in inp_cipher_text:
	# 		print xor_hex_strings(c, new_key).decode("hex")
	# 	print "-------------------------------------------"
	# 	a  = raw_input()
##############################################################################


if __name__ == "__main__":
	# List of cipher text as input
	inp_cipher_text = ["70d89ae1404439f3b426f905fd3d2525ec1a93ea0cb851273ef926f0c92d3bd979715dd00eff2ad9e35f68f39bff4b8a1c2d1409309a5bc4cb1f3f4f9a3b2de26c697928e7c3f44a758f275297eeb8a156bab08e3b5f39182a2cd5bb757845057c8bec88c8be2a8b33d5cec5b21dfc86e164e63d14d182446ba7d41fd97e6096338903c490f5fedacbadb0481ea0e712b85f38c481b2bfd13ea2d30b4b283ebed1dd67aeac", "70d0d4e40d1d3df4b869ac15f474286b800b9cfd4db2547975fb33eb8c683ed3672a09ee04e36f90f11366aacff9418a1b2d02022fc908c48d5b1146903121f9647c7928e382e45169c12d1b9de3ecee5afffd9b7e4876003078d5b97a3f430d39dfe293d4f36f9132d783c2f74fc6d2a061a73f15c1d64825a7d108df2a7d913cdd4ceb90f2fed09ea2bc090ea4a413b34c2986ee", "06f9dff348443be8f539ed05e1783e38e04e9afc0cbd5e2c75b629e6c92524db632b5df50eec2b90ee4a24b49af25dd95a6805032e845bca8d5c11509e3d30a1257c3128e482f44d3c952f5289eae1e218eeb592620c351b312ed9ad3b390a0e399eea88d5f974c538c7d784ea55d0c8ac29a03e0ed5d65623b5d54dd52d34953c9254e390e9f095f5a8b00c50e58e47b5512fc480b2a5d16ae7c10c557825a5d19021e5cb846eb44d612b61febdd68e6f246fa04ca1021b4ff6756827b4097f6075a8b067621881cfdf48b47ba91b3253720e1f41c624a924943dbd90da89c8267bae020b", "1bb1d7e1490178f5e46be11fb5702525a842dbee58fc5f3b36bc6ba39d202cc82b2b15ee18ad3898f1136bb5cff60ed91f25130039c908dbc85c114585756fff7d6b3165b0caf24979972500d6abf9bd18edb282774876152f28d9b569740a1733dff089debe2c972fd6c684f753c1c3ec65a32f159899476ba0c9089c2d75973e9251a190e7f4c6d1ada11c19a9be47bf5029c788e7a9d27be7c510516025a3c0903de4c38466b0442e6b07", "70d0d4e40d1d37f5b439e907f971356bbf0197f949b8103c21e66589", "70c3dfe1490d34f9af6bc546fd7c3a2eec1d94e35ab954753aad2fe69b3b6dd36d7f1ce94bec2d8af64171a08af94bd90568170932c90fc3c24a0b41983c62f861653c3ab0c5ef5b7d952500d481", "11f8c8e358092bf4f525ef03e6316c2aa20adbee0cbf552721b82eedc92a24dd787f12e14be02697e61f24bb8ee14b8a1a2d074c318c5bdfc21f0c419d3d62e5667c3c3bf5d1e91e758f60018fe8f0ee4af3b993774925587f39d2b03b315e43319efdc1ccfb23897ad0c684fa52c0c4f46ca26c16d0935523b1d34dd42b799f3cdd4ae3d7e3f8c0d7b5ad481fa4a947b55134db90e0bedd6ae7d317056d24bfd3dd28acc9c22da155656966f2f3ddc8382f69ad57f5181b41e3722629fa0f747720aea23e361d85969249a96aa55a3259260c185dd361b8768c3db993d498c8227ab2422d3e4d489662a9f26700ab", "1bff9ae64c072cacb423ed10fc732b6ba30098ea0cb9432134bb2bea9a2028d82b3c12e905e82c8de75724b281f30ec6132f0a0e308c5bc8c55e0a41952c27fe7b247900b0d1fe5f6e82251e83abffaf4efffd963b583e1b2a3fd4a03b2c45432897e1c1d6fb3d807ad6cac2f854d6d3ec7dbf6c0eded6452ea2c401d32e7d9035dd57e5d5efe495d7aca4070eb1e96d", "70d8d4a0590c3da0e439e915f073386baf0f88ea01f1593b31bc22e7c921239c6a3311a708ec3c9cf1136bb5cfe44bc9042d174c2b9b12dfc4511f0ddb2c2ae9286e303be3d6bd4f6984330693e4f6ee4affba96694825542b30d9f477394404299ee3849bf129c52edac684fd54c5cee57bfd6c07d784013fbcc44dcc2c7d90319453e1d5f5b6dad8e1a70710b0b30eb950768897fdebd87fb59e59407b3ab3d7d928e0cadd21f55c736979f3f89985203565ee4cbc1d1e40e73c6529e400746b26e7b73573508780dc44a36ce71f340c26180f42c66aae768223e5dfdc95cd7672af4921685e5f8c68a1a460578d0243e4b069bff926ac2347754288d16e1de360311100796017ebec084384c569ebd01ebe1e", "1bff9ae7480a3df2f527a046e1752939a94e92fc0cb25f7534b533e69b262cc8622918a709f83bd9e74b74b69dfe43cf183c4344388009cece4b1d44d63a3bac787a362bf1c0f4527595291789a2b8a15ebab8817e5e2f542b37d2b36e3d0a083290f38f9bea20c532dbce84e955da86e17db2290cc882526ba0c9089c2d7b9227894ae2deaab6c0d0b5bd045cb1af02f64a28dd81b2a4d07be7d01c05693ea2d5d927e9c28a07", "10e4ceac0d1331f4fc6bf80ef03d2f22bc069efd0cb25f2275bb22e5863a289c7e2c51a70ae123d9e65a62b586f45bc6023143052fc909cec0500e45927820f5287c312cb0d1f4597280340788eeb6ee6cf2b8d76b59385430369ca0733d0a14338de0c19cd526813e9583cded1dd4d6f07ba32f08d9944d2ef4c8039c307bde3d894be8c2a6fad4d0a6a1091ba0e713be5f348890faae9e5ba9d5154c7b22f8be", "10e4cea04b0b2aa0e023e515b57e2325bf079fea5ebd443c3ab767cac93b25d37e3319a703ec399ca25161b49af90ec70f680218288c16dbd94c58579f2c2aac7c603c69c3d2fc50759228529be5fcee7ee8b89978447a543e2b9ca0733d0a173391e394deed6f8c3492d4ccf75edd86e129b52902ca93556bbbc74dc8367d8d72964ae3d4a6e1dacbadb04811aab413f6503bdc91e0aad272be9211447e2ff6d6d52ce286d37fbc49742c63bbffc0c82e6770a74db4040b0ced7a2634fc0d314a25a6b82e6518c482d34ea830a93b23006f084a45c277e676a46da88cce8ec43377fd58697b1f4e9774b5f06d49d34347e4f53db7bc2aa076713b4a8298691da8a2c1ed78", "58", "72b19ac3420a3ff2f53ff90af4692524a21dd7af55b345753db831e6c92f22c87f3a13a71fe5268aa25565a1c1b70ee8033c4315339c5cd9c81f164f827826e3666d7930f5d6bc34", "72b19ad9421178e3f525ac00fc73286bb8069eaf5eb9432175b621a39d20289c633010e21ce23d92a24376bc8dfb4bc705680b092e8c41a1", "72b19ae8591028f3ae64a311e26a6228a51dd5fa5cb95e3b7bbc23f6c6362ed5786a48b144e538c8ad5b73e2c2f45cd3063c0c422c8d1da1"]
	new_key = get_key(inp_cipher_text)
# 	# Obtaining a new_key everytime after observing the outputs, guessing words and modifying the key manually
	new_key = "5291ba802d645880944b8c66951d4c4bcc6efb8f2cdc305555d94783e9484dbc0b5f7d876b8d4ff9823304d3ef972eaa7648636c5ce97babad3f7820f658428c0808594990a29d3e1ce14072fa8b98ce389addf71b2c56745f58bcd41b582a635cff84e1bb9e4fe55ab2a3a49e3db5a68009c64c61b8f6214bd4a16dbc5e14fe52fd238db08696b5bec1d4687cc5c767d63e5aa8e492cbbe1ec7b27925084ad6b4b0498ca6a40dd53d00490d9b9db9e84f4700ce3fd5706e2c821c06409468111955c7d6471670e4efb227c61e897a5020067c6a32a304ca56ed4dc9ffbdfba95613dd2c011e3f2de50dc584022ea122378cd549d89c48c55634552deef11a7586404170720d09749e806931a4ac0d82bf7390"
	print "New key: " + new_key + "\n"
	i = 1
	for ct in inp_cipher_text:
		print "Message " + str(i) + ": "
		print xor_hex_strings(ct, new_key).decode("hex")
		i = i + 1
		#Pausing to observe inputs
		#a = raw_input()



	

		










