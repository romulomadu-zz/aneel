from urllib.request  import urlopen, urlretrieve
from bs4 import BeautifulSoup
import re
import pandas as pd
import unidecode
from tqdm import tqdm

def fit_text(text):
    """Function to fit original columns name to column name that will be stored in db.

    Args:
        text: column name which will be changed to fit as db column.
        
    Returns:
        The return value is a string with columns name fitted..

    """
    # remove parenthesis terms
    text = re.sub('\(\S*\)|\s\(\S*\)','',text)
    # decoding and filling blank spaces with underscore    
    text = unidecode.unidecode(text)
    text = re.sub(' ','_',text)

    return re.sub(r'[^a-zA-Z0-9_]','',text.lower())

def main():

	url = 'http://www.aneel.gov.br/dados/relatorios?p_p_id=dadosabertos_WAR_dadosabertosportlet&amp;p_p_lifecycle=2&amp;p_p_state=normal&amp;p_p_mode=view&amp;p_p_resource_id=gerarTipoEmpreendimentoOperacaoCSV&amp;p_p_cacheability=cacheLevelPage&amp;p_p_col_id=column-2&amp;p_p_col_count=1'
	path = './data/'

	with urlopen(url) as html:
		page  = html.read().decode()
		soup = BeautifulSoup(page, 'html.parser')

	links = list()

	for a in tqdm(soup.find_all('a', href=True, alt=True), desc='Reading CSV links...', unit='links'):
		if a['alt'] == 'CSV':
			links.append(a['href'])

	titles = re.findall('\d+\.\d+\s+([\w|\s]+)\s+\-\s<a',page)
	titles = [fit_text(title) for title in titles]

	for link, title in tqdm(zip(links,titles), desc='Downloading CSV files...', unit='files'):
		file_path = path+title+'.csv'
		urlretrieve(link, file_path)

if __name__ == "__main__":
	main()


