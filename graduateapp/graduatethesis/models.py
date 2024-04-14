from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from enum import Enum
# Create your models here.


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class TrangThai(BaseModel):
    trang_thai = models.BooleanField(default=True)

    class Meta:
        abstract = True


class NguoiDung(AbstractUser):
<<<<<<< HEAD
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    avatar = models.ImageField(upload_to='graduatethesis/%Y/%m', default='static/graduatethesis/defaultavatar.jpg')
=======
    avatar = models.ImageField(upload_to='graduatethesis/%Y/%m', default='static/graduatethesis/Quy trình tập luyện sau khi thuộc động tác nhưng chưa có tempo.png.jpg')
>>>>>>> 63c929eccace6850854bc7bbcaaa2300c373d158
    # Kế thừa từ BaseModel và kết nối với AbstractUser để lưu thông tin người dùng
    # Thêm các trường thông tin người dùng khác nếu cần


class GiaoVu(NguoiDung):
<<<<<<< HEAD
    trinh_do = models.CharField(max_length=100)
    class Meta:
        #đặt lại tên hiển thị ra trang admin
        verbose_name_plural = ('Giáo Vụ')
    def __str__(self):
        return (self.first_name+self.last_name)

class GiangVien(NguoiDung):
    bang_cap = models.CharField(max_length=100)
    kinh_nghiem = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = ('Giảng Viên')
    def __str__(self):
        return (self.first_name+self.last_name)


class SinhVien(NguoiDung):
=======
    class Meta:
        verbose_name = "Giáo Vụ"
        verbose_name_plural = verbose_name

    trinh_do = models.CharField(max_length=100)


class GiangVien(NguoiDung):
    class Meta:
        verbose_name = "Giảng Viên"
        verbose_name_plural = verbose_name

    bang_cap = models.CharField(max_length=100)
    kinh_nghiem = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class SinhVien(NguoiDung):
    class Meta:
        verbose_name = "Sinh Viên"
        verbose_name_plural = verbose_name

>>>>>>> 63c929eccace6850854bc7bbcaaa2300c373d158
    mssv = models.CharField(primary_key=True,max_length=20, unique=True)
    nam_nhap_hoc = models.IntegerField()
    lop = models.ForeignKey('Lop', on_delete=models.PROTECT, null=False)

    class Meta:
        verbose_name_plural = ('Sinh Viên')
    def __str__(self):
        return (self.first_name + self.last_name)


<<<<<<< HEAD

class Lop(TrangThai):
=======
class Lop(BaseModel, TrangThai):
>>>>>>> 63c929eccace6850854bc7bbcaaa2300c373d158
    ten_lop = models.CharField(max_length=100)
    si_so = models.IntegerField()

    def __str__(self):
        return self.ten_lop


<<<<<<< HEAD
class NghanhHoc(TrangThai):
=======
class NganhHoc(BaseModel,TrangThai):
>>>>>>> 63c929eccace6850854bc7bbcaaa2300c373d158
    # Thông tin về ngành học
    ten_nganh = models.CharField(max_length=100)
    so_tin_chi = models.IntegerField()

    def __str__(self):
        return self.ten_nganh


class LopHocNganhHoc(BaseModel):
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    nganh_hoc = models.ForeignKey(NganhHoc, on_delete=models.CASCADE)


<<<<<<< HEAD
class KhoaLuanTotNghiep(TrangThai):
=======
class KhoaLuanTotNghiep(BaseModel, TrangThai):
>>>>>>> 63c929eccace6850854bc7bbcaaa2300c373d158
    ten_khoa_luan = models.CharField(max_length=200)
    ty_le_dao_van = models.FloatField()
    diem_tong = models.FloatField()
    mssv = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
<<<<<<< HEAD
    class Meta:
        unique_together=('id','mssv')
=======
    gv_phan_bien = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
>>>>>>> 63c929eccace6850854bc7bbcaaa2300c373d158

    def __str__(self):
        return self.ten_khoa_luan


class KLTNGVHuongDan(BaseModel):
    kltn = models.ForeignKey(KhoaLuanTotNghiep, on_delete=models.CASCADE)
    gv_huong_dan = models.ForeignKey(GiangVien, on_delete=models.CASCADE)


class TieuChi(BaseModel):
    tieu_chi = models.CharField(max_length=200)
    ty_le = models.FloatField()
<<<<<<< HEAD
    kltn = models.ManyToManyField(KhoaLuanTotNghiep,blank=True)
=======
    kltn = models.ManyToManyField(KhoaLuanTotNghiep, blank=True)

>>>>>>> 63c929eccace6850854bc7bbcaaa2300c373d158
    def __str__(self):
        return self.tieu_chi


<<<<<<< HEAD
class HoiDongBVKL(TrangThai):
=======
class HoiDongBVKL(BaseModel, TrangThai):
>>>>>>> 63c929eccace6850854bc7bbcaaa2300c373d158
    # Thông tin về Hội đồng bảo vệ khóa luận
    gv_phan_bien = models.ForeignKey(GiangVien,related_name="gv_phan_bien", on_delete=models.CASCADE)
    chu_tich = models.ForeignKey(GiangVien, related_name="chu_tich",on_delete=models.CASCADE)
    thu_ky = models.ForeignKey(GiangVien, related_name="thu_ky",on_delete=models.CASCADE)
    thanh_vien = models.ManyToManyField(GiangVien,blank=True)
    ngay_bao_ve = models.DateField()


class Diem(BaseModel):
    # Điểm của từng tiêu chí của khóa luận
    tieu_chi = models.ForeignKey(TieuChi, on_delete=models.PROTECT, default=1)
    diem = models.FloatField()
    gv = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
<<<<<<< HEAD
    kltn = models.ForeignKey(KhoaLuanTotNghiep,on_delete=models.CASCADE)
    class Meta:
        unique_together=('tieu_chi','gv','kltn')
=======
    kltn = models.ForeignKey(KhoaLuanTotNghiep, on_delete=models.CASCADE)

    class Meta:
        unique_together=('tieu_chi','gv','kltn')


class VaiTro(BaseModel):
    class ChucVu(Enum):
        CHU_TICH = 1
        THU_KY = 2
        THANH_VIEN = 3

    hdbvkl = models.ForeignKey(HoiDongBVKL, on_delete=models.CASCADE)
    gv = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
    vai_tro = models.IntegerField(choices=[(chuc_vu.value, chuc_vu.name) for chuc_vu in ChucVu])
>>>>>>> 63c929eccace6850854bc7bbcaaa2300c373d158
