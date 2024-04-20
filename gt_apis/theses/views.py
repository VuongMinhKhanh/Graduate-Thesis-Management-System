import requests
from django.db.models import Avg, Count, Q
from django.db.models.functions import ExtractYear
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from theses.export_pdf import some_view
from theses.models import KhoaLuanTotNghiep, HoiDongBVKL, NguoiDung, Diem, SinhVien, GiangVien, GiaoVu
from theses.serializers import KLTNSerializer, HDBVKLSerializer, NguoiDungSerializer, DiemSerializer, \
    SinhVienSerializer, GiaoVuSerializer, GiangVienSerializer
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
    permission_classes = [my_permission.KLTNPermissionUser]

    @action(methods=["patch"], detail=True)
    def change_thesis_status(self, request, *args, **kwargs):
        kltn = self.get_object()
        new_status = request.data.get("trang_thai", None)

        if isinstance(new_status, str):
            new_status = new_status.lower() == 'true'

        if new_status is not None:
            kltn.trang_thai = new_status

            if not new_status:
                auth_header = request.headers.get('Authorization')
                token = auth_header.split(' ')[1] if auth_header else None
                headers = {'Authorization': f'Bearer {token}'}

                scores_api = requests.get(f'http://127.0.0.1:8000/Diem/{kwargs.get("pk")}/get_avg_score/', headers=headers)

                kltn.diem_tong = scores_api.json().get("avg_score")
                kltn.save()

                data = self.get_serializer(kltn).data
                # send_mail.send_mail_for_thesis(data)
                # print(some_view(data))

                return Response({
                    "data": data,
                    "external api response": scores_api.json()
                })

            kltn.save()
            data = self.get_serializer(kltn).data

            return Response(data)
        else:
            return Response({'error': 'New status not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="avg_score", detail=False)
    def get_avg_score(self, request):
        queryset = self.queryset

        year = self.request.query_params.get("year")
        if year:
            queryset = queryset.filter(created_date__year=year)

        faculty = self.request.query_params.get("fac")
        if faculty:
            queryset = queryset.filter(sinh_vien__nganh=faculty)

        avg_score = queryset.aggregate(Avg("diem"))

        return Response({"avg_score": avg_score["diem__avg"]})

    @action(methods=["get"], url_path="frequency", detail=False)
    def get_frequency(self, request):
        queryset = self.queryset

        year = self.request.query_params.get("year")
        if year:
            queryset = queryset.filter(created_date__year=year)

        faculty = self.request.query_params.get("fac")
        if faculty:
            queryset = queryset.filter(sinh_vien__nganh=faculty)  # getting id or name ???

        freq = queryset.aggregate(Count("id"))

        return Response({"frequency": freq["id__count"],
                         "user": serializers.NguoiDungSerializer(request.user).data,
                         "group": request.user.groups.all().values_list('name', flat=True),
                         "valid": request.user.groups.all().values_list('name', flat=True)
                        .filter(Q(name="giáo vụ") | Q(name="sinh viên")).exists()
                         })


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
    permission_classes = [my_permission.KLTNPermissionUser]

    @action(methods=["get"], detail=True)
    def get_thesis_scores(self, request, **kwargs):
        queryset = Diem.objects.filter(kltn=kwargs.get("pk"))
        data = self.get_serializer(queryset, many=True).data
        some_view(data)

        return Response(data)

    @action(methods=["get"], detail=True)
    def get_avg_score(self, request, **kwargs):
        avg_score = self.queryset.aggregate(Avg("diem"))

        return Response({
            "avg_score": avg_score["diem__avg"]
        })

    # @action(methods=["patch"], detail=True)
    # def change_thesis_score(self, request, **kwargs):
    #     # request: diem, tieu chi, lec
    #     diem = self.get_object(kltn=kwargs.get("pk"))
