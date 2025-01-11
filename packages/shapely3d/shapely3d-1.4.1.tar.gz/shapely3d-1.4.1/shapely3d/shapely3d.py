# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 下午4:19
# @Author  : hhacai
# @File    : shapely3d.py
# @Software: PyCharm

import copy
from abc import ABC, abstractmethod
from shapely.wkt import loads
from shapely.ops import unary_union, substring, nearest_points
from shapely.affinity import rotate, scale
from shapely.geometry.base import BaseGeometry
from shapely.geometry import Point, LineString, Polygon, MultiPolygon, MultiPoint, LinearRing, \
    MultiLineString, GeometryCollection
from shapely.geometry.base import CAP_STYLE, JOIN_STYLE
import numpy as np
import numba

DEFAULT_Z = 0
GEOMTYPE_2D = '2D'
GEOMTYPE_3D = '3D'

PRECISION = 0.001


class BaseGeometry3D(BaseGeometry, ABC):

    @property
    @abstractmethod
    def avg_z(self):
        pass

    @property
    @abstractmethod
    def priority(self):
        pass

    @property
    @abstractmethod
    def get_hash_tree(self):
        pass

    @property
    def geom_2d(self):
        return ops3D.trans_3d_2d(self)

    @abstractmethod
    def reset_z(self, z):
        pass

    @property
    def is_valid(self):
        if self.geom_2d.is_valid and self.geometryType() in ['Point3D', 'MultiPoint3D', 'LineString3D',
                                                             'MultiLineString3D', 'Polygon3D', 'MultiPolygon3D']:
            return True
        else:
            return False

    @property
    def centroid(self):
        center_point = super().centroid
        center_point_3d = Point3D(center_point)
        center_point_3d.reset_z(self.avg_z)
        return center_point_3d

    @property
    def convex_hull(self):
        convex_geom = super().convex_hull
        if convex_geom.geometryType() == 'Point':
            convex_geom_3d = Point3D(convex_geom)
        elif convex_geom.geometryType() == 'LineString':
            convex_geom_3d = LineString3D(convex_geom)
        else:
            convex_geom_3d = Polygon3D(convex_geom)
        convex_geom_3d.reset_z(self.avg_z)
        return convex_geom_3d

    @staticmethod
    def get_nearest_z(coords, p):
        xy_coords = coords[:, :2]
        z_coords = coords[:, 2]
        p_array = np.array(p)
        distance = np.linalg.norm(xy_coords - p_array, axis=1) + 1E-6
        weight = 1.0 / distance
        norm_weight = weight / weight.sum()
        avg_z = (z_coords * norm_weight).sum()
        return avg_z
        # if np.min(distance) > 20:
        #     return np.mean(coords, axis=0)[2]
        # else:
        #     min_index = np.argmin(distance)
        #     return coords[min_index][2]
        # _, index = date_tree.query(p, k=1, distance_upper_bound=20)
        # if index >= len(date_tree.data):
        #     return np.mean(list(hash_dict.values()))
        # else:
        #     nearest_p = date_tree.data[index]
        #     z = hash_dict[tuple(nearest_p.tolist())]
        #     return z

    def simplify(self, tolerance):
        if self.is_empty:
            return self
        else:
            geom_2d = super().simplify(tolerance)
            geom_3d = ops3D.trans_2d_3d(geom_2d)
            return geom_3d

    def buffer(self, distance, resolution=16, quadsegs=None, cap_style=CAP_STYLE.round, join_style=JOIN_STYLE.round,
               mitre_limit=5.0, single_sided=False):
        this_z = self.avg_z
        buffer_geom = self.geom_2d.buffer(distance, resolution, quadsegs, cap_style, join_style, mitre_limit,
                                          single_sided)
        buffer_geom_3d = ops3D.trans_2d_3d(buffer_geom, this_z)
        return buffer_geom_3d

    def union(self, other, simple_union=False):
        if self.is_empty:
            return other
        elif other.is_empty:
            return self
        elif simple_union:
            this_z = self.avg_z
            union_geom = self.geom_2d.union(other.geom_2d)
            if not union_geom.is_valid:
                union_geom = union_geom.buffer(0)
            union_geom_3d = ops3D.trans_2d_3d(union_geom, this_z)
            return union_geom_3d
        else:
            self_geoms = []
            self_single_geomtype = ''
            self_single_priority = 1
            if hasattr(self, 'geoms'):
                for geom in self.geoms_3d:
                    self_geoms.append(geom)
                    self_single_geomtype = geom.geometryType()
                    self_single_priority = geom.priority
            else:
                self_geoms.append(self)
                self_single_geomtype = self.geometryType()
                self_single_priority = self.priority
            other_geoms = []
            other_single_geomtype = ''
            other_single_priority = 1
            if hasattr(other, 'geoms'):
                for geom in other.geoms_3d:
                    other_geoms.append(geom)
                    other_single_geomtype = geom.geometryType()
                    other_single_priority = geom.priority
            else:
                other_geoms.append(other)
                other_single_geomtype = other.geometryType()
                other_single_priority = other.priority
            if self_single_geomtype != other_single_geomtype:
                union_geoms = self_geoms if self_single_priority > other_single_priority else other_geoms
                single_geomtype = self_single_geomtype if self_single_priority > other_single_priority else other_single_geomtype
            else:
                union_geoms = self_geoms + other_geoms
                single_geomtype = self_single_geomtype
            if single_geomtype == 'Point3D':
                return MultiPoint3D(union_geoms)
            elif single_geomtype == 'LineString3D':
                return MultiLineString3D(union_geoms)
            else:
                return MultiPolygon3D(union_geoms)

    def intersects(self, other, z_tolerance=3, raw_intersects=False, simple_intersects=False):
        if self.is_empty or other.is_empty:
            return False
        elif z_tolerance is None or raw_intersects:
            return super().intersects(other)
        elif simple_intersects:
            if z_tolerance is not None and self.distance_z(other) > z_tolerance:
                return False
            else:
                return super().intersects(other)
        else:
            self_geoms = []
            if hasattr(self, 'geoms'):
                for geom in self.geoms_3d:
                    self_geoms.append(geom)
            else:
                self_geoms.append(self)
            other_geoms = []
            if hasattr(other, 'geoms'):
                for geom in other.geoms_3d:
                    other_geoms.append(geom)
            else:
                other_geoms.append(other)
            is_intersects = False
            for self_geom in self_geoms:
                for other_geom in other_geoms:
                    if self_geom.intersects(other_geom, raw_intersects=True):
                        self_coords = self_geom.get_hash_tree
                        other_coords = other_geom.get_hash_tree
                        intersection_geom_2d = self_geom.intersection(other_geom, raw_intersects=True)
                        intersection_geom_3d = ops3D.trans_2d_3d(intersection_geom_2d)
                        if intersection_geom_3d.is_empty:
                            continue
                        intersection_geom_type = intersection_geom_3d.geometryType()
                        self_z_list = []
                        other_z_list = []
                        if intersection_geom_type == 'Point3D':
                            inter_p = (intersection_geom_3d.coords[0][0], intersection_geom_3d.coords[0][1])
                            self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                            other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'MultiPoint3D':
                            for sub_geom in intersection_geom_3d:
                                inter_p = (sub_geom.coords[0][0], sub_geom.coords[0][1])
                                self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'LineString3D':
                            if not intersection_geom_3d.is_valid:
                                print('intersects valid warning {}'.format(intersection_geom_3d.wkt))
                                continue
                            # 找相交点
                            for p in intersection_geom_3d.coords:
                                inter_p = (p[0], p[1])
                                self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'MultiLineString3D':
                            # 找相交点
                            for sub_geom in intersection_geom_3d:
                                if not sub_geom.is_valid:
                                    print('intersects valid warning {}'.format(sub_geom.wkt))
                                    continue
                                for p in sub_geom.coords:
                                    inter_p = (p[0], p[1])
                                    self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                    other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'Polygon3D':
                            if not intersection_geom_3d.is_valid:
                                print('intersects valid warning {}'.format(intersection_geom_3d.wkt))
                                continue
                            for p in intersection_geom_3d.boundary.coords:
                                inter_p = (p[0], p[1])
                                self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        elif intersection_geom_type == 'MultiPolygon3D':
                            self_z_list = []
                            other_z_list = []
                            for sub_geom in intersection_geom_3d:
                                if not sub_geom.is_valid:
                                    print('intersects valid warning {}'.format(sub_geom.wkt))
                                    continue
                                for p in sub_geom.boundary.coords:
                                    inter_p = (p[0], p[1])
                                    self_z_list.append(self.get_nearest_z(self_coords, inter_p))
                                    other_z_list.append(self.get_nearest_z(other_coords, inter_p))
                        else:
                            print("intersects type warning {}".format(intersection_geom_3d))
                            continue
                        self_z = sum(self_z_list) / len(self_z_list)
                        other_z = sum(other_z_list) / len(other_z_list)
                        if abs(self_z - other_z) < z_tolerance:
                            is_intersects = True
                            break
            return is_intersects

    def intersection(self, other, z_tolerance=3, raw_intersects=False, simple_intersection=False):
        if self.is_empty or other.is_empty:
            return Point3D()
        elif raw_intersects:
            # return super().intersection(other)
            return self.intersection_np(other)
        elif simple_intersection or z_tolerance is None:
            if z_tolerance is not None and self.distance_z(other) > z_tolerance:
                return Point3D()
            else:
                this_z = self.avg_z
                intersection_geom = self.intersection_np(other)
                intersection_geom_3d = ops3D.trans_2d_3d(intersection_geom, this_z)
                return intersection_geom_3d
        else:
            self_geoms = []
            if hasattr(self, 'geoms'):
                for geom in self.geoms_3d:
                    self_geoms.append(geom)
            else:
                self_geoms.append(self)
            other_geoms = []
            if hasattr(other, 'geoms'):
                for geom in other.geoms_3d:
                    other_geoms.append(geom)
            else:
                other_geoms.append(other)
            intersection_geoms = []
            for self_geom in self_geoms:
                for other_geom in other_geoms:
                    intersection_geom_2d = self_geom.intersection(other_geom, raw_intersects=True)
                    intersection_geom_3d = ops3D.trans_2d_3d(intersection_geom_2d)
                    if intersection_geom_3d.is_empty:
                        continue
                    intersection_geom_type = intersection_geom_3d.geometryType()
                    dst_intersection_geom = []
                    self_coords = self_geom.get_hash_tree
                    other_coords = other_geom.get_hash_tree
                    if intersection_geom_type == 'Point3D':
                        for p in intersection_geom_3d.coords:
                            inter_p = (p[0], p[1])
                            self_z = self.get_nearest_z(self_coords, inter_p)
                            other_z = self.get_nearest_z(other_coords, inter_p)
                            if abs(self_z - other_z) > z_tolerance:
                                break
                            else:
                                dst_intersection_geom.append([p[0], p[1], self_z])
                        if len(dst_intersection_geom) == 0:
                            intersection_geoms.append(Point3D())
                        else:
                            intersection_geoms.append(Point3D(dst_intersection_geom[0]))
                    elif intersection_geom_type == 'MultiPoint3D':
                        for sub_geom in intersection_geom_3d:
                            tmp = []
                            delta_z_exam = True
                            for p in sub_geom.coords:
                                inter_p = (p[0], p[1])
                                self_z = self.get_nearest_z(self_coords, inter_p)
                                other_z = self.get_nearest_z(other_coords, inter_p)
                                if abs(self_z - other_z) > z_tolerance:
                                    delta_z_exam = False
                                    break
                                else:
                                    tmp.append([p[0], p[1], self_z])
                            if not delta_z_exam:
                                dst_intersection_geom.append(Point3D())
                            else:
                                dst_intersection_geom.append(Point3D(tmp[0]))
                        intersection_geoms.extend(dst_intersection_geom)
                    elif intersection_geom_type == 'LineString3D':
                        if not intersection_geom_3d.is_valid:
                            print('intersects error {}'.format(intersection_geom_3d.wkt))
                            continue
                        delta_z_exam = True
                        for p in intersection_geom_3d.coords:
                            inter_p = (p[0], p[1])
                            self_z = self.get_nearest_z(self_coords, inter_p)
                            other_z = self.get_nearest_z(other_coords, inter_p)
                            if abs(self_z - other_z) > z_tolerance:
                                delta_z_exam = False
                                break
                            else:
                                dst_intersection_geom.append([p[0], p[1], self_z])
                        if not delta_z_exam:
                            intersection_geoms.append(LineString3D())
                        else:
                            intersection_geoms.append(LineString3D(dst_intersection_geom))
                    elif intersection_geom_type == 'MultiLineString3D':
                        for sub_geom in intersection_geom_3d:
                            if not sub_geom.is_valid:
                                print('intersects error {}'.format(sub_geom.wkt))
                                continue
                            tmp = []
                            delta_z_exam = True
                            for p in sub_geom.coords:
                                inter_p = (p[0], p[1])
                                self_z = self.get_nearest_z(self_coords, inter_p)
                                other_z = self.get_nearest_z(other_coords, inter_p)
                                if abs(self_z - other_z) > z_tolerance:
                                    delta_z_exam = False
                                    break
                                else:
                                    tmp.append([p[0], p[1], self_z])
                            if not delta_z_exam:
                                intersection_geoms.append(LineString3D())
                            else:
                                dst_intersection_geom.append(LineString3D(tmp))
                        intersection_geoms.extend(dst_intersection_geom)
                    elif intersection_geom_type == 'Polygon3D':
                        if not intersection_geom_3d.is_valid:
                            print('intersects error {}'.format(intersection_geom_3d.wkt))
                            continue
                        delta_z_exam = True
                        for p in intersection_geom_3d.boundary.coords:
                            inter_p = (p[0], p[1])
                            self_z = self.get_nearest_z(self_coords, inter_p)
                            other_z = self.get_nearest_z(other_coords, inter_p)
                            if abs(self_z - other_z) > z_tolerance:
                                delta_z_exam = False
                                break
                            else:
                                dst_intersection_geom.append([p[0], p[1], self_z])
                        if not delta_z_exam:
                            intersection_geoms.append(Polygon3D())
                        else:
                            intersection_geoms.append(Polygon3D(dst_intersection_geom))
                    elif intersection_geom_type == 'MultiPolygon3D':
                        for sub_geom in intersection_geom_3d:
                            if not sub_geom.is_valid:
                                print('intersects error {}'.format(sub_geom.wkt))
                                continue
                            tmp = []
                            delta_z_exam = True
                            for p in sub_geom.boundary.coords:
                                inter_p = (p[0], p[1])
                                self_z = self.get_nearest_z(self_coords, inter_p)
                                other_z = self.get_nearest_z(other_coords, inter_p)
                                if abs(self_z - other_z) > z_tolerance:
                                    delta_z_exam = False
                                    break
                                else:
                                    tmp.append([p[0], p[1], self_z])
                            if not delta_z_exam:
                                intersection_geoms.append(Polygon3D())
                            else:
                                dst_intersection_geom.append(Polygon3D(tmp))
                        intersection_geoms.extend(dst_intersection_geom)
                    elif intersection_geom_type == 'GeometryCollection3D':
                        print("intersection warning {}".format(intersection_geom_3d))
                        continue
                        # for sub_geom in intersection_geom_3d:
                        #     tmp = []
                        #     for p in sub_geom.coords:
                        #         inter_p = (p[0], p[1])
                        #         self_z = self.get_nearest_z(self_data_tree, self_hash_dict,self_coords,  inter_p)
                        #         tmp.append([p[0], p[1], self_z])
                        #     if sub_geom.geom_type == 'LineString':
                        #         dst_intersection_geom.append(LineString3D(tmp))
                        #     elif sub_geom.geom_type == 'Point':
                        #         dst_intersection_geom.append(Point3D(tmp[0]))
                        # return GeometryCollection3D(dst_intersection_geom)
                    else:
                        print("intersection warning {}".format(intersection_geom_3d))
                        continue
            result = ops3D.unary_union(intersection_geoms)
            return result

    def difference(self, other, z_tolerance=3):
        if self.is_empty or other.is_empty:
            return self
        else:
            self_geoms = []
            if hasattr(self, 'geoms'):
                for geom in self.geoms_3d:
                    self_geoms.append(geom)
            else:
                self_geoms.append(self)
            other_geoms = []
            if hasattr(other, 'geoms'):
                for geom in other.geoms_3d:
                    other_geoms.append(geom)
            else:
                other_geoms.append(other)
            diff_geoms = []
            for self_geom in self_geoms:
                diff_part_geoms = []
                for other_geom in other_geoms:
                    if self_geom.distance_z(other_geom) < z_tolerance:
                        self_geom_2d = ops3D.trans_3d_2d(self_geom, retain_z=True)
                        other_geom_2d = ops3D.trans_3d_2d(other_geom, retain_z=True)
                        diff_geom_2d = self_geom_2d.difference(other_geom_2d)
                        diff_geom_3d = ops3D.trans_2d_3d(diff_geom_2d)
                        diff_part_geoms.append(diff_geom_3d)
                    else:
                        diff_part_geoms.append(self_geom)
                diff_geoms.append(ops3D.unary_intersection(diff_part_geoms))
            return ops3D.unary_intersection(diff_geoms)

    def intersection_np(self, other):
        if self.geometryType() == "LineString3D" and other.geometryType() == "LineString3D":
            a_coords = np.array(self.coords)
            a_lines = []
            for i in range(a_coords.shape[0]):
                if i == 0:
                    continue
                a_lines.append([a_coords[i], a_coords[i - 1]])
            b_coords = np.array(other.coords)
            b_lines = []
            for i in range(b_coords.shape[0]):
                if i == 0:
                    continue
                b_lines.append([b_coords[i], b_coords[i - 1]])

            intersect_lines = []
            intersect_coords = []
            for a_line in a_lines:
                for b_line in b_lines:
                    a1, a2, b1, b2 = a_line[0][:2], a_line[1][:2], b_line[0][:2], b_line[1][:2]
                    a_minx, a_maxx = min(a1[0], a2[0]), max(a1[0], a2[0])
                    a_miny, a_maxy = min(a1[1], a2[1]), max(a1[1], a2[1])
                    b_minx, b_maxx = min(b1[0], b2[0]), max(b1[0], b2[0])
                    b_miny, b_maxy = min(b1[1], b2[1]), max(b1[1], b2[1])
                    avg_z = (a_line[0][2] + a_line[1][2] + b_line[0][2] + b_line[1][2]) / 4.0

                    da = a2 - a1
                    db = b2 - b1
                    dp = a1 - b1

                    dap = np.empty_like(da)
                    dap[0] = -da[1]
                    dap[1] = da[0]

                    denom = np.dot(dap, db)
                    num = np.dot(dap, dp)

                    if abs(denom) < 1e-6:
                        a_line_geom = LineString3D([a1, a2])
                        b_line_geom = LineString3D([b1, b2])
                        if a_line_geom.distance(b_line_geom) < 1e-6:
                            a_line_proj_1 = a_line_geom.interpolate(a_line_geom.project(Point3D(b1)))
                            a_line_proj_2 = a_line_geom.interpolate(a_line_geom.project(Point3D(b2)))
                            intersect_lines.append(LineString3D([a_line_proj_1, a_line_proj_2]))
                    else:
                        result = (num / denom.astype(float)) * db + b1
                        result_x, result_y = result
                        if a_minx <= result_x <= a_maxx and b_minx <= result_x <= b_maxx and a_miny <= result_y <= a_maxy and b_miny <= result_y <= b_maxy:
                            intersect_coords.append([result_x, result_y, avg_z])
                        else:
                            pass

            if len(intersect_lines) > 0:
                if len(intersect_lines) == 1:
                    return intersect_lines[0]
                else:
                    return MultiLineString3D(intersect_lines)
            elif len(intersect_coords) == 0:
                return Point3D()
            elif len(intersect_coords) == 1:
                return Point3D(intersect_coords[0])
            else:
                return MultiPoint3D(intersect_coords)
        else:
            return super().intersection(other)

    def distance(self, other, z_tolerance=None):
        if self.is_empty or other.is_empty:
            return 0
        elif z_tolerance is None:
            if self.geometryType() == "Point3D" and other.geometryType() == "Point3D":
                return np.linalg.norm(np.array(self.coords[0])[:2] - np.array(other.coords[0])[:2])
            else:
                return super().distance(other)
        else:
            distance_2d = super().distance(other)
            z_distance = self.distance_z(other)
            if z_distance < z_tolerance:
                return distance_2d
            else:
                return distance_2d + z_distance

    def distance_z(self, other):
        if self.is_empty or other.is_empty:
            return 0
        elif ops3D.judge_2d_3d(self) == GEOMTYPE_2D or ops3D.judge_2d_3d(other) == GEOMTYPE_2D:
            return 0
        else:
            return abs(self.avg_z - other.avg_z)


