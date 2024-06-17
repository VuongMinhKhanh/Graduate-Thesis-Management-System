import requests
from django.conf.global_settings import DATE_FORMAT
from django.db.models import Avg, Count, Q, Sum, F, FloatField
from django.db.models.functions import ExtractYear, Round, Cast
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from theses.utils import *
from theses.export_pdf import export_pdf
from theses.models import *
from theses.serializers import *
from theses import serializers, pagination, my_permission, send_mail


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = NguoiDung.objects.filter(is_active=True)
    serializer_class = NguoiDungSerializer
    parser_classes = [MultiPartParser, ]  # nhận dữ liệu là file

    def get_permissions(self):
        if self.action in ["get_current_user"]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=["get, patch"], url_path="current-user", detail=False)
    def get_current_user(self, request):
        user = request.user

        if request.method.__eq__("patch"):
            for k, v in request.data.items():
                setattr(user, k, v)
                user.save()

        return Response(serializers.NguoiDungSerializer(user).data)


class SinhVienViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = SinhVien.objects.filter(is_active=True)
    serializer_class = SinhVienSerializer
    parser_classes = [MultiPartParser, ]  # nhận dữ liệu là file

    def get_permissions(self):
        if self.action in ["get_current_user"]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=["get, patch"], url_path="current-user", detail=False)
    def get_current_user(self, request):
        user = request.user

        if request.method.__eq__("patch"):
            for k, v in request.data.items():
                setattr(user, k, v)
                user.save()

        return Response(serializers.SinhVienSerializer(user).data)


class GiangVienViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = GiangVien.objects.filter(is_active=True)
    serializer_class = GiangVienSerializer
    parser_classes = [MultiPartParser, ]  # nhận dữ liệu là file

    def get_permissions(self):
        if self.action in ["get_current_user"]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=["get, patch"], url_path="current-user", detail=False)
    def get_current_user(self, request):
        user = request.user

        if request.method.__eq__("patch"):
            for k, v in request.data.items():
                setattr(user, k, v)
                user.save()

        return Response(serializers.GiangVienSerializer(user).data)


class GiaoVuViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = GiaoVu.objects.filter(is_active=True)
    serializer_class = GiaoVuSerializer
    parser_classes = [MultiPartParser, ]  # nhận dữ liệu là file

    def get_permissions(self):
        if self.action in ["get_current_user"]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=["get, patch"], url_path="current-user", detail=False)
    def get_current_user(self, request):
        user = request.user

        if request.method.__eq__("patch"):
            for k, v in request.data.items():
                setattr(user, k, v)
                user.save()

        return Response(serializers.GiaoVuSerializer(user).data)


