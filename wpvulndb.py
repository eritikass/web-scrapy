import crawlbase    # base crawl
import scrapy


class WPVulndbSpider(crawlbase.BaseSpider):
    baseurl = 'https://wpvulndb.com'
    start_urls = [baseurl + '/wordpresses?page=1']
    name = 'wpvulndb'

    parsed = {}


    def parse(self, response):
        self.parse_page(response)

        for url in response.css('.pagination a::attr("href")').re('.*page=.*'):
            print self.baseurl + url
            yield scrapy.Request(response.urljoin(self.baseurl + url), self.parse_page)


    def parse_page(self, response):
        for rrow in response.css('#content table tbody tr'):
            #print rrow

            version =  rrow.css('a::text').extract_first()
            exp =  rrow.css('a[href*=vulnerabilities]')

            #print version
            #print exp

            url = exp.css('::attr("href")').extract_first()

            #print url

            provider_id = url.strip('/').split('/')[-1]

            if not provider_id.isnumeric():
                print "error getting provider_id from url"
                print url
                exit(1)
            #print provider_id

            url = self.baseurl + url

            #print url

            if self.used(provider_id):
                print "used[" + provider_id + "]"
                continue

            title = exp.css('::text').extract_first()
            #print title
            tp = title.split(' - ')

            #print tp

            tp.pop(0)
            title = " ".join(tp).strip();

            print '******'
            print provider_id
            print url
            print title
            print version

            self.insert(provider_id=provider_id, link=url, module=title, exploit=title, version=version)


            # /vulnerabilities/8488

            #break