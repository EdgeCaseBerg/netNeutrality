#pip install lxml
from lxml import etree

#pip install nltk
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

#nltk.download()
from nltk.corpus import movie_reviews

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


def word_feats(words):
    return dict([(word, True) for word in words])

def trainNaiveClassifier():
	negids = movie_reviews.fileids('neg')
	posids = movie_reviews.fileids('pos')
	 
	negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
	posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
	 
	negcutoff = len(negfeats)*3/4
	poscutoff = len(posfeats)*3/4
	 
	trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
	testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
	print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
	 
	classifier = NaiveBayesClassifier.train(trainfeats)
	print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
	classifier.show_most_informative_features()
	return classifier

def main():
	classifier = trainNaiveClassifier()
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
		for comment in comments:
			print classifier.classify(  word_feats(comment.xpath("arr[@name = 'text']/str")[0].text) )
	

if __name__ == "__main__":
	main()



 

 
