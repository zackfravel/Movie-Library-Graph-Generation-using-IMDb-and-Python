# Zack Fravel
# ECE508 - Python Workshop
# Spring 2021
# Final Project
#
# filename: movie.py
#
# description: Formal definition of a 'movie' class that utilizes the
#   IMDB python library to store movie attributes to be used
#   in the graph program. Primary references are the IMDbPY Documentation
#   Release 6.8 by Davide Alberani and H. Turgut Uyar.
#
# library references:
#   https://buildmedia.readthedocs.org/media/pdf/imdbpy/stable/imdbpy.pdf
#

from imdb import IMDb


# Movie Class Definition
class Movie:
	# Private variables
	__name = ""
	__year = ""
	__directors = ""
	__writers = ""
	__actors = ""
	__cinematographers = ""
	__producers = ""
	__composers = ""
	__genres = ""
	__plot = ""
	__runtime = ""
	__coverURL = ""
	__object = ""

	# Return name function
	def name(self):
		return self.__name

	# Return year function
	def year(self):
		return self.__year

	# Return directors function
	def directors(self):
		return self.__directors

	# Return writers function
	def writers(self):
		return self.__writers

	# Return cinematographers function
	def cinematographers(self):
		return self.__cinematographers

	# Return producers function
	def producers(self):
		return self.__producers

	# Return composers function
	def composers(self):
		return self.__composers

	# Return actors function
	def actors(self):
		return self.__actors

	# Return genre function
	def genres(self):
		return self.__genres

	# Return plot function
	def plot(self):
		return self.__plot

	# Return runtime function
	def runtime(self):
		return self.__runtime

	# Return coverURL function
	def getCoverURL(self):
		return self.__coverURL

	# Return XML string of object function
	def getXML(self):
		return self.__object.asXML()

	# Return object function
	def object(self):
		return self.__object

	# Class constructor
	def __init__(self, folderName):
		# create an instance of the IMDb class
		ia = IMDb()

		# Object will be instantiated with a folder name string with the format "MovieName (Year)"
		self.__name = folderName[:-7]
		self.__year = int(folderName[-5:-1])

		# Retrieve information from IMDB into object
		# Search for the movie and store the first 3 results (buffer for remakes, same name, etc. . .)
		query = ia.search_movie(folderName[:-7])[0:3]
		for result in query:
			# Check if the year matches the one in the folder (checking for duplicate named movies)
			if result['year'] == self.__year:
				# Store the IMDb movie object
				movie = ia.get_movie(result.movieID)
				break

		# Set fields based on IMDb query
		self.__object = movie
		self.__directors = movie['directors']
		self.__writers = movie['writers']
		self.__cinematographers = movie['cinematographers']
		self.__producers = movie['producers']
		self.__composers = movie['composers']
		self.__actors = movie['cast']
		self.__genres = movie['genres']
		self.__plot = movie['plot'][0]
		self.__runtime = movie['runtime'][0]
		self.__coverURL = movie['full-size cover url']
