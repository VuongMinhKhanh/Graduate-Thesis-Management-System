from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from theses.models import NguoiDung, KhoaLuanTotNghiep, HoiDongBVKL, SinhVien, GiangVien, KLTNGVHuongDan, Diem, TieuChi, \
    GiaoVu, Lop, NganhHoc


class NguoiDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiDung
        fields = ["first_name", "last_name", "username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}} # trường password chỉ để đăng ký, đừng đọc, trả về

    def create(self, validated_data): # validate data, hash mật khẩu
        data = validated_data.copy()

        user = NguoiDung(**data) # tương đương username=User["username"] (giống nhau username nên tự hiểu)
        user.set_password(user.password) # băm password
        user.save()

        return user


class LopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lop
        fields = ["ten_lop"]


class SinhVienSerializer(NguoiDungSerializer):
    # lop = LopSerializer()

    class Meta(NguoiDungSerializer.Meta):
        model = SinhVien
        fields = NguoiDungSerializer.Meta.fields + ["nam_nhap_hoc", "lop"]

    def create(self, validated_data): # validate data, hash mật khẩu
        data = validated_data.copy()

        user = SinhVien(**data) # tương đương username=User["username"] (giống nhau username nên tự hiểu)
        user.set_password(user.password) # băm password
        user.save()

        return user


class GiangVienSerializer(NguoiDungSerializer):
    class Meta(NguoiDungSerializer.Meta):
        model = GiangVien
        fields = NguoiDungSerializer.Meta.fields + ["bang_cap", "kinh_nghiem"]

    def create(self, validated_data): # validate data, hash mật khẩu
        data = validated_data.copy()

        user = GiangVien(**data) # tương đương username=User["username"] (giống nhau username nên tự hiểu)
        user.set_password(user.password) # băm password
        user.save()

        return user


class GiaoVuSerializer(NguoiDungSerializer):
    class Meta(NguoiDungSerializer.Meta):
        model = GiaoVu
        fields = NguoiDungSerializer.Meta.fields + ["trinh_do"]

    def create(self, validated_data): # validate data, hash mật khẩu
        data = validated_data.copy()

        user = GiaoVu(**data) # tương đương username=User["username"] (giống nhau username nên tự hiểu)
        user.set_password(user.password) # băm password
        user.save()

        return user


class HDBVKLSerializer(ModelSerializer):
    giang_viens = NguoiDungSerializer(many=True)

    class Meta:
        model = HoiDongBVKL
        fields = ["giang_viens"]


class NganhHocSerializer(ModelSerializer):
    class Meta:
        model = NganhHoc
        fields = ['id', 'ten_nganh', 'created_date']


class GVHuongDanSerializer(ModelSerializer):
    gv_huong_dan = GiangVienSerializer(many=True)

    class Meta:
        model = KLTNGVHuongDan
        fields = ["gv_huong_dan"]


class KLTNSerializer(ModelSerializer):
    mssv = SinhVienSerializer()

    class Meta:
        model = KhoaLuanTotNghiep
        fields = [
            'id',
            'ten_khoa_luan',
            'ty_le_dao_van',
            'created_date',
            'diem_tong',
            'trang_thai',
            'mssv',
        ]


class KLTNDetailsSerializer(KLTNSerializer):
    # hoidongbvkl_set = HDBVKLSerializer(many=True)
    gv_huong_dan = serializers.SerializerMethodField() # what???

    class Meta:
        model = KhoaLuanTotNghiep
        fields = KLTNSerializer.Meta.fields + ['gv_huong_dan'] # dupe key nest
            # 'gv_phan_bien',

    def get_gv_huong_dan(self, obj):
        gv_huong_dan = KLTNGVHuongDan.objects.filter(kltn=obj)
        return GVHuongDanSerializer(gv_huong_dan, many=True).data


class TieuChiSerializer(ModelSerializer):
    class Meta:
        model = TieuChi
        fields = ["tieu_chi", "ty_le"]


class DiemSerializer(ModelSerializer):
    tieu_chi = TieuChiSerializer()
    gv = NguoiDungSerializer()

    class Meta:
        model = Diem
        fields = "__all__"



