from django.http import Http404

from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Service

class ServiceFeaturedListView(ListView):
    template_name = "services/list.html"
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Service.objects.featured()

class ServiceFeaturedDetailView(DetailView):
    queryset = Service.objects.all().featured()
    template_name = "services/featured-detail.html"

#Class Based View
class ServiceListView(ListView):
    #traz todos os produtos do banco de dados sem filtrar nada 
    queryset = Service.objects.all()
    template_name = "services/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

#Function Based View
def service_list_view(request):
    queryset = Service.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "services/list.html", context)

class ServiceDetailSlugView(DetailView):
    queryset = Service.objects.all()
    template_name = "services/detail.html"

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug = slug, active = True)
        try:
            instance = Service.objects.get(slug = slug, active = True)
        except Service.DoesNotExist:
            raise Http404("Não encontrado!")
        except Service.MultipleObjectsReturned:
            qs = Service.objects.filter(slug = slug, active = True)
            instance =  qs.first()
        return instance

#Class Based View
class ServiceDetailView(DetailView):
    template_name = "services/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Service.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Esse produto não existe!")
        return instance

#Function Based View
def service_detail_view(request, pk = None, *args, **kwargs):
    instance = Service.objects.get_by_id(pk)
    print(instance)
    if instance is None:
        raise Http404("Esse produto não existe!")

    context = {
        'object': instance
    }
    return render(request, "services/detail.html", context)