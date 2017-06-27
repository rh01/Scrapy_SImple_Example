本片教程参考 [scrapy官方教程](http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html) 修改过来的，测试网站已经停止运营，按照给出的思路，重新测试了 [dmoztools.net](dmoztools.net) 这个静态网站。
步骤相对详细，可以在任何操作系统环境下实现。

## Requirements

* Python2.7
* Anaconda3
* [Scrapy Tutorial](http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html)

## Steps 

* 创建一个Scrapy项目
* 定义提取的Item
* 编写爬取网站的 spider 并提取 Item
* 编写 Item Pipeline 来存储提取到的Item(即数据)

## 创建项目

```shell
scrapy startproject tutorial
```
You can see out message, like this:
```shell
New Scrapy project 'tutorial', using template directory 'C:\\Users\\Shine\\Anaconda3\\envs\\spider\\lib\\site-packages\\scrapy\\templates\\project', created in:
    C:\Users\Shine\Desktop\scrapy_tt\tutorial

You can start your first spider with:
    cd tutorial
    scrapy genspider example example.com

```

该命令将会创建包含下列内容的 `tutorial` 目录:
```shell
tutorial/
    scrapy.cfg
    tutorial/
        __init__.py
        items.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            ...
```
这些文件分别是:

* scrapy.cfg: 项目的配置文件
* tutorial/: 该项目的python模块。之后您将在此加入代码。
* tutorial/items.py: 项目中的item文件.
* tutorial/pipelines.py: 项目中的pipelines文件.
* tutorial/settings.py: 项目的设置文件.
* tutorial/spiders/: 放置spider代码的目录.

## 定义Item

Item 是保存爬取到的数据的容器；其使用方法和python字典类似， 并且提供了额外保护机制来避免拼写错误导致的未定义字段错误。

类似在ORM中做的一样，可以通过创建一个 `scrapy.Item` 类， 并且定义类型为` scrapy.Field` 的类属性来定义一个Item。

首先根据需要从`dmoz.org`获取到的数据对`item`进行建模。 需要从dmoz中获取`名字`，`url`，以及`网站的描述`。 对此，在item中定义相应的字段(`field`)。编辑 `tutorial` 目录中的 `items.py` 文件:
```python

import scrapy

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
```
一开始这看起来可能有点复杂，但是通过定义item， 您可以很方便的使用Scrapy的其他方法。而这些方法需要知道您的item的定义。

## 编写第一个爬虫(Spider)

Spider是用户编写用于从单个网站(或者一些网站)爬取数据的类。

其包含了一个用于下载的初始URL，如何跟进网页中的链接以及如何分析页面中的内容， 提取生成 `item` 的方法。

为了创建一个Spider，您必须继承 `scrapy.Spider` 类， 且定义以下三个属性:

* `name`: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
* `start_urls`: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
* `parse`() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 该方法负责 **解析返回的数据(response data)**，**提取数据(生成item)** 以及 **生成需要进一步处理的URL的 Request 对象**。
以下为我们的第一个Spider代码，保存在 tutorial/spiders 目录下的 dmoz_spider.py 文件中:

```python
import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/",
        "http://dmoztools.net/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
```

## 爬取
进入项目的根目录，执行下列命令启动spider:

```shell
scrapy crawl dmoz
```

`crawl dmoz` 启动用于爬取 `dmoz.org` 的spider，您将得到类似的输出:

```shell
2017-06-27 08:59:01 [scrapy.core.engine] INFO: Spider opened
2017-06-27 08:59:01 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2017-06-27 08:59:01 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
2017-06-27 08:59:01 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://dmoztools.net/robots.txt> (referer: None)
2017-06-27 08:59:01 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://dmoztools.net/Computers/Programming/Languages/Python/Books/> (referer: None)
2017-06-27 08:59:01 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://dmoztools.net/Computers/Programming/Languages/Python/Resources/> (referer: None)
2017-06-27 08:59:02 [scrapy.core.engine] INFO: Closing spider (finished)
2017-06-27 08:59:02 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 737,
 'downloader/request_count': 3,
 'downloader/request_method_count/GET': 3,
 'downloader/response_bytes': 14538,
 'downloader/response_count': 3,
 'downloader/response_status_count/200': 3,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2017, 6, 27, 0, 59, 2, 120000),
 'log_count/DEBUG': 4,
 'log_count/INFO': 7,
 'response_received_count': 3,
 'scheduler/dequeued': 2,
 'scheduler/dequeued/memory': 2,
 'scheduler/enqueued': 2,
 'scheduler/enqueued/memory': 2,
 'start_time': datetime.datetime(2017, 6, 27, 0, 59, 1, 513000)}
2017-06-27 08:59:02 [scrapy.core.engine] INFO: Spider closed (finished)c
```