class Point3D(BaseGeometry3D, Point):
    def __init__(self, *args):
        Point.__init__(self, *args)
        self.empty_flag = False
        if len(args) == 0:
            self.empty_flag = True
            return
        if not self.has_z:
            Point.__init__(self, [self.x, self.y, DEFAULT_Z])

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            return self.z

    @property
    def priority(self):
        return 1

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # for p in self.coords:
        #     hash_dict[(p[0], p[1])] = p[2]
        #     tree_dataset.append([p[0], p[1]])
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(self.coords)
        return np.array(self.coords)

    # @property
    # def is_empty(self):
    #     return self.empty_flag

    def geometryType(self):
        return "Point3D"

    def reset_z(self, z):
        Point3D.__init__(self, [self.x, self.y, z])


class LineString3D(BaseGeometry3D, LineString):
    def __init__(self, *args):
        LineString.__init__(self, *args)
        self.empty_flag = False
        if len(args) == 0:
            self.empty_flag = True
            return
        if not self.has_z:
            self.reset_z(DEFAULT_Z)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            coords = np.array(list(self.coords))
            return float(np.mean(coords[:, 2]))

    @property
    def priority(self):
        return 2

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # for p in self.coords:
        #     hash_dict[(p[0], p[1])] = p[2]
        #     tree_dataset.append([p[0], p[1]])
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(self.coords)
        return np.array(self.coords)

    def geometryType(self):
        return "LineString3D"

    def reset_z(self, z):
        bound_coords_3d = []
        bound_coords = list(self.coords)
        for bound_coord in bound_coords:
            bound_coords_3d.append([bound_coord[0], bound_coord[1], z])
        LineString3D.__init__(self, bound_coords_3d)

    def interpolate(self, distance, normalized=False):
        if self.is_empty:
            return self
        else:
            this_z = self.avg_z
            line_2d = ops3D.trans_3d_2d(self)
            inter_point_2d = line_2d.interpolate(distance, normalized)
            inter_point_3d = ops3D.trans_2d_3d(inter_point_2d)
            inter_point_3d.reset_z(this_z)
            return inter_point_3d

    def project(self, other, normalized=False):
        if self.is_empty or other.is_empty:
            return 0
        else:
            line_2d = ops3D.trans_3d_2d(self)
            other_2d = ops3D.trans_3d_2d(other)
            project_distance = line_2d.project(other_2d, normalized)
            return project_distance


