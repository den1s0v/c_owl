# msg2table.py

import re



INPUT = "control-flow-statements-domain-messages.txt"

data = []

def main():
	with open(INPUT) as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			
			parse_line(line)
		
	for row in data:
		print(*["'%s'" % (x) for x in row], sep="\t")
		# '"%s"' % (x)
		# repr(x)
		
def parse_line(s):
	n, ru, en = s.split('\t')
	name = n.split(" ", maxsplit=1)[0]
	m = re.search(r'\s\(.+?\)', n)
	if m:
		name += m[0]
	
	data.append((
		len(data) + 1,
		name,
		  en
		  # pad_multiline(en)
	))


def pad_multiline(s, width=70):
	parts = [s[i:i+width] for i in range(0, len(s), width)]
	# sep = "\\"
	sep = "\x0D\x0A"
	return sep.join(parts)
	

if __name__ == '__main__':
	main()
	
