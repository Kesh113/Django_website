from django.contrib.sitemaps import Sitemap

from test_app.models import Test_app, Category


class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Test_app.published.all()

    def lastmod(self, obj):
        return obj.time_update

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Category.objects.all()