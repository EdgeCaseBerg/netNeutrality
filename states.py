#pip install lxml
from lxml import etree

datafiles = [
	"14-28-RAW-Solr-1.xml",
	"14-28-RAW-Solr-2.xml",
	"14-28-RAW-Solr-3a.xml",
	"14-28-RAW-Solr-3b.xml",
	"14-28-RAW-Solr-4.xml",
	"14-28-RAW-Solr-5.xml"
]

#Set this to the folder path where you unzipped the xml datasets
datadir = "unzipped"

def main():
	numMessagesByState = {}
	doms = []
	for datafile in datafiles:
		dom = None
		print "Reading data file: {}/{}".format(datadir,datafile)
		try:
			dom = etree.parse("{}/{}".format(datadir,datafile) )
		except Exception, e:
			print e
		if not dom:
			continue

		comments = dom.getroot().getchildren()[1]
		docs = comments.xpath("doc")
		for doc in docs:
			states = doc.xpath("arr[@name='stateCd']/str")
			for state in states:
				state = state.text
				if state in numMessagesByState:
					numMessagesByState[state] += 1
				else:
					numMessagesByState[state] = 1
		

	print numMessagesByState
	

if __name__ == "__main__":
	main()



 

 
