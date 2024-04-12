from graduatethesis.models import *

def load_nguoidung(params={}):
    q = NguoiDung.objects.all()

    return q