from django.db import models
from django.contrib.auth.models import AbstractUser

from enum import Enum
# Create your models here.


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    updated_date = models.DateTimeField(auto_now=True,null=True)
    class Meta:
        abstract = True


class TrangThai(models.Model):
    trang_thai = models.BooleanField(default=True)
    class Meta:
        abstract = True



class NguoiDung(AbstractUser):
    pass
    # Kế thừa từ BaseModel và kết nối với AbstractUser để lưu thông tin người dùng
    # Thêm các trường thông tin người dùng khác nếu cần


class GiaoVu(BaseModel):
    trinh_do = models.CharField(max_length=100)
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE)


class GiangVien(BaseModel):
    bang_cap = models.CharField(max_length=100)
    kinh_nghiem = models.CharField(max_length=255)
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE)


class SinhVien(BaseModel):
    mssv = models.CharField(primary_key=True,max_length=20, unique=True)
    nam_nhap_hoc = models.IntegerField()
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE)
    lop = models.ForeignKey('Lop', on_delete=models.PROTECT, null=False)


class Lop(BaseModel,TrangThai):
    ten_lop = models.CharField(max_length=100)
    si_so = models.IntegerField()


class NghanhHoc(BaseModel,TrangThai):
    # Thông tin về ngành học
    ten_nganh = models.CharField(max_length=100)
    so_tin_chi = models.IntegerField()


class LopHocNghanhHoc(BaseModel):
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    nghanh_hoc = models.ForeignKey(NghanhHoc, on_delete=models.CASCADE)


class KhoaLuanTotNghiep(BaseModel):
    ten_khoa_luan = models.CharField(max_length=200)
    ty_le_dao_van = models.FloatField()
    diem_tong = models.FloatField()
    mssv = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    id_gv_phan_bien = models.ForeignKey(GiangVien, on_delete=models.CASCADE)


class KLTNGVHuongDan(BaseModel):
    id_kltn = models.ForeignKey(KhoaLuanTotNghiep, on_delete=models.CASCADE)
    id_gv_huong_dan = models.ForeignKey(GiangVien, on_delete=models.CASCADE)


class TieuChi(BaseModel):
    tieu_chi = models.CharField(max_length=200)
    ty_le = models.FloatField()
    id_kltn = models.ManyToManyField(KhoaLuanTotNghiep, blank=True)


class HoiDongBVKL(BaseModel,TrangThai):
    # Thông tin về Hội đồng bảo vệ khóa luận
    ngay_bao_ve = models.DateField()


class Diem(BaseModel):
    # Điểm của từng tiêu chí của khóa luận
    tieu_chi = models.CharField(max_length=200)
    diem = models.FloatField()
    id_kltn = models.ForeignKey(KhoaLuanTotNghiep, on_delete=models.CASCADE)
    id_gv = models.ForeignKey(GiangVien, on_delete=models.CASCADE)


class VaiTro(BaseModel):
    class ChucVu(Enum):
        CHU_TICH = 1
        THU_KY = 2
        THANH_VIEN = 3
    id_kltn = models.ForeignKey(KhoaLuanTotNghiep, on_delete=models.CASCADE)
    id_gv = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
    vai_tro = models.CharField(max_length=100, choices=[(chuc_vu.value, chuc_vu.name) for chuc_vu in ChucVu])