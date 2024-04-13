from django.contrib import admin
from graduatethesis.models import *
from django.utils.html import mark_safe
from django.urls import path
# Register your models here.
class TieuChiInlineAdmin(admin.StackedInline):
    model = TieuChi.kltn.through


class ThesisAppAdminSite(admin.AdminSite):
    site_header = "Quản trị người dùng"

    def get_urls(self):
        return [
                path('user/',self.stats_view)
        ]+ super().get_urls()

    def stats_view(self):
        pass

admin_site = ThesisAppAdminSite(name='gt_ts')


class NguoiDungAdmin(admin.ModelAdmin):
    def avatar(self,nguoidung):
        if nguoidung:
            return mark_safe(
                '<img src= "/static/{url}" width="120"/>'.format(url=nguoidung.avatar.name)
            )

class KhoaLuanTotNghiepAdmin(admin.ModelAdmin):
    inlines = [TieuChiInlineAdmin,]


admin_site.register(NguoiDung,NguoiDungAdmin)
admin_site.register(SinhVien)
admin_site.register(GiaoVu)
admin_site.register(GiangVien)
admin_site.register(KhoaLuanTotNghiep,KhoaLuanTotNghiepAdmin)
admin_site.register(HoiDongBVKL)
admin_site.register(Lop)
admin_site.register(KLTNGVHuongDan)
admin_site.register(LopHocNghanhHoc)
admin_site.register(TieuChi)
admin_site.register(Diem)
admin_site.register(NghanhHoc)




