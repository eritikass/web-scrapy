import crawlbase    # base crawl
import scrapy


class ExploitDbSpider(crawlbase.BaseSpider):
    baseurl = 'http://0day.today'
    start_urls = [baseurl + '/webapps/1']
    name = '0day'

    agreeFormData = {
        "agree": "Yes, I agree"
    }

    def parse(self, response):
        yield scrapy.FormRequest.from_response(response, callback = self.parse_agreed, method = "POST", formdata = self.agreeFormData)

    def parse_agreed(self, response):
        if "Do you agree to these terms?" in response.body:
            print "terms agree error!!!"
            print response.url
            return

        self.parse_page(response)


        for page in response.css('.pages a'):  #:attr("href")').re('.*/platform/.*'):
            txt = page.css('::text').extract_first()
            if "next" in txt:
                url = page.css('::attr("href")').extract_first()
                print self.baseurl + url
                yield scrapy.Request(response.urljoin(self.baseurl + url), self.parse_agreed)
                break

    def parse_page(self, response):
        for post in response.css('.ExploitTableContent div.td.allow_tip h3 a'):
            title = post.css('::text').extract_first()
            url = post.css('::attr("href")').extract_first()

            if self.is_wp(title):
                print "found exp."
                print title
                print url

                provider_id = self.get_provider_id(url)
                print provider_id

                if self.used(provider_id):
                    #print "used"
                    continue

                url2 = self.baseurl + url
                title2 = self.cleanup_str(title)
                self.insert(provider_id=provider_id, link=url2, module=title2, exploit=title2, version="")