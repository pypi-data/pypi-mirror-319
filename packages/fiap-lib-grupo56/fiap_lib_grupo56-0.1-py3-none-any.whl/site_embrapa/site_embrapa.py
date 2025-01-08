import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class SiteEmbrapa:
    """
    Possui os métodos necessários para se fazer o webscrapping dos dados do site.
    Também gerencia um tipo de cache dos dados para quando o site estiver fora do ar.
    
    """
    def __init__(self):
        self.UrlBase = "http://vitibrasil.cnpuv.embrapa.br/index.php"

    def obterProducaoGeralPorAno(self, ano: int) -> list:
        """
        Recupera do site da embrapa, toda a produção de um ano.  Se o site estiver offline, retornará a produção de cache obtido previamente.

        """

        webscrapping = WebscrappingSiteEmbrapa(self.UrlBase)
        retorno = webscrapping.obterProducaoGeralPorAno(ano)
        return retorno


class WebscrappingSiteEmbrapa:
    """
    Realiza o webscrapping na página especifica do site, de acordo com o método utilizado. (Producao, Processamento etc...)

    """
    def __init__(self, urlBase: str):
        self.UrlBase = urlBase

    def obterProducaoGeralPorAno(self, ano: int) -> list:
        """
        Realiza o Webscrapping no site da embrapa

        """
        url = f"{self.UrlBase}?opcao=opt_02&Ano={ano}" 
        xpath = "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]/tbody/tr"

        retorno = self.obterElementosTR(url, xpath)

        return retorno;


    def obterElementosTR(self, url: str, xpath_tbody: str) -> list:
        """
        Abre a página da url e obtem lista de WebElement

        """
        # Defina as opções do navegador
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        # O webdriver_manager cuida de baixar a versão correta do ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Abre a página no navegador
        driver.get(url)

        # Encontra todos os elementos <a> que têm links
        # link_elements = driver.find_elements('tag name', 'a')

        tags_tr_do_tbody = driver.find_elements(By.XPATH, xpath_tbody)

        return tags_tr_do_tbody
