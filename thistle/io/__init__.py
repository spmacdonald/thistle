import re
import xml.etree.cElementTree as ElementTree


class WikipediaXmlReader(object):

    def __init__(self, fh, namespace):
        self.fh = fh
        self.namespace = namespace

    def __iter__(self):
        context = ElementTree.iterparse(self.fh, events=('start', 'end'))
        context = iter(context)
        event, root = context.next()

        for event, elem in context:
            if event == 'end' and elem.tag == '{0}page'.format(self.namespace):
                yield WikipediaPage(elem, self.namespace)
                root.clear()


class WikipediaPage(object):

    REDIRECT = r'#REDIRECT'
    CATEGORY = r'\[\[Category:(.*?)\]\]'
    LINKS = r'\[\[(.*?)\]\]'
    STUB = r'\-stub\}\}'
    DISAMB = r'\{\{disambig\}\}'
    SPECIAL_PREFIXES = set(('Wikipedia', 'MediaWiki', 'File', 'Portal', 'Template', 'Category', 'Help'))

    def __init__(self, page, namespace):
        self.page = page
        self.namespace = namespace

    @property
    def title(self):
        return self.page.findtext('{0}title'.format(self.namespace))

    @property
    def text(self):
        return self.page.findtext('{0}revision/{0}text'.format(self.namespace))

    @property
    def redirect(self):
        return re.search(self.REDIRECT, self.text, re.MULTILINE)

    @property
    def stub(self):
        return re.search(self.STUB, self.text, re.MULTILINE)

    @property
    def disamb(self):
        return re.search(self.DISAMB, self.text, re.MULTILINE)

    @property
    def special(self):
        fields = self.title.split(':')
        if len(fields) > 0 and fields[0] in self.SPECIAL_PREFIXES:
            return True
        return False

    @property
    def categories(self):
        categories = set()
        for c in re.finditer(self.CATEGORY, self.text, re.MULTILINE):
            categories.add(c.group(1).split('|')[0])
        return categories

    @property
    def links(self):
        links = set()
        for l in re.finditer(self.LINKS, self.text, re.MULTILINE):
            link = l.group(1)
            if ':' not in link:
                links.add(link.split('|')[0])
        return links
