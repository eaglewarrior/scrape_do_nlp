from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'This package will just take twitter keys and topic you want to scrape and give summarya dn sentiment as output'
LONG_DESCRIPTION = 'This package will scrape google and twitter and if sentiment flag is on it will do sentiment analysis and give summarization as output, the package is modular enough and separate task can be done like only scraping only google text or twitter text etc '

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="scrape_do_nlp", 
        version=VERSION,
        author="Rinki Nag",
        author_email="accanymous@gmail.com",
        url="https://github.com/eaglewarrior/scrape_do_nlp",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["requests","urllib","time","spacy","bs4","wordcloud","matplotlib","nltk","re","unicodedata","tweepy","textblob","pandas","numpy","gensim"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)