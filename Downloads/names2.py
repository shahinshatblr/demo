# -*- coding: utf-8 -*-
import scrapy

class NamesSpider(scrapy.Spider):
	name="names"
	allowed_domains=['clutch.co']
	start_urls=['https://clutch.co/directory/mobile-application-developers?sort_by=field_pp_reviews_count&field_pp_min_project_size=All&field_pp_hrly_rate_range=All&field_pp_size_people=All&field_pp_cs_small_biz=&field_pp_cs_midmarket=&field_pp_cs_enterprise=&client_focus=&field_pp_if_advertising=&field_pp_if_automotive=&field_pp_if_arts=&field_pp_if_bizservices=&field_pp_if_conproducts=&field_pp_if_education=&field_pp_if_natural_resources=&field_pp_if_finservices=&field_pp_if_gambling=&field_pp_if_gaming=&field_pp_if_government=&field_pp_if_healthcare=&field_pp_if_hospitality=&field_pp_if_it=&field_pp_if_legal=&field_pp_if_manufacturing=&field_pp_if_media=&field_pp_if_nonprofit=&field_pp_if_realestate=&field_pp_if_retail=&field_pp_if_telecom=&field_pp_if_transportation=&field_pp_if_utilities=&field_pp_if_other=&industry_focus=&field_pp_location_country_select=All&field_pp_location_province=&field_pp_location_latlon_1%5Bpostal_code%5D=&field_pp_location_latlon_1%5Bsearch_distance%5D=100&field_pp_location_latlon_	1%5Bsearch_units%5D=mile&page=0']
	def __init__(self):
		self.count=0
		self.count2=0
	def parse(self,response):
		for data in response.css('div.col-xs-12.col-md-10.bordered-right.provider-base-info>div.row.provider-row-header>div.col-xs-12'):
			#name1={
				#'name':data.css('h3.company-name>span.field-content>a::text').extract_first()
				#}
			#yield name1
			#self.company_name=data.css('h3.company-name>span.field-content>a::text').extract_first()
			review=data.css('div.rating-reviews').extract_first()
			if review is not 'na':
				details_url=data.css('span.field-content>a::attr(href)').extract_first()
				details_url=response.urljoin(details_url)
				yield scrapy.Request(url=details_url,callback=self.parse_details)
		next_page_url=response.css('li.pager-next>a::attr(href)').extract_first()
		if next_page_url:
			self.count=self.count+1
		if self.count<=70:
			next_page_url=response.urljoin(next_page_url)
			yield scrapy.Request(url=next_page_url,callback=self.parse)
				
	def parse_details(self,response):
		for details in response.css('div.review-border'):
			details={
				'name':response.css('div.page-heading-brand-info>h1.page-title::text').extract_first(),
				'project':details.css('div.col-30.project-col>h2>a::text').extract_first(),
				'amount':details.css('div.field.field-name-field-fdb-cost.field-type-taxonomy-term-reference.field-label-hidden.field-label-inline.clearfix>div.field-items>div.field-item.even::text').extract_first(),
				'summary':details.css('div.field.field-name-field-fdb-proj-description.field-type-text-long.field-label-inline.clearfix>div.field-items>div.field-item.even>p::text').extract_first(),
				'project_review':review.css('div.field.field-name-field-fdb-client-quote.field-type-text-long.field-label-hidden>div.field-items>div.field-item.even>p::text').extract_first()
				'reviewer_title':details.css('div.group-fdb-reviewer>div.__relative>div.field.field-name-field-fdb-title.field-type-text.field-label-hidden>div.field-items>div.field-item.even::text').extract_first(),
				
				'reviewer_name':details.css('div.group-fdb-reviewer>div.__relative>div.field.field-name-field-fdb-full-name-display.field-type-text.field-label-hidden>div.field-items>div.field-item.even::text').extract_first(),
				}
			details['summary']=(details['summary'].encode('ascii','ignore')).decode('unicode_escape')
			for key, value in details.iteritems():
				if details['reviewer_name'] is None:
        				details['reviewer_name']='null'
				if details['project_review'] is None:
        				details['project_review']='null'
				if details['reviewer_title'] is None:
        				details['reviewer_title']='null'
			details['reviewer_name']=(details['reviewer_name'].encode('ascii','ignore')).decode('unicode_escape')
			details['project_review']=(details['project_review'].encode('ascii','ignore')).decode('unicode_escape')
			details['name']=details['name'].replace('\n','')
			self.count2=self.count2+1
			self.logger.info('count = %s', self.count2)
			yield details
		next_url=response.css('div.text-center>ul.pagination>li.next>a::attr(href)').extract_first()
		next_url=response.urljoin(next_url)
		yield scrapy.Request(url=next_url,callback=self.parse_details)
		
