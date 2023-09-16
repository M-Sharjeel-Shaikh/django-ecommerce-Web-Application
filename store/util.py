import string
import random
from django.utils.text import slugify
from django.core.paginator import Paginator


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    slug = new_slug if new_slug is not None else slugify(instance.title)
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug[:max_length-5], randstr=random_string_generator(size=4))

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def shop_pagination(request, query):
    paginator = Paginator(query, 1)
    page_number = request.GET.get('page')
    # ======= which connect page connect and pagination =======
    page_data = paginator.get_page(page_number)
    total = page_data.paginator.num_pages

    return {
        'total_product': page_data,
        'totalpage': [n + 1 for n in range(total)],
    }