class Polygon3D(BaseGeometry3D, Polygon):
    def __init__(self, *args):
        Polygon.__init__(self, *args)
        self.empty_flag = False
        if len(args) == 0:
            self.empty_flag = True
            return
        if not self.has_z:
            self.reset_z(DEFAULT_Z)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            coords = np.array(list(self.boundary.coords))
            return float(np.mean(coords[:, 2]))

    @property
    def priority(self):
        return 3

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # coords = []
        # for p in self.boundary.coords:
        #     hash_dict[(p[0], p[1])] = p[2]
        #     tree_dataset.append([p[0], p[1]])
        #     coords.append(p)
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(coords)
        coords = []
        for p in self.boundary.coords:
            coords.append(p)
        return np.array(coords)

    @property
    def boundary(self):
        boundary_line = super().boundary
        boundary_line = ops3D.trans_2d_3d(boundary_line)
        if boundary_line.geometryType() == 'MultiLineString3D':
            max_length = None
            exterior_line = boundary_line.geoms_3d[0]
            for line in boundary_line.geoms_3d:
                if max_length is None or line.length > max_length:
                    max_length = line.length
                    exterior_line = line
            return exterior_line
        else:
            return boundary_line

    def geometryType(self):
        return "Polygon3D"

    def reset_z(self, z):
        bound_coords_3d = []
        bound_coords = list(self.boundary.coords)
        for bound_coord in bound_coords:
            bound_coords_3d.append([bound_coord[0], bound_coord[1], z])
        Polygon3D.__init__(self, bound_coords_3d)


