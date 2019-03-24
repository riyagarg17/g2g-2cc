
import json
from bs4 import BeautifulSoup as bsp
import requests
from flask import Flask
import myconstants
import blueprint

app = Flask(__name__)


@app.route('/organization_details')
def organization_details():
    response = requests.get(myconstants.orgs_url)
    html = response.content
    soup = bsp(html, "html.parser")
    get_organizations = soup.findAll("li", {'class': 'organization-card__container'})
    final_result = fetch_details(get_organizations)
    print(final_result)
    return json.dumps(final_result)


def fetch_details(get_organizations):
    extracted_result = list()
    count = 0
    for item in get_organizations:
        purl = item.find('a', {'class': 'organization-card__link'})
        org_name = item['aria-label']

        info = item.find('div', {'class': 'organization-card__tagline font-black-54'})
        info = info.text
        p_link = myconstants.base_url_gsoc + purl['href']
        page = requests.get(p_link)
        if page.status_code != 200:
            break
        p_link = myconstants.base_url_gsoc + purl['href']
        response1 = requests.get(p_link)
        html1 = response1.content
        soup1 = bsp(html1, "html.parser")
        org_link = soup1.find("a", {"class": "org__link"})
        org_link = org_link.text
        techies = soup1.findAll("li", {"class": "organization__tag organization__tag--technology"})
        tech = []
        for titem in techies:
            tech.append(titem.text)
        mtopics = soup1.findAll("li", {"class": "organization__tag organization__tag--topic"})
        topics = []
        for j in mtopics:
            topics.append(j.text)
        count += 1
        print(count)
        extracted_result.append({
            'organization_name': org_name,
            'description': info,
            'link': org_link,
            'technologies': tech,
            'topics': topics
        })
	#Extracting Only 10 organization details Change below count value to get details of more.
        if count == 10:
            return extracted_result


if __name__ == "__main__":
    app.run(debug=True)
