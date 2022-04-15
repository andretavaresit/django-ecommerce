from django.db.models import Q
from django.db import models
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse

#Custom queryset
class ServiceQuerySet(models.query.QuerySet):
    
    def active(self):
        return self.filter(active = True)

    def featured(self):
        return self.filter(featured = True, active = True)

    def search(self, query):
        lookups = (Q(title__contains = query) | 
                   Q(description__contains = query) | 
                   Q(price__contains = query) |
                   Q(tag__title__icontains = query))
        return self.filter(lookups).distinct()

class ServiceManager(models.Manager):
    
    def get_queryset(self):
        return ServiceQuerySet(self.model, using = self._db)
    
    def all(self):
        return self.get_queryset().active()

    def featured(self):
        #self.get_queryset().filter(featured = True)
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

# Create your models here.
class Service(models.Model): #product_category
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank = True, unique = True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=20, default=100.00)
    image       = models.FileField(upload_to = 'services/', null = True, blank = True)
    featured    = models.BooleanField(default = False)
    active      = models.BooleanField(default = True)
    timestamp   = models.DateTimeField(auto_now_add = True)


    objects = ServiceManager()

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug = self.slug)
        return reverse("services:detail", kwargs={"slug": self.slug})
    
    #python 3
    def __str__(self):
        return self.title
        
    #python 2
    def __unicode__(self):
        return self.title

def service_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(service_pre_save_receiver, sender = Service)