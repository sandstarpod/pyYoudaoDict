#! /usr/bin/python
# -*- encoding:utf-8 -*-
import re;
import urllib;
import urllib2;
import sys;

#BEGIN

#This part is from the Internet.
#Thanks the author.
#http://www.cnblogs.com/nwf5d/archive/2011/11/20/2255674.html

#Modified by Moody "Kuuy" Wizmann



def debug():
	xml = open("word.xml").read();
	print get_text(xml);
	print get_elements_by_path(xml, "custom-translation/content");
	#print_translations(xml, False, False);
def get_elements_by_path(xml, elem):
	if type(xml) == type(''):
		xml = [xml];
	if type(elem) == type(''):
		elem = elem.split('/');
	if (len(xml) == 0):
		return [];
	elif (len(elem) == 0):
		return xml;
	elif (len(elem) == 1):
		result = [];
		for item in xml:
			result += get_elements(item, elem[0]);
		return result;
	else:
		subitems = [];
		for item in xml:
			subitems += get_elements(item, elem[0]);
		return get_elements_by_path(subitems, elem[1:]);
textre = re.compile("\!\[CDATA\[(.*?)\]\]", re.DOTALL);
def get_text(xml):
	match = re.search(textre, xml);
	if not match:
		return xml;
	return match.group(1);
def get_elements(xml, elem):
	p = re.compile("<" + elem + ">" + "(.*?)</" + elem + ">", re.DOTALL);
	it = p.finditer(xml);
	result = [];
	for m in it:
		result.append(m.group(1));
	return result;

def crawl_xml(queryword):
	return urllib2.urlopen("http://dict.yodao.com/search?keyfrom=dict.python&q="
        + urllib.quote_plus(queryword) + "&xmlDetail=true&doctype=xml").read();
def print_translations(xml, with_color, detailed):
        #print xml;
	original_query = get_elements(xml, "original-query");
	queryword = get_text(original_query[0]);
	custom_translations = get_elements(xml, "custom-translation");
	print queryword
	translated = False;
	
	try:
		cus=custom_translations[0]
		source = get_elements_by_path(cus, "source/name");
		
		#print  "Translations from " + source[0] 
		contents = get_elements_by_path(cus, "translation/content");
		for content in contents[0:5]:
			print get_text(content);
		translated = True;
	except:
		print "没有此单词或网络错误"
#END



def dict_it(word):
	argv=[]
	argv.append(word)
	xml = crawl_xml(" ".join(argv));
	print_translations(xml, True, False);

def main():
	file=open('input.txt')
	for line in file:
		dict_it(line)
		print('---------------------------------')

if __name__ == "__main__":
	sys.stdout=open('outfile.txt','w')
	main();

