from theses.models import GiangVien,HoiDongBVKL,Diem
from django.db.models import Avg
# Kiểm tra giảng viên có nằm trong HDBVKhoaLuan của một Khóa luận tốt nghiệp không
def check_giang_vien_in_hdbv_kltn(giangvien, kltn):
    hdbvkl = kltn.hdbvkl
    giang_vien_list = set([hdbvkl.gv_phan_bien, hdbvkl.chu_tich, hdbvkl.thu_ky])
    giang_vien_list.update(hdbvkl.thanh_vien.all())
    return giangvien in giang_vien_list

# Kiểm tra tiêu chí có nằm trong Khóa luận tốt nghiệp không
def check_tieu_chi_in_kltn(tieuchi, kltn):
    return tieuchi in kltn.tieu_chi.all()
#Tính tiểm tổng
def calculate_diem_tong(kltn):
    tieu_chis = kltn.tieu_chi.all()
    total_diem = 0
    for tc in tieu_chis:
        diems = Diem.objects.filter(kltn=kltn, tieu_chi=tc)
        if diems.exists():
            avg_diem = diems.aggregate(Avg('diem'))['diem__avg']
            total_diem += avg_diem * tc.ty_le
    return total_diem