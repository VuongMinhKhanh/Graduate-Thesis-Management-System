import requests
from django.conf.global_settings import DATE_FORMAT
from django.db.models import Avg, Count, Q, Sum, F, FloatField
from django.db.models.functions import ExtractYear, Round, Cast
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from theses.export_pdf import export_pdf
from theses.models import KhoaLuanTotNghiep, HoiDongBVKL, NguoiDung, Diem, SinhVien, GiangVien, GiaoVu, NganhHoc
from theses.serializers import KLTNSerializer, HDBVKLSerializer, NguoiDungSerializer, DiemSerializer, \
    SinhVienSerializer, GiaoVuSerializer, GiangVienSerializer, NganhHocSerializer, KLTNDetailsSerializer
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


class KLTNViewSet(viewsets.ViewSet, generics.ListAPIView, generics.UpdateAPIView):
    queryset = KhoaLuanTotNghiep.objects.all()  # filter(trang_thai=True)
    serializer_class = KLTNSerializer
    # permission_classes = [my_permission.KLTNPermissionUser]

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


class HDBVKLViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = HoiDongBVKL.objects.all()
    serializer_class = HDBVKLSerializer
    permission_classes = [my_permission.KLTNPermissionUser]

    @action(methods=["get"], detail=True)
    def get_hdbvkl(self, request, **kwargs):
        # send_mail.send_mail_for_thesis(queryset)

        pk = kwargs.get("pk")
        hdbvkl = self.queryset.get(pk=pk)
        serializer = self.get_serializer(hdbvkl)

        # send_mail.send_mail_for_thesis(serializer.data)

        return Response(serializer.data)


class DiemViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Diem.objects.all()
    serializer_class = DiemSerializer
    # permission_classes = [my_permission.KLTNPermissionUser]

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
