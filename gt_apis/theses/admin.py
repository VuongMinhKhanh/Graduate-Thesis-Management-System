from django.contrib import admin
from django.utils.html import mark_safe
from theses.models import *
from django.forms.models import BaseInlineFormSet

# Register models that do not require special admin customizations directly
admin.site.register(Lop)
admin.site.register(NganhHoc)
admin.site.register(NguoiDung, name="Người Dùng")
admin.site.register(SinhVien, name="Sinh Viên")
admin.site.register(GiangVien, name="Giảng Viên")
admin.site.register(GiaoVu, name="Giáo Vụ")
admin.site.register(KLTNGVHuongDan)
admin.site.register(HoiDongBVKL)
# admin.site.register(Diem)  # Consider if special customization is needed


class DiemInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.queryset = Diem.objects.filter(kltn=self.instance)
            allowed_tieu_chi = self.instance.tieu_chi.all()
            for form in self.forms:
                if 'tieu_chi' in form.fields:
                    form.fields['tieu_chi'].queryset = allowed_tieu_chi
        else:
            self.queryset = Diem.objects.none()


class DiemInline(admin.TabularInline):
    model = Diem
    formset = DiemInlineFormset
    extra = 1


class KhoaLuanTotNghiepAdmin(admin.ModelAdmin):
    # list_display = ['ten_khoa_luan', 'mssv', 'diem_tong']
    search_fields = ['ten_khoa_luan', 'mssv__ten']
    list_filter = ['mssv', 'diem_tong']
    inlines = [DiemInline]
    # filter_horizontal = ('tieu_chis',)


class TieuChiAdmin(admin.ModelAdmin):
    list_display = ['tieu_chi', 'ty_le']
    filter_horizontal = ['kltn']


# Ensure KhoaLuanTotNghiep is registered only once with the correct admin configuration
admin.site.register(KhoaLuanTotNghiep, KhoaLuanTotNghiepAdmin)
admin.site.register(TieuChi, TieuChiAdmin)