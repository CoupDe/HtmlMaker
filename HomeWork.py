class Tag(object):
    def __init__(self, tag, is_single=False, klass=None, topLevel=False, *args, **kwargs):

        self.tag = tag
        self.text = ''
        self.attributes = {}
        self.topLevel = topLevel
        self.is_single = is_single
        self.children = []
        self.html = ''

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        if kwargs:
            for attr, value in kwargs.items():
                if attr == 'klass':
                    attr = attr.replace('k', 'c')
                if '_' in attr:
                    attr = attr.replace('_', '-')
                self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "\n</%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)

            else:
                return "\n<{tag} {attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )


class TopLevelTag(Tag, object):
    def __init__(self, tag, *args, **kwargs):
        super(TopLevelTag, self).__init__(tag, is_single=False, topLevel=True, *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def __str__(self):
        html = "<%s>" % self.tag
        for child in self.children:
            html += str(child)
        html += "</%s>\n" % self.tag
        return html

    def __iadd__(self, other):
        self.children.append(other)
        return self


class HTML:
    def __init__(self, output=None):
        self.output = output

        self.children = []

    def __enter__(self):

        return self

    def __exit__(self, type, value, traceback):
        if self.output is not None:
            self.file_obj = open(self.output, 'w')
            self.file_obj.write('<html>\n')
            for child in self.children:
                self.file_obj.write(str(child))
            self.file_obj.write('</html>')
        else:
            print(self)
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "</html>"
        return html


def fileName():
    p = input('Для создания файла введите его название, для вывода в консоль нажмите Enter\n')
    if p == '':
        p = None
    elif 'html' in p:
        pass
    else:
        p = p + '.html'
    return p


with HTML(output=fileName()) as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
    doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

    with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
        with Tag("p") as paragraph:
            paragraph.text = "another test"
            div += paragraph

        with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
            div += img
        body += div
    doc += body
