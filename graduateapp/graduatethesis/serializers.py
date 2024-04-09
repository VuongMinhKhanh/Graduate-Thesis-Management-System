from rest_framework import serializers
from graduatethesis.models import (NguoiDung,SinhVien,GiaoVu,GiangVien,HoiDongBVKL,KhoaLuanTotNghiep,NghanhHoc
,KLTNGVHuongDan,Lop,LopHocNghanhHoc,TieuChi,Diem,VaiTro)

class NguoiDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiDung
        fields = '__all__'


class SinhVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinhVien
        fields = '__all__'

class GiangVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiangVien
        fields = '__all__'


class GiaoVuSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiaoVu
        fields = '__all__'


class HoiDongBVKLSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoiDongBVKL
        fields = '__all__'


class KhoaLuanTotNghiepSerializer(serializers.ModelSerializer):
    class Meta:
        model = KhoaLuanTotNghiep
        fields = '__all__'


class LopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lop
        fields = '__all__'

class NghanhHocSerializer(serializers.ModelSerializer):
    class Meta:
        model = NghanhHoc
        fields = '__all__'


class LopHocNghanhHocSerializer(serializers.ModelSerializer):
    class Meta:
        model = LopHocNghanhHoc
        fields = '__all__'


class KLTNGVHuongDanSerializer(serializers.ModelSerializer):
    class Meta:
        model = KLTNGVHuongDan
        fields = '__all__'


class TieuChiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TieuChi
        fields = '__all__'


class DiemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diem
        fields = '__all__'


class VaiTroSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaiTro
        fields = '__all__'
