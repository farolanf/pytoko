import re
from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from toko.models import Taxonomy

class Command(BaseCommand):
    help = 'Populate taxonomy form input file.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            'inputfile',
            help='Text file containing indented items.'
        )

    def handle(self, *args, **options):
        with open(options['inputfile']) as file:
            data = file.read()
        lines = data.split('\n')
        tree = self.build_tree(lines)
        Taxonomy.objects.all().delete()
        self.create_object(tree)

    def create_object(self, item, parent=None):
        obj = None
        if item['indent'] >= 0:
            obj = Taxonomy.objects.create(name=item['title'], slug=item['slug'], parent=parent)
        if len(item['children']):
            for it in item['children']:
                self.create_object(it, obj)

    def build_tree(self, lines):
        """
        Build tree of objects from a list of lines.
        """
        root = {
            'slug': '',
            'indent': -1,
            'children': [],
        }
        ancestors = [root]
        prev_indent = -1

        for line in lines:
            parts = line.split(';')

            indent = len(parts[0]) - len(parts[0].lstrip())

            title = parts[0].strip()

            if title == '': continue

            _slug = parts[1].strip() if len(parts) > 1 else ''

            slug = re.sub(r'[^a-zA-Z0-9]', '-', title)
            slug = re.sub(r'-+', '-', slug)
            slug = slug.lower()

            # remove non ancestor
            for i in range(len(ancestors)-1, -1, -1):
                if ancestors[i]['indent'] >= indent:
                    ancestors.pop()

            parent = ancestors[-1]

            if _slug == '/':
                # prepend with parent slug
                slug = '%s-%s' % (parent['slug'], slug)

            item = {
                'indent': indent,
                'title': title,
                'slug': slug,
                'children': [],
            }

            parent['children'].append(item)

            if prev_indent < indent:
                ancestors.append(item)

        return root
