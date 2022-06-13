from requests_html import HTMLSession
import csv

s = HTMLSession()
base_url = 'https://id.indeed.com'


def get_links(keyword):
      keyword = '+'.join(keyword.split(' '))
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
      url_to_scrape = base_url + "/jobs?q=" + keyword
      links = []
      for i in range(0, 5):
            extention = ""
            if i != 0:
                  extention = "&start=" + str(i * 10)
            url = url_to_scrape + extention
            r = s.get(url, headers = headers)
            joblisting = r.html.find('div.job_seen_beacon')
            for job in joblisting:
                  href = job.find('a.jcs-JobTitle', first = True).attrs['href']
                  complete_link = base_url + href
                  links.append(complete_link)
      return links


def parse_job(url):
      r = s.get(url)
      title = r.html.find('div.jobsearch-JobInfoHeader-title-container', first = True).text.strip()
      try:
        salary = r.html.find('span.icl-u-xs-mr--xs.attribute_snippet', first = True).text.strip()
      except:
        salary = 'None'
      desc = r.html.find('div.jobsearch-jobDescriptionText', first = True).text.strip('').replace('\n', ' ')
      company = r.html.find('a[target=_blank]', first = True).text.strip('')
      urls = url
      jobs = {
        'position': title,
        'company': company,
        'salary': salary,
        'description': desc,
        'link' : urls,
        }
      return jobs


def save_csv(results):
      keys = results[0].keys()
      with open('indeed_data.csv', 'a', newline='', encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)


results = []
def main():
      keywords = input('Enter job position keyword: ')
      links = get_links(keywords)
      for link in links:
            results.append(parse_job(link))
      save_csv(results)


if __name__ == '__main__':
      main()
      print('-----------Extraction of data is complete. Check the csv file.-----------')