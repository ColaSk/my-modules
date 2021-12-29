import re
import logging
from datetime import datetime
from pyexiv2 import Image

from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)

XMPINFO = [
    'GimbalPitchDegree', 'FlightYawDegree'
]

def get_xmp(fh):
    """获取图片中的 XMP 信息"""

    xmp_string = b''
    xml_started = False
    xml_finished = False
    for line in fh:
        open_tag = line.find(b'<x:xmpmeta')
        close_tag = line.find(b'</x:xmpmeta>')
        if open_tag != -1:
            xml_started = True
            line = line[open_tag:]
        if close_tag != -1:
            line_offset = 0
            if open_tag != -1:
                line_offset = open_tag
            line = line[:(close_tag - line_offset) + 12]
            xml_finished = True
        if xml_started:
            xmp_string += line
        if xml_finished:
            break
    return xmp_string


def xmpstr2dict(xmpstr: str):
    rt = {}
    root = ET.fromstring(xmpstr)
    for rdf in root.iter('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description'):

        attr = {key.split('}')[-1]: value for key, value in rdf.attrib.items()}
        drone_dji_dict = {drone_dji.tag.split('}')[-1]: drone_dji.text for drone_dji in rdf}

        rt.update(attr)
        rt.update(drone_dji_dict)

    return rt


class PicOperator(object):
    """图像基本操作
    1. 获取必要的图像信息
    """

    def __init__(self, path) -> None:

        self.path = path
        self.img = Image(self.path)

    def image_xmp(self):
        """由于图片中的xmp信息存储格式不尽相同, 采用自己的xmp信息读取器, 
           抛弃pyexiv2的xmp读取器
        """
        with open(self.path, 'rb') as fi:
            return xmpstr2dict(
                get_xmp(fi).decode(encoding='utf-8'))

    def image_exif(self):
        return self.img.read_exif()
    
    @staticmethod
    def convert_exif_longlat(latalt: str):
        """经纬度数据换算
        """

        if not latalt:
            return None

        latalt = latalt.split(" ")
        rt = 0
        ratio = [1, 60, 3600]

        for i, dms in enumerate(latalt):
            dms = dms.split('/')
            if len(dms) < 2:
                rt += float(dms[0]) / ratio[i]
            else:
                rt += float(dms[0]) / float(dms[1]) / ratio[i]
        return rt

    @staticmethod
    def time_format(datetime_str, datetime_format=None):

        datetime_format_full = '%Y-%m-%d %H:%M:%S'
        datetime_format_file_date = "%Y:%m:%d %H:%M:%S"

        if datetime_format:
            return datetime.strptime(datetime_str, datetime_format)

        if re.match("(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", datetime_str):
            d_t = datetime.strptime(datetime_str, datetime_format_full)
        elif re.match("(\d{4}:\d{1,2}:\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", datetime_str):
            d_t = datetime.strptime(datetime_str, datetime_format_file_date)
        else:
            raise Exception(f"{datetime_str} can't match")

        return d_t

    @staticmethod
    def groups(datas):
        """图片数据分组"""

        def near(point1, point2, acc):
            if (abs(point1[0] - point2[0]) <= acc and
                    abs(point1[1] - point2[1]) <= acc):
                return True
            return False

        def create_key(point):
            return ' '.join((str(point[0]), str(point[1])))

        rt = {}

        datas = sorted(datas, key=lambda d: d.get('datetime_original'))
        group_coordinate = (None, None)

        for pic in datas:

            pic_coordinate = (pic.get('longitude'), pic.get('latitude'))
            if not all(group_coordinate):
                key = create_key(pic_coordinate)
                group_coordinate = pic_coordinate
                rt.setdefault(key, []).append(pic)
                continue

            if (not near(pic_coordinate, group_coordinate, 0.00001)):

                break_sign = False
                for key in rt:
                    longitude, latitude = (float(coor) for coor in key.split(' '))
                    if near(pic_coordinate, (longitude, latitude), 0.00001):
                        group_coordinate = (longitude, latitude)
                        rt[key].append(pic)
                        break_sign = True
                        break

                if not break_sign:
                    key = create_key(pic_coordinate)
                    rt.setdefault(key, []).append(pic)

            else:
                key = create_key(group_coordinate)
                rt[key].append(pic)

        return rt

    def __del__(self):
        self.img.close()


def image_info(path):
    """获取一些指定的图片信息
        并不是全部的图片信息
    """
    pic_operator = PicOperator(path)

    pic_xmp = pic_operator.image_xmp()
    pic_exif = pic_operator.image_exif()

    name = path.split('/')[-1]

    make = pic_exif.get("Exif.Image.Make")
    model = pic_exif.get("Exif.Image.Model")

    gimbal_pitch = (
        float(pic_xmp.get(XMPINFO[0]))
        if pic_xmp.get(XMPINFO[0])
        else None)
    flight_yaw = (
        float(pic_xmp.get(XMPINFO[1]))
        if pic_xmp.get(XMPINFO[1])
        else None)

    longitude = PicOperator.convert_exif_longlat(pic_exif.get("Exif.GPSInfo.GPSLongitude"))
    long_ref = pic_exif.get("Exif.GPSInfo.GPSLongitudeRef")
    if longitude and long_ref != "E":
        longitude = longitude * (-1)

    latitude = PicOperator.convert_exif_longlat(pic_exif.get("Exif.GPSInfo.GPSLatitude"))
    lat_ref = pic_exif.get("Exif.GPSInfo.GPSLatitudeRef")
    if latitude and lat_ref != "N":
        latitude = latitude * (-1)

    altitude = PicOperator.convert_exif_longlat(pic_exif.get("Exif.GPSInfo.GPSAltitude"))
    focal_length = PicOperator.convert_exif_longlat(pic_exif.get("Exif.Photo.FocalLength"))

    _w = pic_exif.get("Exif.Photo.PixelXDimension") or pic_exif.get("Exif.Image.ImageWidth")
    width = int(_w) if _w else None

    _l = pic_exif.get("Exif.Photo.PixelYDimension") or pic_exif.get("Exif.Image.ImageLength")
    length = int(_l) if _l else None

    datetime_original = PicOperator.time_format(pic_exif.get("Exif.Photo.DateTimeOriginal"))


    return {
        "path": path,
        "name": name,
        "make": make,
        "model": model,
        "width": width,
        "length": length,
        "longitude": longitude,
        "latitude": latitude,
        "altitude": altitude,
        "focal_length": focal_length,
        "gimbal_pitch": gimbal_pitch,
        "flight_yaw": flight_yaw,
        "datetime_original": datetime_original
    }
