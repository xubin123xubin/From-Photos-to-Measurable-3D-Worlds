import numpy as np
from plyfile import PlyData, PlyElement

class InstantSplatPLYParser:
    """
    增强版PLY文件解析器
    支持InstantSplat不同阶段生成的点云格式
    """
    
    def __init__(self, ply_path):
        self.ply_path = ply_path
        self.properties = {}
        self.header_info = {}
        self.vertex_count = 0
        self.is_gaussian = False  # 是否为高斯点云
        
    def parse(self):
        ply_data = PlyData.read(self.ply_path)
        
        if 'vertex' not in ply_data:
            raise ValueError("Invalid PLY file: No vertex element found")
        
        vertices = ply_data['vertex']
        self.vertex_count = vertices.count
        
        # 检查是否为高斯点云
        self._check_gaussian_format(vertices)
        
        self._extract_header_info(ply_data)
        self._extract_properties(vertices)
        
        return self
    
    def _check_gaussian_format(self, vertices):
        """检查是否为3D高斯点云格式"""
        # 高斯点云特有的属性
        gaussian_props = {'opacity', 'scale_0', 'rot_0', 'f_dc_0'}
        available_props = set(vertices.data.dtype.names)
        
        # 如果包含任意高斯属性则认为是高斯点云
        self.is_gaussian = len(gaussian_props & available_props) > 0
    
    def _extract_header_info(self, ply_data):
        self.header_info = {
            'format': ply_data.header.format,
            'elements': [elem.name for elem in ply_data.elements],
            'comments': ply_data.comments,
            'vertex_count': self.vertex_count,
            'is_gaussian': self.is_gaussian
        }
    
    def _extract_properties(self, vertices):
        property_names = vertices.data.dtype.names
        
        for prop in property_names:
            prop_data = vertices[prop]
            
            # 处理多维属性
            if prop_data.ndim > 1:
                self.properties[prop] = np.array([v for v in prop_data])
            else:
                self.properties[prop] = np.array(prop_data)
    
    def get_property(self, name):
        if name not in self.properties:
            available = ', '.join(self.properties.keys())
            raise KeyError(f"Property '{name}' not found. Available properties: {available}")
        return self.properties[name]
    
    def get_position(self):
        """获取点云位置坐标"""
        return np.column_stack((
            self.get_property('x'),
            self.get_property('y'),
            self.get_property('z')
        ))
    
    def get_normals(self):
        """获取点云法线向量"""
        return np.column_stack((
            self.get_property('nx'),
            self.get_property('ny'),
            self.get_property('nz')
        ))
    
    def get_color(self):
        """获取点云颜色 - 支持两种格式"""
        if self.is_gaussian:
            # 高斯点云：从球谐系数推导颜色
            try:
                f_dc = self.get_property('f_dc_0')
                if f_dc.ndim == 1:  # 单点情况
                    return f_dc
                return f_dc[:, 0, :]  # 取球谐系数的DC项
            except KeyError:
                pass
        
        # 初始几何点云：直接使用RGB值
        return np.column_stack((
            self.get_property('red'),
            self.get_property('green'),
            self.get_property('blue')
        )) / 255.0  # 归一化到[0,1]
    
    def get_opacity(self):
        """获取不透明度（仅高斯点云）"""
        if not self.is_gaussian:
            return None
        try:
            return self.get_property('opacity')
        except KeyError:
            return None
    
    def get_gaussian_properties(self):
        """获取高斯点云特有属性"""
        if not self.is_gaussian:
            return {}
        
        properties = {}
        for prop in ['scale_0', 'scale_1', 'scale_2', 
                     'rot_0', 'rot_1', 'rot_2', 'rot_3',
                     'f_dc_0', 'f_rest_0']:
            try:
                properties[prop] = self.get_property(prop)
            except KeyError:
                pass
                
        return properties
    
    def summary(self):
        print(f"PLY File: {self.ply_path}")
        print(f"Vertex Count: {self.vertex_count}")
        print(f"Point Cloud Type: {'3D Gaussian' if self.is_gaussian else 'Initial Geometry'}")
        print(f"Properties: {list(self.properties.keys())}")
        
        # 打印属性统计信息
        print("\nProperty Statistics:")
        for prop, values in self.properties.items():
            dtype = values.dtype
            shape = values.shape
            stats = ""
            
            if np.issubdtype(dtype, np.floating):
                stats = f"Range: [{np.min(values):.4f}, {np.max(values):.4f}]"
            elif np.issubdtype(dtype, np.integer):
                stats = f"Range: [{np.min(values)}, {np.max(values)}]"
                
            if len(shape) == 1:
                print(f"  - {prop}: {len(values)} elements, {dtype}, {stats}")
            else:
                print(f"  - {prop}: {shape} shape, {dtype}, {stats}")

# 使用示例
if __name__ == "__main__":
    ply_file = "output_infer/sora/Art/point_cloud/iteration_1000/point_cloud.ply"  # 替换为你的PLY文件路径
    
    try:
        parser = InstantSplatPLYParser(ply_file)
        parser.parse()
        parser.summary()
        
        # 获取点云数据
        positions = parser.get_position()
        colors = parser.get_color()
        normals = parser.get_normals()
        
        print("\nExtracted Data:")
        print(f"Positions shape: {positions.shape}")
        print(f"Colors shape: {colors.shape}")
        print(f"Normals shape: {normals.shape}")
        
        # 检查是否为高斯点云
        if parser.is_gaussian:
            print("\nGaussian Properties:")
            gaussian_props = parser.get_gaussian_properties()
            for prop, values in gaussian_props.items():
                print(f"  {prop}: shape={values.shape}, dtype={values.dtype}")
            
            opacity = parser.get_opacity()
            if opacity is not None:
                print(f"Opacity range: [{opacity.min():.4f}, {opacity.max():.4f}]")
        
    except Exception as e:
        print(f"Error parsing PLY file: {e}")