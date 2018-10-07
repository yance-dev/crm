from django.conf import settings
from stark.service.stark import StarkConfig

class RbacPermission(object):

    def get_add_btn(self):
        name = "%s:%s" %(self.site.namespace,self.get_add_url_name,)
        permission_dict = self.request.session.get(settings.PERMISSION_SESSION_KEY)
        if name in permission_dict:
            return super().get_add_btn()

    def get_list_display(self):
        val = super().get_list_display()
        permission_dict = self.request.session.get(settings.PERMISSION_SESSION_KEY)
        edit_name = "%s:%s" %(self.site.namespace,self.get_change_url_name,)
        del_name = "%s:%s" %(self.site.namespace,self.get_del_url_name,)
        if edit_name not in permission_dict:
            val.remove(StarkConfig.display_edit)

        if del_name not in permission_dict:
            val.remove(StarkConfig.display_del)

        return val