class KLTNViewSet(viewsets.ViewSet, generics.ListAPIView, generics.UpdateAPIView,generics.CreateAPIView):
    queryset = KhoaLuanTotNghiep.objects.all()  # filter(trang_thai=True)
    serializer_class = KLTNSerializer
    permission_classes = [my_permission.GiaoVuPermissionUser]

    @action(methods=["patch"], detail=True)
    def change_thesis_status(self, request, *args, **kwargs):
        kltn = self.get_object()
        new_status = request.data.get("trang_thai", None)

        if isinstance(new_status, str):
            new_status = new_status.lower() == 'true'

        if new_status is not None:
            kltn.trang_thai = new_status

            if not new_status:
                # auth_header = request.headers.get('Authorization')
                # token = auth_header.split(' ')[1] if auth_header else None
                # headers = {'Authorization': f'Bearer {token}'}

                # scores_api = requests.get(f'{settings.BASE_URL}/Diem/{kwargs.get("pk")}/get_avg_score/', headers=headers)

                kltn.diem_tong = calculate_average_score(kwargs.get("pk")) # scores_api.json().get("avg_score")
                kltn.save()

                data = self.get_serializer(kltn).data
                print(data)
                send_mail.send_mail_for_thesis(data)
                # print(some_view(data))

                return Response({
                    "data": data,
                })

            kltn.save()
            data = self.get_serializer(kltn).data

            return Response(data)
        else:
            return Response({'error': 'New status not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="avg_score", detail=False)
    def get_avg_score(self, request):
        year = request.GET.get('year', None)
        years = KhoaLuanTotNghiep.objects.values_list("created_date__year", flat=True).distinct()

        average_scores = (KhoaLuanTotNghiep.objects
                          .filter(diem_tong__isnull=False)
                          .values("id", "ten_khoa_luan", "diem_tong", "created_date", "created_date__year", "created_date__month", "created_date__day"))

        if year:
            average_scores = average_scores.filter(created_date__year=year)
            context = {
                "average_scores": average_scores,
                "years": years,
                "request_year": int(year),
            }
        else:
            context = {
                "average_scores": average_scores,
                "years": years,
                "request_year": None,
            }

            return Response(context)
        # queryset = self.queryset
        #
        # year = self.request.query_params.get("year")
        # if year:
        #     queryset = queryset.filter(created_date__year=year)
        #
        # faculty = self.request.query_params.get("fac")
        # if faculty:
        #     queryset = queryset.filter(sinh_vien__nganh=faculty)
        #
        # avg_score = queryset.aggregate(Avg("diem"))
        #
        # return Response({"avg_score": avg_score["diem__avg"]})

    @action(methods=["get"], url_path="frequency", detail=False)
    def get_frequency(self, request):
        faculties = NganhHoc.objects.all()

        freq_stats = (NganhHoc.objects.annotate(
            freq=Count("lop__sinhvien__khoaluantotnghiep"),
        ).values("id", "ten_nganh", "created_date", "freq"))

        faculties_serialized = NganhHocSerializer(faculties, many=True).data

        context = {
            "freq_stats": freq_stats,
            "faculties": faculties_serialized,
        }

        return Response(context)

    @action(methods=['post'], url_path='add', detail=False)
    def add_KLTN(self, request):
        # lấy danh sách cách mssv gửi trên body
        sinh_vien_list = request.data.get('mssv', [])

        if len(sinh_vien_list) == 0:
            return Response({"error": "Phải có ít nhất một sinh viên mới được tạo"}, status.HTTP_400_BAD_REQUEST)

        ten_khoa_luan = request.data.get("ten_khoa_luan")
        ty_le_dao_van = request.data.get("ty_le_dao_van")
        diem_tong = request.data.get("diem_tong")
        c = KhoaLuanTotNghiep.objects.create(ten_khoa_luan=ten_khoa_luan, ty_le_dao_van=ty_le_dao_van,
                                             diem_tong=diem_tong)
        # thêm từng sinh viên vào KLTN
        for mssv in sinh_vien_list:
            if not SinhVien.objects.filter(mssv=mssv.get('mssv')).exists():
                return Response({"error": f"Sinh viên với mã số sinh viên: {mssv.get('mssv')} không tồn tại."},
                                status=status.HTTP_400_BAD_REQUEST)
            sinhVien = SinhVien.objects.get(mssv=mssv.get('mssv'))
            c.mssv.add(sinhVien)
        return Response(serializers.KLTNSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=["patch"], url_path="add_hdbvkl", detail=True)
    def add_HDBVKL(self, request, pk=None):
        hdbvkl_id = request.data.get("hdbvkl")

        if hdbvkl_id is None:
            return Response("Vui lòng cung cấp ID của hội đồng bảo vệ khóa luận", status=status.HTTP_400_BAD_REQUEST)

        try:
            hdbvkl = HoiDongBVKL.objects.get(pk=hdbvkl_id)
        except HoiDongBVKL.DoesNotExist:
            return Response("Hội đồng bảo vệ khóa luận không tồn tại", status=status.HTTP_404_NOT_FOUND)

        if hdbvkl.khoaluantotnghiep_set.count() >= 5:
            return Response("Hội đồng bảo vệ khóa luận đã chấm tối đa 5 khóa luận tốt nghiệp",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            kltn = KhoaLuanTotNghiep.objects.get(pk=pk)
        except KhoaLuanTotNghiep.DoesNotExist:
            return Response("Khóa luận tốt nghiệp không tồn tại", status=status.HTTP_404_NOT_FOUND)

        kltn.hdbvkl = hdbvkl
        kltn.save()
        response_data = {
            "message": "Thêm thành công",
            "kltn": {
                "id": kltn.id,
                "ten_khoa_luan": kltn.ten_khoa_luan,
                "diem_tong": kltn.diem_tong,
                "hdbvkl": {
                    "id": hdbvkl.id
                }
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='add_gvhd', detail=True)
    def add_GiangVienHuongDan(self, request, pk):
        try:
            khoaluan = KhoaLuanTotNghiep.objects.get(id=pk)
        except KhoaLuanTotNghiep.DoesNotExist:
            return Response({"error": "Không tìm thấy khóa luận tốt nghiệp"}, status=status.HTTP_404_NOT_FOUND)

        kltngv_huong_dan = khoaluan.kltngvhuongdan_set.first()
        if kltngv_huong_dan is None:
            kltngv_huong_dan = KLTNGVHuongDan.objects.create(kltn=khoaluan)

        c = kltngv_huong_dan.gv_huong_dan.count()
        gv_huong_dan_list = request.data.get("gv_huong_dan", [])

        if (c + len(gv_huong_dan_list)) > 2:
            return Response({"error": "Số lượng giảng viên hướng dẫn đã đạt tối đa"},
                            status=status.HTTP_400_BAD_REQUEST)

        for id in gv_huong_dan_list:
            gv_id = id.get("id")
            if not GiangVien.objects.filter(id=gv_id).exists():
                return Response({"error": f"Giảng viên có id: {gv_id} không tồn tại!"},
                                status=status.HTTP_400_BAD_REQUEST)

            gv = GiangVien.objects.get(id=gv_id)
            kltngv_huong_dan.gv_huong_dan.add(gv)

        return Response("Thêm thành công", status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path="add_tieu_chi_vao_kltn", detail=True)
    def add_tieuchi(self, request, pk=None):
        if KhoaLuanTotNghiep.objects.filter(pk=pk).exists():
            kltn = KhoaLuanTotNghiep.objects.get(pk=pk)
            tieuchi_list = request.data.get('tieu_chi', [])

            for tieuchi_id in tieuchi_list:
                if TieuChi.objects.filter(pk=tieuchi_id).exists():
                    tieuchi = TieuChi.objects.get(pk=tieuchi_id)
                    kltn.tieu_chi.add(tieuchi)
                else:
                    return Response(
                        {"error": f"Không tồn tại tiêu chí có id là: {tieuchi_id}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response("Thêm thành công", status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": f"Không tồn tại Khóa luận tốt nghiệp có id là: {pk}"},
                status=status.HTTP_400_BAD_REQUEST
            )
class HDBVKLViewSet(viewsets.ViewSet,generics.ListAPIView,generics.UpdateAPIView,generics.CreateAPIView):
    queryset = HoiDongBVKL.objects.all()
    serializer_class = HDBVKLSerializer
    permission_classes = [my_permission.GiaoVuPermissionUser]

    @action(methods=["get"], detail=True)
    def get_hdbvkl(self, request, **kwargs):
        # send_mail.send_mail_for_thesis(queryset)

        pk = kwargs.get("pk")
        hdbvkl = self.queryset.get(pk=pk)
        serializer = self.get_serializer(hdbvkl)

        # send_mail.send_mail_for_thesis(serializer.data)

        return Response(serializer.data)

    @action(methods="post", detail=False)
    def add_hdbvkl(self, request):
        gv_phanbien = GiangVien.objects.get(id=request.data.get("gv_phan_bien"))
        chu_tich = GiangVien.objects.get(id=request.data.get("chu_tich"))
        thu_ky = GiangVien.objects.get(id=request.data.get("thu_ky"))
        ngay_bao_ve = request.data.get("ngay_bao_ve")
        hd = HoiDongBVKL.objects.create(gv_phan_bien=gv_phanbien, chu_tich=chu_tich, thu_ky=thu_ky,
                                        ngay_bao_ve=ngay_bao_ve)
        thanh_vien_list = request.data.get("thanh_vien", [])
        if (len(thanh_vien_list) <= 2):
            for thanh_vien in thanh_vien_list:
                if GiangVien.objects.filter(pk=thanh_vien).exists():
                    thanh_vien = GiangVien.objects.get(pk=thanh_vien)
                    hd.thanh_vien.add(thanh_vien)
                else:
                    return Response({"error": f"thành viên có id {thanh_vien} thêm vào không hợp lệ"},
                                    status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers.HDBVKLSerializer(hd), status=status.HTTP_201_CREATED)

    @action(methods=["patch"], url_path="trang_thai_hdbvkl", detail=True)
    def khoa_hdbvkl(self, request, pk):
        try:
            hdbvkl = HoiDongBVKL.objects.get(pk=pk)
            # Đảo ngược giá trị hiện tại của trang_thai
            hdbvkl.trang_thai = not hdbvkl.trang_thai
            hdbvkl.save()
            return Response({"message": "Cập nhật trạng thái thành công", "trang_thai": hdbvkl.trang_thai},
                            status=status.HTTP_200_OK)
        except HoiDongBVKL.DoesNotExist:
            return Response({"error": "Hội đồng bảo vệ khóa luận không tồn tại"}, status=status.HTTP_404_NOT_FOUND)


class TieuChiViewSet(viewsets.ViewSet,generics.ListAPIView,generics.CreateAPIView):
    queryset = TieuChi.objects.all()
    serializer_class = TieuChiSerializer
    permission_classes = [my_permission.GiaoVuPermissionUser]


class DiemViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView,generics.CreateAPIView,generics.UpdateAPIView):
    queryset = Diem.objects.all()
    serializer_class = DiemSerializer
    permission_classes = [my_permission.GiangVienPermissionUser]

    @action(methods=["get"], detail=True)
    def get_thesis_scores(self, request, **kwargs):
        queryset = Diem.objects.filter(kltn=kwargs.get("pk"))
        data = self.get_serializer(queryset, many=True).data

        return Response(data)

    @action(methods=["get"], detail=True)
    def export_pdf(self, request, **kwargs):
        queryset = Diem.objects.filter(kltn=kwargs.get("pk"))
        # thesis_name = KhoaLuanTotNghiep.objects.filter(id=kwargs.get("pk")).first().ten_khoa_luan
        thesis_name = KhoaLuanTotNghiep.objects.filter(id=kwargs.get("pk")).first().ten_khoa_luan
        data = self.get_serializer(queryset, many=True).data
        if request.user.is_authenticated:
            export_pdf(data, thesis_name, [request.user.email, "2151050191khanh@ou.edu.vn"])
        else:
            export_pdf(data, thesis_name, ["2151050191khanh@ou.edu.vn"])

        return Response(f"Export successfully to {request.user.email if request.user.is_authenticated else request.user}!", status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def calculate_current_score(self, request, **kwargs):
        print(calculate_average_score(kwargs.get("pk")))
        return Response(calculate_average_score(kwargs.get("pk")))

    # @action(methods=["get"], detail=True)
    # def get_avg_score(self, request, **kwargs):
    #     # queryset = Diem.objects.filter(kltn=kwargs.get("pk"))
    #     # avg_score = queryset.aggregate(Avg("diem"))
    #
    #     average_scores = (KhoaLuanTotNghiep.objects.filter(id=kwargs.get("pk"))
    #                       .annotate(
    #         average_score=Round(
    #             Sum(Cast(F('diem__diem') * F('diem__tieu_chi__ty_le') / 100, FloatField())) / Count('diem__gv',
    #                                                                                                 distinct=True), 2)
    #     ).values("average_score"))
    #     # print(average_scores)
    #     return Response({
    #         "avg_score": average_scores[0]["average_score"]
    #     })

    # @action(methods=["patch"], detail=True)
    # def change_thesis_score(self, request, **kwargs):
    #     # request: diem, tieu chi, lec
    #     diem = self.get_object(kltn=kwargs.get("pk"))
    @action(methods=["post"], url_path="add", detail=False)
    def add_diem(self, request):
        # Lấy dữ liệu từ request
        kltn_id = request.data.get('kltn')
        diem = request.data.get('diem')
        tieuchi_id = request.data.get("tieuchi")
        giangvien = request.user.id

        try:
            # Lấy đối tượng KhoaLuanTotNghiep từ ID
            kltn = KhoaLuanTotNghiep.objects.get(pk=kltn_id)
            if kltn.hdbvkl.trang_thai == False:
                return Response({"error": "Hội đồng đã bị khóa nên không thể sửa điểm"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Lấy hội đồng bảo vệ khóa luận liên quan đến KhoaLuanTotNghiep này
            hdbvkl = kltn.hdbvkl

            ## lấy giảng viên đang thêm điểm vào
            giangvien = GiangVien.objects.get(pk=giangvien)

            if not check_giang_vien_in_hdbv_kltn(giangvien=giangvien, kltn=kltn):
                return Response({"error": "Bạn không nằm trong hội đồng bảo vệ khóa luận này"},
                                status=status.HTTP_400_BAD_REQUEST)

            tieuchi = kltn.tieu_chi.get(pk=tieuchi_id)
            if not check_tieu_chi_in_kltn(tieuchi=tieuchi, kltn=kltn):
                return Response({"error": "Tiêu chí không nằm trong khóa luận tốt nghiệp này"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Tạo và lưu đối tượng Diem
            Diem.objects.create(
                tieu_chi=tieuchi,
                diem=diem,
                gv=giangvien,
                kltn=kltn
            )
            # cập nhật điểm Tong
            kltn.diem_tong = calculate_diem_tong(kltn)
            kltn.save()
            # Ghi lại hành động vào ActionLog
            ActionLog.objects.create(
                user=giangvien,
                action=f"Thêm điểm cho tiêu chí {tieuchi_id} của khóa luận {kltn_id}"
            )
            return Response("Thêm điểm thành công", status=status.HTTP_201_CREATED)

        except KhoaLuanTotNghiep.DoesNotExist:
            return Response({"error": "Không tìm thấy khóa luận tốt nghiệp"}, status=status.HTTP_404_NOT_FOUND)
        except TieuChi.DoesNotExist:
            return Response({"error": "Không tìm thấy tiêu chí"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["patch"], url_path="update", detail=True)
    def update_diem(self, request, pk):
        diem_id = pk  # Sử dụng pk từ URL để xác định điểm cần sửa
        new_diem_value = request.data.get('diem')
        giangvien_id = request.user.id  # Lấy ID của giảng viên đang đăng nhập

        # Kiểm tra xem dữ liệu có đầy đủ không
        if new_diem_value is None:
            return Response({"error": "Dữ liệu không đầy đủ"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Lấy đối tượng Diem từ ID
            diem_obj = Diem.objects.get(pk=diem_id)

            # Kiểm tra xem giảng viên hiện tại có phải là người đã thêm điểm trước đó không
            if diem_obj.gv.id != giangvien_id:
                return Response({"error": "Bạn chỉ có thể sửa điểm của chính mình"}, status=status.HTTP_403_FORBIDDEN)

            # Lấy đối tượng KhoaLuanTotNghiep từ Diem
            kltn = diem_obj.kltn
            if kltn.hdbvkl.trang_thai==False:
                return Response({"error": "Hội đồng đã bị khóa nên không thể sửa điểm"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Cập nhật giá trị điểm mới
            old_diem_value = diem_obj.diem
            diem_obj.diem = new_diem_value
            diem_obj.save()

            # Ghi lại hành động vào ActionLog
            giangvien = request.user
            ActionLog.objects.create(
                user=giangvien,
                action=f"Sửa điểm cho tiêu chí {diem_obj.tieu_chi.id} của khóa luận {kltn.id} từ {old_diem_value} thành {new_diem_value}"
            )
            # Cập nhật điểm tổng của KhoaLuanTotNghiep
            calculate_diem_tong(kltn)

            return Response({
                "message": "Sửa điểm thành công",
                "diem": {
                    "id": diem_obj.id,
                    "new_diem_value": new_diem_value,
                    "kltn": kltn.trang_thai,
                    "tieu_chi": diem_obj.tieu_chi.tieu_chi,
                    "old_diem_value": old_diem_value
                }
            }, status=status.HTTP_200_OK)

        except Diem.DoesNotExist:
            return Response({"error": "Không tìm thấy điểm"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def calculate_average_score(pk):
    average_scores = (KhoaLuanTotNghiep.objects.filter(id=pk)
                      .annotate(
        average_score=Round(
            Sum(Cast(F('diem__diem') * F('diem__tieu_chi__ty_le') / 100, FloatField())) / Count('diem__gv',
                                                                                                distinct=True), 2)
    ).values("average_score"))
    # print(average_scores)
    return average_scores[0]["average_score"]


class KLTNDetailsViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = KhoaLuanTotNghiep.objects.all()
    serializer_class = KLTNDetailsSerializer
    permission_classes = [my_permission.SinhVienPermissionUser]

    @action(methods=["get"], detail=True)
    def get_thesis_details(self, request, **kwargs):
        queryset = KhoaLuanTotNghiep.objects.filter(id=kwargs.get("pk")).first()
        data = self.get_serializer(queryset).data

        return Response(data)
