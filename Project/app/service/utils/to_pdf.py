from PIL import Image
import pathlib
from datetime import datetime

today = datetime.today().strftime( "%d_%m" )


class PdfBuilder:
	"""
	This class is used to create a single pdf file from all the screenshots, that is being send
	afterwards by email. It has the functionality of defining the pdf quality (file size reduction).
	"""

	# Getting all the filepaths of the screenshots to be collected in the pdf file
	# Used internally by the class method convert_to_pdf
	@classmethod
	def _get_files( cls, folder ):
		final_dir = folder
		all_images = list( final_dir.glob( "*.png" ) )

		return all_images

	@classmethod
	def convert_to_pdf( cls, folder, quality=90 ):
		images = cls._get_files( folder=folder )
		image_files = [Image.open( image ) for image in images]
		final_images = [file.convert( 'RGB' ) for file in image_files]
		if len( final_images ) > 1:
			destination = f"{folder}/Ads_Preview_{today}.pdf"
			final_images[0].save( destination,
			                      save_all=True,
			                      append_images=final_images[1:],
			                      quality=quality )
		else:
			destination = f"{folder}/Ads_Preview_{today}.pdf"
			final_images[0].save( destination )
		return destination



if __name__ == "__main__":
	# Used for testing in Development
	res = PdfBuilder.convert_to_pdf( folder="Toshko", quality=80 )
	print( res )