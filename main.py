from urllib.request import urlopen
from urllib.error import URLError
from xml.etree.ElementTree import fromstring, ParseError


def get_url():
	"""Get an RSS feed URL from the user and return it."""
	url = input('Enter an RSS feed URL (Or leave blank to quit): ')
	print()
	return url


def read(url):
	"""Read and print the title/description/link for each RSS item in {url}."""
	try:
		# Extract the XML document into a bytestring {xml}.
		with urlopen(url) as response:
			xml = response.read()
	except (ValueError, URLError) as e:
		print(f'Ran into a problem while parsing your URL ({url}):\nException: {e}\n')
	else:
		try:
			# Transform the XML bytestring {xml} into an ElementTree {root}.
			root = fromstring(xml)
		except ParseError:
			print(f'Ran into a problem while parsing your URL ({url}):\nException: {url} is not a valid XML document\n')
		else:
			# Iterate through all RSS channel items in the ElementTree {root}.
			for item in root.findall('./channel/item'):
				print_text(item, 'title')
				print_text(item, 'description')
				print_text(item, 'link')
				print()


def print_text(element, tag):
	"""Print the XML {tag}'s text field within {element}."""
	caps_tag = tag[0].upper() + tag[1:]
	
	try:
		print(f'{caps_tag}: {element.find(tag).text}')
	except AttributeError:
		print(f'{caps_tag}: NULL')


def main():
	"""Main loop to allow the user to enter multiple RSS feed URLs."""
	url = get_url()
	
	while url != '':
		read(url)
		url = get_url()


if __name__ == '__main__':
	main()