查看包含 `[dmoz]` 的输出，可以看到输出的log中包含定义在 `start_urls `的初始URL，并且与spider中是一一对应的。在log中可以看到其没有指向其他页面( `(referer:None)` )。

除此之外，更有趣的事情发生了。就像 `parse` 方法指定的那样，有两个包含url所对应的内容的文件被创建了: *Book* , *Resources* 。

## 刚才发生了什么？

Scrapy为Spider的 `start_urls` 属性中的每个URL创建了 `scrapy.Request` 对象，并将 `parse` 方法作为`回调函数`(callback)赋值给了Request。

Request对象经过调度，执行生成 `scrapy.http.Response` 对象并送回给spider `parse()` 方法。


## 提取Item

### Selectors选择器简介

从网页中提取数据有很多方法。Scrapy使用了一种基于 `XPath` 和 `CSS` 表达式机制: `Scrapy Selectors`。 

这里给出 `XPath` 表达式的例子及对应的含义:

`/html/head/title`: 选择HTML文档中 `<head>` 标签内的 `<title>` 元素
`/html/head/title/text()`: 选择上面提到的 `<title>` 元素的文字
`//td`: 选择所有的 `<td>` 元素
`//div[@class="mine"]`: 选择所有具有 `class="mine"` 属性的 `div` 元素

上边仅仅是几个简单的XPath例子，XPath实际上要比这远远强大的多。 

为了配合XPath，Scrapy除了提供了 `Selector` 之外，还提供了方法来避免每次从response中提取数据时生成selector的麻烦。

Selector有四个基本的方法:

* `xpath()`: 传入xpath表达式，返回该表达式所对应的所有节点的selector list列表 。
* `css()`: 传入CSS表达式，返回该表达式所对应的所有节点的selector list列表.
* `extract()`: 序列化该节点为unicode字符串并返回list。
* `re()`: 根据传入的正则表达式对数据进行提取，返回unicode字符串list列表。

## 在Shell中尝试Selector选择器

为了介绍Selector的使用方法，接下来将要使用内置的 Scrapy shell。
首先需要进入项目的根目录，执行下列命令来启动shell:

```shell
>>> response.headers
{'Via': ['1.1 5570ab7675109645d02bb72112dedcea.cloudfront.net (CloudFront)'], 'X-Cache': ['RefreshHit from cloudfront'], 'Vary': ['Accept-Encoding'], 'Server': ['AmazonS3'], 'Last-Modified': ['Mon, 20 Mar 2017 16:50:55 GMT'], 'X-Amz-Cf-Id': ['EelvTvqXcYZQX3jFbj4LXdQSxh1bRxJbAmAx-LIZd_zY48M7J7XV0g=='], 'Date': ['Sun, 25 Jun 2017 14:04:43 GMT'], 'Content-Type': ['text/html']}
>>> response.selector.xpath('//title')
[<Selector xpath='//title' data=u'<title>DMOZ - Computers: Programming: La'>]
>>> response.selector.xpath('//title')
[<Selector xpath='//title' data=u'<title>DMOZ - Computers: Programming: La'>]
>>> response.selector.xpath('//title').extract
<bound method SelectorList.extract of [<Selector xpath='//title' data=u'<title>DMOZ - Computers: Programming: La'>]>
>>> response.selector.xpath('//title').extract()
[u'<title>DMOZ - Computers: Programming: Languages: Python: Books</title>']
>>> response.selector.xpath('//title/text()')
[<Selector xpath='//title/text()' data=u'DMOZ - Computers: Programming: Languages'>]
>>> response.selector.xpath('//title/text()').extract()
[u'DMOZ - Computers: Programming: Languages: Python: Books']
>>> response.selector.xpath('//title/text()').re('w+')
[]
>>> response.selector.xpath('//title/text()').re('\w+')
[u'DMOZ', u'Computers', u'Programming', u'Languages', u'Python', u'Books']
>>> ','.join(response.selector.xpath('//title/text()').re('\w+')[0])
u'D,M,O,Z'
>>> ','.join(response.selector.xpath('//title/text()').re('\w+'))
u'DMOZ,Computers,Programming,Languages,Python,Books'
>>> ' '.join(response.selector.xpath('//title/text()').re('\w+'))
u'DMOZ Computers Programming Languages Python Books'
>>>
```
## 提取数据

现在尝试从这些页面中提取些有用的数据。

在终端中输入 `response.body` 来观察HTML源码并确定合适的XPath表达式。不过，这任务非常无聊且不易。
可以考虑使用Chrome的检查工具。



网站的描述:

`response.xpath('//*[@id="site-list-content"]/div/div/div/text()').extract()`