class MultiPoint3D(BaseGeometry3D, MultiPoint):
    def __init__(self, points=None):
        MultiPoint.__init__(self, points)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            list_z = []
            for point3d in self.geoms_3d:
                list_z.append(point3d.z)
            return float(np.mean(list_z))

    @property
    def priority(self):
        return 4

    @property
    def geoms_3d(self):
        geoms = []
        for geom in self.geoms:
            geoms.append(Point3D(geom))
        return geoms

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # coords = []
        # for sub_geom in self:
        #     for p in sub_geom.coords:
        #         hash_dict[(p[0], p[1])] = p[2]
        #         tree_dataset.append([p[0], p[1]])
        #         coords.append(p)
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(coords)
        coords = []
        for sub_geom in self:
            for p in sub_geom.coords:
                coords.append(p)
        return np.array(coords)

    def geometryType(self):
        return "MultiPoint3D"

    def reset_z(self, z):
        points = []
        for geom in self.geoms_3d:
            geom.reset_z(z)
            points.append(geom)
        self.__init__(points)


class MultiLineString3D(BaseGeometry3D, MultiLineString):
    def __init__(self, lines=None):
        MultiLineString.__init__(self, lines)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            list_z = []
            for line3d in self.geoms_3d:
                list_z.append(line3d.avg_z)
            return float(np.mean(list_z))

    @property
    def priority(self):
        return 5

    @property
    def geoms_3d(self):
        geoms = []
        for geom in self.geoms:
            geoms.append(LineString3D(geom))
        return geoms

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # coords = []
        # for sub_geom in self:
        #     for p in sub_geom.coords:
        #         hash_dict[(p[0], p[1])] = p[2]
        #         tree_dataset.append([p[0], p[1]])
        #         coords.append(p)
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(coords)
        coords = []
        for sub_geom in self:
            for p in sub_geom.coords:
                coords.append(p)
        return np.array(coords)

    def geometryType(self):
        return "MultiLineString3D"

    def reset_z(self, z):
        lines = []
        for geom in self.geoms_3d:
            geom.reset_z(z)
            lines.append(geom)
        self.__init__(lines)


