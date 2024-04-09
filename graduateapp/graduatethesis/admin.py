from django.contrib import admin
from graduatethesis.models import (NguoiDung,SinhVien,GiaoVu,GiangVien,HoiDongBVKL,KhoaLuanTotNghiep,NghanhHoc
,KLTNGVHuongDan,Lop,LopHocNghanhHoc,TieuChi,Diem,VaiTro)
from django.utils.html import mark_safe

# from graduatethesis.models import

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.
admin.site.register(NguoiDung)
admin.site.register(SinhVien)
admin.site.register(GiaoVu)
admin.site.register(GiangVien)
admin.site.register(KhoaLuanTotNghiep)
admin.site.register(HoiDongBVKL)
admin.site.register(Lop)
admin.site.register(KLTNGVHuongDan)
admin.site.register(LopHocNghanhHoc)
admin.site.register(TieuChi)
admin.site.register(Diem)
admin.site.register(VaiTro)



