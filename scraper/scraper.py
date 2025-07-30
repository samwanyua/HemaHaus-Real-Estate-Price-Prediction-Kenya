import requests
from bs4 import BeautifulSoup
import time
from database.init_db import get_connection

headers = {"User-Agent": "Mozilla/5.0"}

URLS = {
    "nairobi": "https://www.property24.co.ke/property-for-sale-in-nairobi-c1890",
    "thika": "https://www.property24.co.ke/property-for-sale-in-thika-c1850",
    "kisumu": "https://www.property24.co.ke/property-for-sale-in-kisumu-c1862",
    "eldoret": "https://www.property24.co.ke/property-for-sale-in-eldoret-c1919",
    "malindi": "https://www.property24.co.ke/property-for-sale-in-malindi-c1853",
    "kikuyu": "https://www.property24.co.ke/property-for-sale-in-kikuyu-c1847",
    "kajiado": "https://www.property24.co.ke/property-for-sale-in-kajiado-c1836",
    "kwale": "https://www.property24.co.ke/property-for-sale-in-kwale-c1867",
    "machakos": "http://property24.co.ke/property-for-sale-in-machakos-p66",
    "nyeri": "https://www.property24.co.ke/property-for-sale-in-nyeri-p101",
    "mombasa": "https://www.property24.co.ke/property-for-sale-in-mombasa-c1887",
    "nakuru": "https://www.property24.co.ke/property-for-sale-in-nakuru-c1896",
    "ngong": "https://www.property24.co.ke/property-for-sale-in-ngong-c1838",
    "nanyuki": "https://www.property24.co.ke/property-for-sale-in-nanyuki-c1868",
    "athi_river": "https://www.property24.co.ke/property-for-sale-in-athi-river-c1821",
    "naivasha": "https://www.property24.co.ke/property-for-sale-in-naivasha-c1895",
    "juja": "https://www.property24.co.ke/property-for-sale-in-juja-c1846",
    "lamu": "https://www.property24.co.ke/property-for-sale-in-lamu-c1869",
    "nyandarua": "https://www.property24.co.ke/property-for-sale-in-nyandarua-c2149",
    "isinya": "https://www.property24.co.ke/property-for-sale-in-isinya-c2153",
    "kitengela": "https://www.property24.co.ke/property-for-sale-in-kitengela-c1871",
    "ruiru": "https://www.property24.co.ke/property-for-sale-in-ruiru-c1849",
    "kilifi": "https://www.property24.co.ke/property-for-sale-in-kilifi-c1852",
    "kiambu": "https://www.property24.co.ke/property-for-sale-in-kiambu-c1851",
    "kiserian": "https://www.property24.co.ke/property-for-sale-in-kiserian-c1837",
    "limuru": "https://www.property24.co.ke/property-for-sale-in-limuru-c1848",
    "watamu": "https://www.property24.co.ke/property-for-sale-in-watamu-c1856",
    "narok": "https://www.property24.co.ke/property-for-sale-in-narok-c1899",
    "nyahururu": "https://www.property24.co.ke/property-for-sale-in-nyahururu-c1901",
    "ongata_rongai": "https://www.property24.co.ke/property-for-sale-in-ongata-rongai-s14581?CityId=1839&CityName=ongata-rongai"
}

def get_total_pages(base_url):
    try:
        resp = requests.get(base_url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        pagination = soup.select("ul.pagination li.pagelink a")
        pages = [int(a.text.strip()) for a in pagination if a.text.strip().isdigit()]
        return max(pages) if pages else 1
    except Exception as e:
        print(f"Error getting total pages for {base_url}: {e}")
        return 1


def scrape_page(base_url, page):
    url = base_url if page == 1 else f"{base_url}?Page={page}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"Failed to fetch page {page}: {e}")
        return []

    cards = soup.select(".p24_content")
    results = []
    for card in cards:
        try:
            price_tag = card.select_one(".p24_price")
            title_tag = card.select_one(".p24_propertyTitle")
            loc_tag = card.select_one(".p24_location")
            addr_tag = card.select_one(".p24_address")
            desc_tag = card.select_one(".p24_excerpt")

            features = card.select(".p24_featureDetails span")
            beds = features[0].text.strip() if len(features) > 0 else None
            baths = features[1].text.strip() if len(features) > 1 else None
            parking = features[2].text.strip() if len(features) > 2 else None

            size_span = card.select_one(".p24_size span")

            listing = {
                "title": title_tag.text.strip() if title_tag else None,
                "price": price_tag.text.strip() if price_tag else None,
                "location": loc_tag.text.strip() if loc_tag else None,
                "address": addr_tag.text.strip() if addr_tag else None,
                "description": desc_tag.text.strip() if desc_tag else None,
                "bedrooms": beds,
                "bathrooms": baths,
                "parking": parking,
                "size": size_span.text.strip() if size_span else None,
                "source": "property24",
                "page": page,
                "url": url
            }
            results.append(listing)

        except Exception as e:
            print(f"Error parsing card on page {page}: {e}")
    return results


def save_to_postgres(listings):
    conn = get_connection()
    cur = conn.cursor()
    for l in listings:
        cur.execute("""
            INSERT INTO raw_listings 
            (title, price, location, address, description, bedrooms, bathrooms, parking, size, source, page, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            l['title'], l['price'], l['location'], l['address'], l['description'],
            l['bedrooms'], l['bathrooms'], l['parking'], l['size'],
            l['source'], l['page'], l['url']
        ))
    conn.commit()
    cur.close()
    conn.close()


def scrape_all():
    for city, base_url in URLS.items():
        print(f"\n🌍 Scraping: {city}")
        total_pages = get_total_pages(base_url)
        print(f"🔢 Total pages in {city}: {total_pages}")
        for page in range(1, total_pages + 1):
            print(f"   → Page {page}")
            listings = scrape_page(base_url, page)
            save_to_postgres(listings)
            time.sleep(1)


if __name__ == "__main__":
    scrape_all()
