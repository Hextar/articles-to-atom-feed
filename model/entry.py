import uuid
from datetime import datetime


# A Class of support representing an Atom Entry
class Entry:
	id = ''
	authors = []
	title = ''
	link = ''
	updated = ''
	text = ''
	summary = ''

	def __init__(self, link, authors, title, text, summary): 
		self.id = uuid.uuid1().hex
		self.authors = authors
		self.title = title
		self.link = link
		self.updated = datetime.now().isoformat()+'Z'
		self.text = text
		self.summary = summary