class MultiPolygon3D(BaseGeometry3D, MultiPolygon):
    def __init__(self, polygons=None):
        MultiPolygon.__init__(self, polygons)

    @property
    def avg_z(self):
        if self.is_empty:
            return 0
        else:
            list_z = []
            for polygon3d in self.geoms_3d:
                list_z.append(polygon3d.avg_z)
            return float(np.mean(list_z))

    @property
    def priority(self):
        return 6

    @property
    def geoms_3d(self):
        geoms = []
        for geom in self.geoms:
            geoms.append(Polygon3D(geom))
        return geoms

    @property
    def get_hash_tree(self):
        # hash_dict = {}
        # tree_dataset = []
        # coords = []
        # for sub_geom in self:
        #     for p in sub_geom.boundary.coords:
        #         hash_dict[(p[0], p[1])] = p[2]
        #         tree_dataset.append([p[0], p[1]])
        #         coords.append(p)
        # data_tree = spatial.KDTree(tree_dataset)
        # return hash_dict, data_tree, np.array(coords)
        coords = []
        for sub_geom in self:
            for p in sub_geom.boundary.coords:
                coords.append(p)
        return np.array(coords)

    def geometryType(self):
        return "MultiPolygon3D"

    def reset_z(self, z):
        polygons = []
        for geom in self.geoms_3d:
            geom.reset_z(z)
            polygons.append(geom)
        self.__init__(polygons)


class wkt3D:
    @staticmethod
    def loads(data: str, z=None):
        geometry = loads(data)
        if geometry.geometryType() == 'Point':
            geometry_3d = Point3D(geometry)
            if z is not None:
                geometry_3d.reset_z(z)
            return geometry_3d
        elif geometry.geometryType() == 'LineString':
            geometry_3d = LineString3D(geometry)
            if z is not None:
                geometry_3d.reset_z(z)
            return geometry_3d
        elif geometry.geometryType() == 'Polygon':
            geometry_3d = Polygon3D(geometry)
            if z is not None:
                geometry_3d.reset_z(z)
            return geometry_3d
        else:
            print("wkt format error: {}".format(data))
            return Point3D()


