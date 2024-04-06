from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
# Create your models here.


class ChucVu(Enum):
    CHU_TICH = 1
    THU_KY = 2
    THANH_VIEN = 3


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_created=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    pass


class GiaoVu(BaseModel):
    trinh_do = models.CharField(max_length=100)
    nguoi_dung = models.OneToOneField(User, on_delete=models.CASCADE)


class GiangVien(BaseModel):
    bang_cap = models.CharField(max_length=100)
    kinh_nghiem = models.CharField(max_length=255)
    nguoi_dung = models.OneToOneField(User, on_delete=models.CASCADE)


class SinhVien(BaseModel):
    mssv = models.CharField(max_length=20, unique=True)
    nam_nhap_hoc = models.IntegerField()
    lop = models.ForeignKey('Lop', on_delete=models.PROTECT, null=False)


class Lop(BaseModel):
    ten_lop = models.CharField(max_length=100)
    si_so = models.IntegerField()
    tinh_trang_lop = models.CharField(max_length=100)


class MonHoc(BaseModel):
    ten_mon_hoc = models.CharField(max_length=100)
    so_tin_chi = models.IntegerField()
    tinh_trang_mon = models.CharField(max_length=100)


class LopHocMonHoc(BaseModel):
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    mon_hoc = models.ForeignKey(MonHoc, on_delete=models.CASCADE)


class KhoaLuanTotNghiep(BaseModel):
    ten_khoa_luan = models.CharField(max_length=100)
    ty_le_dao_van = models.FloatField()
    diem = models.FloatField()
    sinh_vien = models.OneToOneField(SinhVien, on_delete=models.CASCADE)
    gv_phan_bien = models.ForeignKey(GiangVien, on_delete=models.PROTECT, related_name='khoa_luan_phan_bien',null=False)


class KLTNGVHuongDan(BaseModel):
    khoa_luan = models.ForeignKey(KhoaLuanTotNghiep, on_delete=models.CASCADE)
    gv_huong_dan = models.ForeignKey(GiangVien, on_delete=models.CASCADE)


class TieuChi(BaseModel):
    tieu_chi = models.CharField(max_length=100)
    ty_le = models.FloatField()


class KLTNTieuChi(BaseModel):
    khoa_luan = models.ForeignKey(KhoaLuanTotNghiep, on_delete=models.CASCADE)
    tieu_chi = models.ForeignKey(TieuChi, on_delete=models.CASCADE)


class HoiDongBVKL(BaseModel):
    ngay_bao_ve = models.DateField()


class Diem(BaseModel):
    tieu_chi = models.CharField(max_length=100)
    diem = models.FloatField()
    khoa_luan = models.ForeignKey(KhoaLuanTotNghiep, on_delete=models.CASCADE)
    giang_vien = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
    hoi_dong_bvkl = models.ForeignKey(HoiDongBVKL, on_delete=models.CASCADE)


class VaiTro(BaseModel):
    khoa_luan = models.ForeignKey(KhoaLuanTotNghiep, on_delete=models.CASCADE)
    gv = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
    hoi_dong_bvkl = models.ForeignKey(HoiDongBVKL, on_delete=models.CASCADE)
    vai_tro = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in ChucVu])



