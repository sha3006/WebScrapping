import requests
from bs4 import BeautifulSoup
import os

class PinterestScraper:
    def load_images(self, filename):
            with open(filename, 'r', encoding='utf-8') as image_file:
                return image_file.read()


    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        return [image['src'] for image in content.find_all('img', src=True)]

    def download(self, url, output_folder):
        response = requests.get(url)
        filename = os.path.join(output_folder, url.split('/')[-1])

        print('Downloading image %s from URL %s' % (filename, url))

        if response.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in response.iter_content(chunk_size=128):
                    image.write(chunk)

    def run(self, input_file, output_folder):
        html = self.load_images(input_file)
        urls = self.parse(html)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for url in urls:
            self.download(url, output_folder)

if __name__ == '__main__':
    input_html_file = 'images.html'
    output_image_folder = 'downloaded_images'
    
    scraper = PinterestScraper()
    scraper.run(input_html_file, output_image_folder)
