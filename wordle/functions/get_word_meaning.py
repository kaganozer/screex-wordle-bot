import requests

_http_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://sozluk.gov.tr/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.51 "
                  "Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def get_word_meaning(word: str):
    api_url = f"https://sozluk.gov.tr/gts?ara={word}"
    
    try:
        response = requests.get(url=api_url, headers=_http_headers)
        if response.status_code == 200:
            word_data = response.json()
            word_meaning = word_data[0]["anlamlarListe"][0]["anlam"]
            return word_meaning
        else:
            return None
    except Exception:
        return None