网站的标题:

`response.xpath('//*[@id="site-list-content"]/div/div/a/div/text()').extract()
`
以及网站的链接:

`response.xpath('//*[@id="site-list-content"]/div/div/a/@href').extract()
`
之前提``到过，每个 `.xpath()` 调用返回selector组成的list，因此我们可以拼接更多的 `.xpath()` 来进一步获取某个节点。我们将在下边使用这样的特性:
为了方便查看，可以写入到 `html` 文件中去。

```python
with open('format.html','wb') as f:
    for i in response.xpath('//*[@id="site-list-content"]/div/div[3]').extract():
        f.write(i)
```


## 使用item

`Item` 对象是自定义的python字典。 使用标准的字典语法来获取到其每个字段的值。(字段即是之前用Field赋值的属性):
```python
>>> item = DmozItem()
>>> item['title'] = 'Example title'
>>> item['title']
'Example title'
```

一般来说，Spider将会将爬取到的数据以 Item 对象返回。所以为了将爬取的数据返回，最终的代码将是:
```python
import scrapy

from tutorial.items import TutorialItem

class DmozSpiderSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoztools.net"]
    start_urls = ['http://dmoztools.net/Computers/Programming/Languages/Python/Books/',
                  'http://dmoztools.net/Computers/Programming/Languages/Python/Resources/']

    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        for sel in response.xpath('//*[@id="site-list-content"]/div/div[3]'):
            item = TutorialItem()
            item['name'] = sel.xpath('a/div/text()').extract()[0]
            item['link'] = sel.xpath('a/@href').extract()[0]
            item['desc'] = sel.xpath('div/text()').extract()[0].strip()
            yield item      
```


现在对dmoztools.net 进行爬取将会产生 TutorialItem 对象:

```shell
{'desc': u'The primary goal of this book is to promote object-oriented design using Python and to illustrate the use of the emerging object-oriented design patterns.\r\nA secondary goal of the book is to present mathematical tools just in time. Analysis techniques and proofs are presented as needed and in the proper context.',
 'link': u'http://www.brpreiss.com/books/opus7/html/book.html',
 'name': u'Data Structures and Algorithms with Object-Oriented Design Patterns in Python '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Mark Pilgrim, Guide to Python 3  and its differences from Python 2. Each chapter starts with a real code sample and explains it fully. Has a comprehensive appendix of all the syntactic and semantic changes in Python 3',
 'link': u'http://www.diveintopython.net/',
 'name': u'Dive Into Python 3 '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'This book covers a wide range of topics. From raw TCP and UDP to encryption with TSL, and then to HTTP, SMTP, POP, IMAP, and ssh. It gives you a good understanding of each field and how to do everything on the network with Python.',
 'link': u'http://rhodesmill.org/brandon/2011/foundations-of-python-network-programming/',
 'name': u'Foundations of Python Network Programming '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'Free Python books and tutorials.',
 'link': u'http://www.techbooksforfree.com/perlpython.shtml',
 'name': u'Free Python books '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'Annotated list of free online books on Python scripting language. Topics range from beginner to advanced.',
 'link': u'http://www.freetechbooks.com/python-f6.html',
 'name': u'FreeTechBooks: Python Scripting Language '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Allen B. Downey, Jeffrey Elkner, Chris Meyers; Green Tea Press, 2002, ISBN 0971677506. Teaches general principles of programming, via Python as subject language. Thorough, in-depth approach to many basic and intermediate programming topics. Full text online and downloads: HTML, PDF, PS, LaTeX. [Free, Green Tea Press]',
 'link': u'http://greenteapress.com/thinkpython/',
 'name': u'How to Think Like a Computer Scientist: Learning with Python '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Guido van Rossum, Fred L. Drake, Jr.; Network Theory Ltd., 2003, ISBN 0954161769. Printed edition of official tutorial, for v2.x, from Python.org. [Network Theory, online]',
 'link': u'http://www.network-theory.co.uk/python/intro/',
 'name': u'An Introduction to Python '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Rashi Gupta; John Wiley and Sons, 2002, ISBN 0471219754. Covers language basics, use for CGI scripting, GUI development, network programming; shows why it is one of more sophisticated of popular scripting languages. [Wiley]',
 'link': u'http://www.wiley.com/WileyCDA/WileyTitle/productCd-0471219754.html',
 'name': u'Making Use of Python '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Magnus Lie Hetland; Apress LP, 2002, ISBN 1590590066. Readable guide to ideas most vital to new users, from basics common to high level languages, to more specific aspects, to a series of 10 ever more complex programs. [Apress]',
 'link': u'http://hetland.org/writing/practical-python/',
 'name': u'Practical Python '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Rytis Sileika, ISBN13: 978-1-4302-2605-5, Uses real-world system administration examples like manage devices with SNMP and SOAP, build a distributed monitoring system, manage web applications and parse complex log files, monitor and manage MySQL databases.',
 'link': u'http://sysadminpy.com/',
 'name': u'Pro Python System Administration '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'A Complete Introduction to the Python 3.',
 'link': u'http://www.qtrac.eu/py3book.html',
 'name': u'Programming in Python 3 (Second Edition) '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Dave Brueck, Stephen Tanner; John Wiley and Sons, 2001, ISBN 0764548077. Full coverage, clear explanations, hands-on examples, full language reference; shows step by step how to use components, assemble them, form full-featured programs. [John Wiley and Sons]',
 'link': u'http://www.wiley.com/WileyCDA/WileyTitle/productCd-0764548077.html',
 'name': u'Python 2.1 Bible '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'A step-by-step tutorial for OOP in Python 3, including discussion and examples of abstraction, encapsulation, information hiding, and raise, handle, define, and manipulate exceptions.',
 'link': u'https://www.packtpub.com/python-3-object-oriented-programming/book',
 'name': u'Python 3 Object Oriented Programming '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Guido van Rossum, Fred L. Drake, Jr.; Network Theory Ltd., 2003, ISBN 0954161785. Printed edition of official language reference, for v2.x, from Python.org, describes syntax, built-in datatypes. [Network Theory, online]',
 'link': u'http://www.network-theory.co.uk/python/language/',
 'name': u'Python Language Reference Manual '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u"By Richard Hightower; Addison-Wesley, 2002, 0201616165. Begins with Python basics, many exercises, interactive sessions. Shows programming novices concepts and practical methods. Shows programming experts Python's abilities and ways to interface with Java APIs. [publisher website]",
 'link': u'http://www.informit.com/store/product.aspx?isbn=0201616165&redir=1',
 'name': u'Python Programming with the Java Class Libraries: A Tutorial for Building Web and Enterprise Applications with Jython '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Ivan Van Laningham; Sams Publishing, 2000, ISBN 0672317354. Split into 24 hands-on, 1 hour lessons; steps needed to learn topic: syntax, language features, OO design and programming, GUIs (Tkinter), system administration, CGI. [Sams Publishing]',
 'link': u'http://www.informit.com/store/product.aspx?isbn=0672317354',
 'name': u'Sams Teach Yourself Python in 24 Hours '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By David Mertz; Addison Wesley. Book in progress, full text, ASCII format. Asks for feedback. [author website, Gnosis Software, Inc.]',
 'link': u'http://gnosis.cx/TPiP/',
 'name': u'Text Processing in Python '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Books/>
{'desc': u'By Sean McGrath; Prentice Hall PTR, 2000, ISBN 0130211192, has CD-ROM. Methods to build XML applications fast, Python tutorial, DOM and SAX, new Pyxie open source XML processing library. [Prentice Hall PTR]',
 'link': u'http://www.informit.com/store/product.aspx?isbn=0130211192',
 'name': u'XML Processing with Python '}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Resources/>
{'desc': u'Contains links to assorted resources from the Python universe, compiled by PythonWare.',
 'link': u'http://www.pythonware.com/daily/',
 'name': u"eff-bot's Daily Python URL "}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Resources/>
{'desc': u'Features Python books, resources, news and articles.',
 'link': u'http://oreilly.com/python/',
 'name': u"O'Reilly Python Center "}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Resources/>
{'desc': u'Resources for reporting bugs, accessing the Python source tree with CVS and taking part in the development of Python.',
 'link': u'https://www.python.org/dev/',
 'name': u"Python Developer's Guide "}
2017-06-27 10:54:33 [scrapy.core.scraper] DEBUG: Scraped from <200 http://dmoztools.net/Computers/Programming/Languages/Python/Resources/>
{'desc': u'Scripts, examples and news about Python programming for the Windows platform.',
 'link': u'http://win32com.goermezer.de/',
 'name': u'Social Bug '}
```

## 保存爬取到的数据

最简单存储爬取的数据的方式是使用 `Feed exports`:
```shell
scrapy crawl dmoz -o items.json
```

该命令将采用 JSON 格式对爬取的数据进行序列化，生成 `items.json` 文件。

文件类似于这样：
![](https://ooo.0o0.ooo/2017/06/27/5951cc4634392.png)

## License

 ![](https://img.shields.io/packagist/l/doctrine/orm.svg)


## credit

Credit by [Scrapy](https://github.com/marchtea/scrapy_doc_chs/blob/0.24/intro/tutorial.rst), Modified by [Shine](https://github.com/rh01)