from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.http import  HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your models here.

class DateTime(models.Model):
    datetime=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return unicode(self.datetime)

class Item(models.Model):
    name=models.CharField(max_length=60)
    created=models.ForeignKey(DateTime)
    priority=models.IntegerField(default=0)
    difficulty=models.IntegerField(default=0)
    done=models.BooleanField(default=False)

    def mark_done(self):
        return "<a href='%s'>Done</a>" % reverse("todo.views.mark_done",args=[self.pk])
    mark_done.allow_tags=True

class ItemAdmin(admin.ModelAdmin):
    list_display=["name","priority","difficulty","created","mark_done","done"]
    search_fields=["name"]

class ItemInline(admin.TabularInline):
    model=Item

class DateAdmin(admin.ModelAdmin):
    list_display=["datetime"]
    inlines=[ItemInline]

    def response_add(self,request,obj,post_url_continue='../%s/'):
        opts=obj._meta
        pk_value=obj._get_pk_val()

        msg="Item(s) were added sucessfully."

        if request.POST.has_key("_continue"):
            self.message_user(request,msg+' '+_("You may edit it again below."))
            if request.POST.has_key("_popup"):
                post_url_continue+="?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window,"%s","%s");'
                                '</script>' % (pk_value,obj))
        elif request.POST.has_key("_addanother"):
            self.message_user(request,msg+' '+(_("You may add another %s below.")%force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request,msg)
            return HttpResponseRedirect(reverse("admin:to_do_item_changelist"))


admin.site.register(Item,ItemAdmin)
admin.site.register(DateTime,DateAdmin)