class ops3D:
    @staticmethod
    def trans_3d_2d(geom, retain_z=False):
        if ops3D.judge_2d_3d(geom) == GEOMTYPE_2D:
            return geom
        elif geom.geometryType() == 'Point3D':
            if geom.is_empty:
                geom_2d = Point()
            else:
                geom_2d = Point(geom.x, geom.y, geom.z) if retain_z else Point(geom.x, geom.y)
        elif geom.geometryType() == 'LineString3D':
            if geom.is_empty:
                geom_2d = LineString()
            else:
                geom_2d = LineString(np.array(list(geom.coords))) if retain_z else LineString(
                    np.array(list(geom.coords))[:, :2])
        elif geom.geometryType() == 'Polygon3D':
            if geom.is_empty:
                geom_2d = Polygon()
            else:
                geom_2d = Polygon(np.array(list(geom.boundary.coords))) if retain_z else Polygon(
                    np.array(list(geom.boundary.coords))[:, :2])
        elif geom.geometryType() == 'MultiPoint3D':
            geoms = []
            for geom_ in geom.geoms_3d:
                geoms.append(ops3D.trans_3d_2d(geom_, retain_z))
            geom_2d = MultiPoint(geoms)
        elif geom.geometryType() == 'MultiLineString3D':
            geoms = []
            for geom_ in geom.geoms_3d:
                geoms.append(ops3D.trans_3d_2d(geom_, retain_z))
            geom_2d = MultiLineString(geoms)
        elif geom.geometryType() == 'MultiPolygon3D':
            geoms = []
            for geom_ in geom.geoms_3d:
                geoms.append(ops3D.trans_3d_2d(geom_, retain_z))
            geom_2d = MultiPolygon(geoms)
        else:
            print("trans_3d_2d format error: {}".format(geom.wkt))
            return Point()
        return geom_2d

    @staticmethod
    def trans_2d_3d(geom, z: float = None):
        if ops3D.judge_2d_3d(geom) == GEOMTYPE_3D:
            return geom
        elif geom.geometryType() == 'Point':
            if geom.is_empty:
                geom_3d = Point3D()
            else:
                geom_3d = Point3D(geom)
        elif geom.geometryType() == 'LineString':
            if geom.is_empty:
                geom_3d = LineString3D()
            else:
                geom_3d = LineString3D(geom)
        elif geom.geometryType() == 'Polygon':
            if geom.is_empty:
                geom_3d = Polygon3D()
            else:
                geom_3d = Polygon3D(geom)
        elif geom.geometryType() == 'MultiPoint':
            geoms = []
            for geom_ in geom.geoms:
                geoms.append(Point3D(geom_))
            geom_3d = MultiPoint3D(geoms)
        elif geom.geometryType() == 'MultiLineString':
            geoms = []
            for geom_ in geom.geoms:
                geoms.append(LineString3D(geom_))
            geom_3d = MultiLineString3D(geoms)
        elif geom.geometryType() == 'MultiPolygon':
            geoms = []
            for geom_ in geom.geoms:
                geoms.append(Polygon3D(geom_))
            geom_3d = MultiPolygon3D(geoms)
        else:
            print("trans_2d_3d format error: {}".format(geom.wkt))
            return Point3D()
        if z is not None and not geom_3d.is_empty:
            geom_3d.reset_z(z)
        return geom_3d

    @staticmethod
    def judge_2d_3d(geom):
        if '3D' in geom.geometryType():
            return GEOMTYPE_3D
        else:
            return GEOMTYPE_2D

    @staticmethod
    def unary_union(geoms: list, z: float = 0.0, simple_union=False):
        if len(geoms) == 0:
            return Polygon3D()
        elif simple_union:
            geoms_2d = []
            zs = []
            for geom in geoms:
                if ops3D.judge_2d_3d(geom) == GEOMTYPE_3D:
                    geoms_2d.append(ops3D.trans_3d_2d(geom))
                    zs.append(geom.avg_z)
                else:
                    geoms_2d.append(geom)
                    zs.append(z)
            union_geom = unary_union(geoms_2d)
            if union_geom.is_empty:
                return Polygon3D()
            else:
                avg_z = float(np.mean(zs))
                union_geom_3d = ops3D.trans_2d_3d(union_geom)
                union_geom_3d.reset_z(avg_z)
                return union_geom_3d
        else:
            union_geom = Polygon3D()
            for geom in geoms:
                union_geom = union_geom.union(geom)
            return union_geom

    @staticmethod
    def unary_intersection(geoms: list, z_tolerance=3):
        if len(geoms) == 0:
            return Polygon3D()
        elif len(geoms) == 1:
            return geoms[0]
        else:
            base_geom = geoms[0]
            for i, geom in enumerate(geoms):
                if i > 0:
                    base_geom = base_geom.intersection(geom, z_tolerance)
            return base_geom

    @staticmethod
    def nearest_points(geom1, geom2):
        if ops3D.judge_2d_3d(geom1) == GEOMTYPE_3D:
            geom1_z = geom1.avg_z
            geom1 = ops3D.trans_3d_2d(geom1)
        else:
            geom1_z = 0.0
        if ops3D.judge_2d_3d(geom2) == GEOMTYPE_3D:
            geom2_z = geom2.avg_z
            geom2 = ops3D.trans_3d_2d(geom2)
        else:
            geom2_z = 0.0
        point1, point2 = nearest_points(geom1, geom2)
        point1_3d = ops3D.trans_2d_3d(point1, geom1_z)
        point2_3d = ops3D.trans_2d_3d(point2, geom2_z)
        return point1_3d, point2_3d

    @staticmethod
    def substring(geom: LineString3D, start_dist, end_dist, normalized=False):
        if normalized is False:
            start_norm_distance = start_dist * geom.length
            end_norm_distance = end_dist * geom.length
        else:
            start_norm_distance = start_dist
            end_norm_distance = end_dist
        xy_line = LineString(np.array(list(geom.coords))[:, :2])
        yz_line = LineString(np.array(list(geom.coords))[:, 1:])
        sub_xy_line = substring(xy_line, start_norm_distance, end_norm_distance, normalized)
        sub_yz_line = substring(yz_line, start_norm_distance, end_norm_distance, normalized)
        sub_xy_coords = np.array(list(sub_xy_line.coords))[:, :2]
        sub_z_coords = np.array(list(sub_yz_line.coords))[:, -1]
        sub_z_coords = np.interp(np.linspace(0, sub_z_coords.shape[0] - 1, num=sub_xy_coords.shape[0], endpoint=True),
                                 np.linspace(0, sub_z_coords.shape[0] - 1, num=sub_z_coords.shape[0], endpoint=True),
                                 sub_z_coords)
        sub_line = LineString3D(np.append(sub_xy_coords, sub_z_coords[:, np.newaxis], axis=1))
        return sub_line

    @staticmethod
    def interpolate(geom: LineString3D, interp_dist, normalized=False):
        if not normalized:
            interp_norm = interp_dist / geom.length
        else:
            interp_norm = interp_dist
        start_coord = np.array(geom.coords[0])
        end_coord = np.array(geom.coords[-1])
        interp_x = start_coord[0] + (end_coord[0] - start_coord[0]) * interp_norm
        interp_y = start_coord[1] + (end_coord[1] - start_coord[1]) * interp_norm
        interp_z = start_coord[2] + (end_coord[2] - start_coord[2]) * interp_norm
        return Point3D(interp_x, interp_y, interp_z)


