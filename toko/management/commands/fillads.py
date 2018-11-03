import os
import csv
import math
import random
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db.models import F
from toko.models import Ad, Taxonomy, Provinsi, Kabupaten, AdImage, Product, ProductType, File as FileModel

class Command(BaseCommand):
    help = 'Fill ads table'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            'inputfile',
            help='CSV file'
        )

    def handle(self, inputfile, *args, **options):
        self.user = get_user_model().objects.filter(is_superuser=True).first()
        with open(inputfile) as f:
            rows = csv.reader(f)
            self.process(rows)
    
    def process(self, rows):
        header = True
        for columns in rows:
            if header:
                header = False
                continue
            self.createAd(columns)
    
    def createAd(self, columns):
        category_root = Taxonomy.objects.get(slug='kategori')
        
        category = random.choice(Taxonomy.objects.filter(
                tree_id=category_root.tree_id, 
                rght=F('lft') + 1
            ).all()
        )

        provinsi = random.choice(Provinsi.objects.all())
        kabupaten = random.choice(provinsi.kabupaten_set.all())

        price = math.floor(float(columns[4]) * 15000)

        ad = Ad.objects.create(user=self.user, title=columns[1][:70], 
            desc=columns[2][:4000], price=price, nego=random.random() > 0.5, category=category, provinsi=provinsi, kabupaten=kabupaten)

        names = ['apple.jpg', 'brocoli.jpg', 'burger.jpg', 'nasi goreng udang.jpg']

        random.shuffle(names)

        for i, name in enumerate(names):
            path = os.path.join('toko/data', name)
            file = File(open(path, 'rb'))
            file_obj = FileModel.objects.create(user=ad.user, file=file)
            AdImage.objects.create(ad=ad, file=file_obj, order=i)

        product_type = category.product_types.order_by('?').first()
        product = Product.objects.create(ad=ad, product_type=product_type)
        for field in product_type.specs.all():
            value = field.choices.order_by('?').first()
            product.specs.create(field=field, value=value)
