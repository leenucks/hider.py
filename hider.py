import base64
import sys


def EncodeBase64(encodingText):

	return (base64.b64encode(encodingText.encode('ascii')).decode('ascii'))

def DecodeBase64(decodingText):

	return (base64.b64decode(decodingText.encode('ascii')).decode('ascii'))

def Obfuscate(text, file, password):

	text = EncodeBase64(text)
	password = EncodeBase64(password)
	passwd = [x for x in password]

	n = 0
	for _ in range(0, len(passwd)+1):
		text = text.replace(passwd[n:n+2][1], '!')
		text = text.replace(passwd[n:n+2][0], passwd[n:n+2][1])
		text = text.replace('!', passwd[n:n+2][0])
		n += 2
		if passwd[n:n+2] == []: break

	text = text.encode('ascii').hex()
	newFile = file.replace('py', 'Obfuscated.py') if file.split('.')[-1] == 'py' else f'{file}.Obfuscated'

	with open(newFile, 'w') as f:
		f.write(text)
		f.close()
	print(f'Done Obfuscating {file} --> {newFile}')

def Deobfuscate(text, file, password):

	text = bytes.fromhex(text).decode('ascii')
	password = EncodeBase64(password)
	passwd = [x for x in password]
	passwd = passwd[::-1]
	n = 0
	for _ in range(0, len(passwd)+1):
		text = text.replace(passwd[n:n+2][1], '!')
		text = text.replace(passwd[n:n+2][0], passwd[n:n+2][1])
		text = text.replace('!', passwd[n:n+2][0])
		n += 2
		if passwd[n:n+2] == []: break

	text = DecodeBase64(text)
	newFile = file.replace('py', 'Deobfuscated.py') if file.split('.')[-1] == 'py' else f'{file}.Deobfuscated'

	with open(newFile, 'w') as f:
		f.write(text)
		f.close()
	print(f'Done Deobfuscating {file} --> {newFile}')

methodsAllowed = {
	'o' : Obfuscate,
	'd' : Deobfuscate,
}

try:
	method, file, password = sys.argv[1], sys.argv[2], sys.argv[3]
	if method.lower() not in methodsAllowed.keys(): raise IndexError

except IndexError:

	print(
	f'''\nUsage : python3 {sys.argv[0]} [method] [file] [password]\n
	Method [allowed : o/d (obfuscate/deobfuscate)]
	File [*.py/*.*]
	Password [U know this :)]
	Example : python3 {sys.argv[0]} o tosecure.py thisispassword'''
		)
	sys.exit(0)

try:

	with open(file, 'r') as f:
		text = f.read()
		f.close()

except FileNotFoundError: print(f'U sure about existence of file : {file}\nTry again!!'); sys.exit(0)

if __name__ == '__main__':

	print("\n\tHIDER.py v1.0 @d34r0\n\t~ (Ob/Deob)fuscate your *.py/(*.*) scripts with Password...\n")
	try: methodsAllowed[method](text, file, password)
	except Exception as e:  print("Only Input Files Obfuscated with this tool...\n or maybe password's wrong!!\n"); sys.exit(0)