class ops3D_smp:
    @staticmethod
    def geom_to_array(geom):
        if geom.geometryType() == 'Point3D':
            return np.array(geom.coords)[0]
        else:
            return np.array(geom.coords)

    @staticmethod
    @numba.jit(nopython=True)
    def distance_point_point(point_1, point_2):
        vector = point_1 - point_2
        dis = np.sqrt(vector[0] ** 2 + vector[1] ** 2)
        return dis

    @staticmethod
    @numba.jit(nopython=True)
    def interpolate(line, interp_dist, normalized=False):
        start_coord, end_coord = line[0], line[-1]
        line_vector = end_coord - start_coord
        line_length = np.sqrt(line_vector[0] ** 2 + line_vector[1] ** 2)
        if not normalized:
            interp_norm = interp_dist / line_length
        else:
            interp_norm = interp_dist
        new_point = start_coord + line_vector * interp_norm
        return new_point

    @staticmethod
    @numba.jit(nopython=True)
    def points_line_distance(points, line):
        points = points[:, :2]
        line = line[:, :2]
        start, end = line[0], line[-1]
        vector_base = end - start
        module_base = np.sqrt(vector_base[0] ** 2 + vector_base[1] ** 2)
        vector_new = points - start
        cross = np.dot(vector_base, vector_new.T)
        # 垂足在线段内的位置
        t = cross / module_base ** 2
        # 垂足到点的距离
        vectors_result = start + (vector_base.reshape(-1, 2).T * t).T - points
        distance = np.sqrt(vectors_result[:, 0] ** 2 + vectors_result[:, 1] ** 2)
        # distance = np.linalg.norm(start + (vector_base.reshape(-1, 2).T * t).T - points, axis=1)
        # 修正线段外的垂足距离
        vectors_start_outlier = points[np.logical_or(t < 0, t > 1)] - start
        vectors_end_outlier = points[np.logical_or(t < 0, t > 1)] - end
        start_outlier_distance = np.sqrt(vectors_start_outlier[:, 0] ** 2 + vectors_start_outlier[:, 1] ** 2)
        end_outlier_distance = np.sqrt(vectors_end_outlier[:, 0] ** 2 + vectors_end_outlier[:, 1] ** 2)
        start_outlier_distance[end_outlier_distance < start_outlier_distance] = end_outlier_distance[
            end_outlier_distance < start_outlier_distance]
        distance[np.logical_or(t < 0, t > 1)] = start_outlier_distance
        return distance

    @staticmethod
    def polygon_contains_point(polygon_coords, point):
        def isRayIntersectsSegment(poi, s_poi, e_poi):  # [x,y] [lng,lat]
            # 输入：判断点，边起点，边终点，都是[lng,lat]格式数组
            if s_poi[1] == e_poi[1]:  # 排除与射线平行、重合，线段首尾端点重合的情况
                return False
            if s_poi[1] > poi[1] and e_poi[1] > poi[1]:  # 线段在射线上边
                return False
            if s_poi[1] < poi[1] and e_poi[1] < poi[1]:  # 线段在射线下边
                return False
            if s_poi[1] == poi[1] and e_poi[1] > poi[1]:  # 交点为下端点，对应spoint
                return False
            if e_poi[1] == poi[1] and s_poi[1] > poi[1]:  # 交点为下端点，对应epoint
                return False

            xseg = e_poi[0] - (e_poi[0] - s_poi[0]) * (e_poi[1] - poi[1]) / (e_poi[1] - s_poi[1])  # 求交
            if xseg < poi[0]:  # 交点在射线起点的左侧
                return False
            return True  # 排除上述情况之后

        sinsc = 0  # 交点个数
        for i in range(len(polygon_coords) - 1):  # 循环每条边的曲线->each polygon 是二维数组[[x1,y1],…[xn,yn]]
            s_poi = polygon_coords[i]
            e_poi = polygon_coords[i + 1]
            if isRayIntersectsSegment(point, s_poi, e_poi):
                sinsc += 1  # 有交点就加1
        return True if sinsc % 2 == 1 else False


class affinity3D:
    @staticmethod
    def rotate(geom, angle, origin='center', use_radians=False):
        geom_2d = ops3D.trans_3d_2d(geom, retain_z=True)
        if isinstance(origin, str):
            origin_2d = origin
        else:
            origin_2d = ops3D.trans_3d_2d(origin, retain_z=True)
        rot_geom_2d = rotate(geom_2d, angle, origin=origin_2d, use_radians=use_radians)
        rot_geom_3d = ops3D.trans_2d_3d(rot_geom_2d)
        return rot_geom_3d

    @staticmethod
    def scale(geom, xfact=1.0, yfact=1.0, zfact=1.0, origin='center'):
        geom_2d = ops3D.trans_3d_2d(geom, retain_z=True)
        if isinstance(origin, str):
            origin_2d = origin
        else:
            origin_2d = ops3D.trans_3d_2d(origin, retain_z=True)
        scale_geom_2d = scale(geom_2d, xfact=xfact, yfact=yfact, zfact=zfact, origin=origin_2d)
        scale_geom_3d = ops3D.trans_2d_3d(scale_geom_2d)
        return scale_geom_3d


