import scrapy
from csv import writer
from ..items import parseItem

class QuotesSpider(scrapy.Spider):
    name = "goodreads"

    start_urls = [
            'https://goodreads.com/list/popular_lists',
           
         ]
    def parse(self, response):
        quotes = response.xpath('//div[@class="cell"]')
        
        with open('detail.csv','a',encoding='utf8',newline='' ) as f:
         
            thewriter = writer(f)
            header = ['Title', 'List', 'Listfulldetails']
            thewriter.writerow(header)
            
            for quote in quotes:
                
                title = quote.xpath('.//a[@class="listTitle"]/text()').get().strip()
                cat_url = "https://goodreads.com" + quote.xpath('.//a[@class="listTitle"]/@href').get().strip()
                cat_details = quote.xpath('.//div[@class="listFullDetails"]/text()').get().replace("—","").strip()
                info = [title,cat_url,cat_details]
                thewriter.writerow(info)
           
    
            # next_pages =  "https://goodreads.com" + response.xpath ('.//a[@class="next_page"]/@href').get()
            # if next_pages:
            #     next_pages=next_pages
     
                yield scrapy.Request(url=cat_url, callback=self.parseitem,dont_filter=True)         

        
    def parseitem(self, response):
       
        # cat_url = "https://goodreads.com" + response.xpath('.//a[@class="listTitle"]/@href')
        booklist = response.xpath ('//tr[@itemscope]')
        

        with open('bookdetail.csv','a',encoding='utf8',newline='') as f:
         
            thewriter = writer(f)
            header = ['BookTitle', 'BookRating','AuthorName']
            thewriter.writerow(header)
            for book in booklist:
                    item = parseItem()
                    item ['book_title'] = book.xpath('.//a[@class="bookTitle"]/span/text()').get()
                    item ['book_rating'] = book.xpath('.//span[@class="minirating"]/text()').get()
                    item ['author_name'] = book.xpath('.//a[@class="authorName"]/span/text()').get()
                    yield item
                    bookinfo = [item]
                    thewriter.writerow(bookinfo)
         
                    next_pages = "https://goodreads.com" + response.xpath ('.//a[@class="next_page"]/@href').get()
                    if next_pages:
                        next_pages=next_pages
                    yield scrapy.Request(url=next_pages, callback=self.parseitem)

             