if __name__ == '__main__':
    import time
    from shapely.wkt import loads, dumps

    start_time = time.perf_counter_ns()

    # p1 = Polygon3D([[0,0,0],[2,0,0],[2,2,0],[0,2,0]])
    # p2 = Polygon3D([[1,1,0],[3,1,0],[3,3,0],[1,3,0]])
    # p1.simplify(0.1)
    # m = MultiPolygon3D([p1, p2])
    # l = LineString3D([[-1, -1, 0], [4, 4, 0]])
    #
    # inter = m.intersection(l)
    #
    # diff = l.difference(m)

    l = loads('LINESTRING Z (-24.865510940551758 -108.04869842529297 -1.0543826818466187, -24.66522979736328 -106.58277893066406 -1.0543826818466187, -24.525543212890625 -105.1126937866211 -1.0543826818466187, -24.480897903442383 -104.42523956298828 -1.0543826818466187, -24.4478816986084 -103.38141632080078 -1.0543826818466187, -24.37455177307129 -102.19562530517578 -1.0601369142532349, -23.822471618652344 -95.288330078125 -1.1504853963851929, -23.543794631958008 -91.0727310180664 -1.1792351007461548, -23.29152488708496 -87.82382202148438 -1.1946642398834229, -23.051475524902344 -83.5208511352539 -1.2733641862869263, -22.009708404541016 -68.2905044555664 -1.578384518623352, -21.330963134765625 -59.1236572265625 -1.6633756160736084, -20.9156551361084 -53.247772216796875 -1.7181470394134521, -20.38943099975586 -46.52284622192383 -1.7869620323181152, -20.095666885375977 -42.41844177246094 -1.8086715936660767, -19.98692512512207 -40.580711364746094 -1.817394495010376, -19.714229583740234 -36.88304901123047 -1.8270272016525269, -19.310129165649414 -32.83588790893555 -1.843172550201416)')
    l_wkt = dumps(l, rounding_precision=3)
    l = loads(l_wkt)
    l = ops3D.trans_2d_3d(l)
    p = loads('MULTIPOLYGON Z (((-25.17000389099121 -107.48816680908203 -1.176424503326416, -24.750520706176758 -100.5003433227539 -1.0805699825286865, -23.93222427368164 -88.46794128417969 -1.2540700435638428, -23.1112060546875 -78.25184631347656 -1.395169973373413, -22.459091186523438 -69.16151428222656 -1.5537699460983276, -21.75568199157715 -59.35614013671875 -1.665369987487793, -21.074846267700195 -49.86541748046875 -1.7715699672698975, -20.345870971679688 -39.70363998413086 -1.820970058441162, -19.369956970214844 -30.792884826660156 -1.8586699962615967, -18.085742950439453 -24.48055648803711 -1.8883700370788574, -16.418201446533203 -19.51572608947754 -1.884469985961914, -13.028414726257324 -13.797011375427246 -1.8598699569702148, -6.637198448181152 -17.801366806030273 -1.8598699569702148, -9.596943855285645 -22.564157485961914 -1.884469985961914, -11.306183815002441 -26.579072952270508 -1.8883700370788574, -12.336660385131836 -32.00490951538086 -1.8586699962615967, -13.212553024291992 -40.22431182861328 -1.820970058441162, -13.977500915527344 -50.36618423461914 -1.7715699672698975, -14.8486909866333 -59.888206481933594 -1.665369987487793, -15.609148025512695 -69.65843963623047 -1.5537699460983276, -16.101255416870117 -78.66190338134766 -1.395169973373413, -16.728113174438477 -88.99103546142578 -1.2540700435638428, -17.549802780151367 -101.00991821289062 -1.0805699825286865, -18.07523536682129 -107.99024200439453 -1.176424503326416, -25.17000389099121 -107.48816680908203 -1.176424503326416)), ((-13.028414726257324 -13.797011375427246 -1.6007745365301769, -16.418201446533203 -19.51572608947754 -1.6007745365301769, -18.085742950439453 -24.48055648803711 -1.6007745365301769, -19.369956970214844 -30.792884826660156 -1.6007745365301769, -20.345870971679688 -39.70363998413086 -1.6007745365301769, -21.074846267700195 -49.86541748046875 -1.6007745365301769, -21.75568199157715 -59.35614013671875 -1.6007745365301769, -22.459091186523438 -69.16151428222656 -1.6007745365301769, -23.1112060546875 -78.25184631347656 -1.6007745365301769, -23.93222427368164 -88.46794128417969 -1.6007745365301769, -24.750520706176758 -100.5003433227539 -1.6007745365301769, -25.17000389099121 -107.48816680908203 -1.6007745365301769, -26.16820691030861 -107.42824409030501 -1.6007745365301769, -25.748723725494155 -100.44042060397689 -1.6007745365301769, -25.748216170908623 -100.43249231205053 -1.6007745365301769, -24.929919738413506 -88.40009027347631 -1.6007745365301769, -24.929010551989954 -88.38783438450018 -1.6007745365301769, -24.108335926202408 -78.17601481323237 -1.6007745365301769, -23.456527967799722 -69.08996103382223 -1.6007745365301769, -22.753118778131903 -59.28458696189517 -1.6007745365301769, -22.072283059825942 -49.79386438330378 -1.6007745365301769, -21.34330776290478 -39.63208687441092 -1.6007745365301769, -21.339926976738035 -39.594770067223386 -1.6007745365301769, -20.36401297527319 -30.684014909752687 -1.6007745365301769, -20.349883000033454 -30.593523405908964 -1.6007745365301769, -19.065668980258064 -24.281195067285918 -1.6007745365301769, -19.033702157034583 -24.162164681246278 -1.6007745365301769, -17.366160653128333 -19.197334282686707 -1.6007745365301769, -17.327353344576284 -19.099261413562925 -1.6007745365301769, -17.278432362242214 -19.0058214202908 -1.6007745365301769, -13.888645641966333 -13.287106706240506 -1.6007745365301769, -13.028414726257324 -13.797011375427246 -1.6007745365301769)), ((-18.07523536682129 -107.99024200439453 -1.6007745365301769, -17.549802780151367 -101.00991821289062 -1.6007745365301769, -16.728113174438477 -88.99103546142578 -1.6007745365301769, -16.101255416870117 -78.66190338134766 -1.6007745365301769, -15.609148025512695 -69.65843963623047 -1.6007745365301769, -14.8486909866333 -59.888206481933594 -1.6007745365301769, -13.977500915527344 -50.36618423461914 -1.6007745365301769, -13.212553024291992 -40.22431182861328 -1.6007745365301769, -12.336660385131836 -32.00490951538086 -1.6007745365301769, -11.306183815002441 -26.579072952270508 -1.6007745365301769, -9.596943855285645 -22.564157485961914 -1.6007745365301769, -6.637198448181152 -17.801366806030273 -1.6007745365301769, -5.787840508255876 -18.329184094384768 -1.6007745365301769, -8.706983945168561 -23.02663851777481 -1.6007745365301769, -10.343861412592982 -26.871578266025985 -1.6007745365301769, -11.346612002676704 -32.1514273893045 -1.6007745365301769, -12.216546786178723 -40.31492100963439 -1.6007745365301769, -12.980333280711736 -50.44139532473388 -1.6007745365301769, -12.981660225746298 -50.457295817726944 -1.6007745365301769, -13.852232521283806 -59.97256583851619 -1.6007745365301769, -14.611268090421495 -69.72453617178809 -1.6007745365301769, -15.102745802984373 -78.71647948397273 -1.6007745365301769, -15.103091882136365 -78.72248025752843 -1.6007745365301769, -15.729949639704724 -89.05161233760656 -1.6007745365301769, -15.73044200681818 -89.05924280193362 -1.6007745365301769, -16.55213161253107 -101.07812555339846 -1.6007745365301769, -16.55262383863296 -101.08497924533908 -1.6007745365301769, -17.078056425302883 -108.06530303684299 -1.6007745365301769, -18.07523536682129 -107.99024200439453 -1.6007745365301769)))')
    p_wkt = dumps(p, rounding_precision=3)
    p = loads(p_wkt)
    p = ops3D.trans_2d_3d(p)

    diff = l.difference(p)

    print(time.perf_counter_ns() - start_time)

    print('develop test')
