#!/usr/bin/env python
"""
简化版的 draccus 机制演示
展示机器类型如何传递给 RobotConfig
"""

# ============================================
# 第1部分：模拟 draccus.ChoiceRegistry
# ============================================
class ChoiceRegistry:
    """注册表基类"""
    _registry = {}  # 存储：名字 -> 类
    
    @classmethod
    def register_subclass(cls, name):
        """装饰器：注册子类"""
        def decorator(subclass):
            print(f"📝 注册：'{name}' -> {subclass.__name__}")
            cls._registry[name] = subclass
            subclass._choice_name = name
            return subclass
        return decorator
    
    def get_choice_name(self, klass):
        """获取类注册时的名字"""
        return klass._choice_name
    
    @classmethod
    def get_subclass_by_name(cls, name):
        """根据名字查找子类"""
        return cls._registry.get(name)


# ============================================
# 第2部分：定义机器人配置（类似你的项目）
# ============================================
class RobotConfig(ChoiceRegistry):
    """机器人配置基类"""
    
    def __init__(self, port, id=None):
        self.port = port
        self.id = id
        print(f"  → RobotConfig.__init__() 被调用")
        print(f"     参数: port={port}, id={id}")
        print(f"     注意：没有 type 参数！")
    
    @property
    def type(self):
        """动态属性：返回机器类型"""
        result = self.get_choice_name(self.__class__)
        print(f"  → 访问 .type 属性 -> 动态计算返回: '{result}'")
        return result


# 注册子类（这发生在导入时）
@RobotConfig.register_subclass("so101_follower")  # ← 这里注册名字
class SO101FollowerConfig(RobotConfig):
    """SO101 机器人配置"""
    pass


@RobotConfig.register_subclass("so100_follower")
class SO100FollowerConfig(RobotConfig):
    """SO100 机器人配置"""
    pass


print("\n" + "="*60)
print("注册完成！注册表内容：")
print(RobotConfig._registry)
print("="*60 + "\n")


# ============================================
# 第3部分：模拟命令行解析和对象创建
# ============================================
def simulate_draccus(robot_type, robot_port):
    """模拟 draccus 的工作流程"""
    
    print(f"\n{'='*60}")
    print(f"模拟命令行输入：")
    print(f"  --robot.type={robot_type}")
    print(f"  --robot.port={robot_port}")
    print(f"{'='*60}\n")
    
    # 步骤1：解析命令行参数为字典
    print("步骤1: 解析命令行参数")
    params = {
        "type": robot_type,
        "port": robot_port
    }
    print(f"  解析结果: {params}\n")
    
    # 步骤2：查找注册表
    print("步骤2: 查找注册表")
    print(f"  查找 type='{robot_type}'...")
    ConfigClass = RobotConfig.get_subclass_by_name(robot_type)
    print(f"  找到类: {ConfigClass.__name__}\n")
    
    # 步骤3：创建实例（注意：不传 type！）
    print("步骤3: 创建实例")
    print(f"  调用: {ConfigClass.__name__}(port='{robot_port}')")
    robot = ConfigClass(port=robot_port)
    print(f"  实例创建完成: {robot}\n")
    
    # 步骤4：访问 type 属性
    print("步骤4: 访问 type 属性")
    print(f"  调用: robot.type")
    result = robot.type
    print(f"  结果: '{result}'\n")
    
    # 步骤5：验证
    print("步骤5: 验证")
    print(f"  robot.port = '{robot.port}'")
    print(f"  robot.type = '{robot.type}'")
    print(f"  robot.__class__.__name__ = '{robot.__class__.__name__}'")
    print(f"  type(robot) = {type(robot)}")
    
    return robot


# ============================================
# 第4部分：运行演示
# ============================================
if __name__ == "__main__":
    # 演示1：创建 SO101 机器人
    robot1 = simulate_draccus("so101_follower", "COM24")
    
    print("\n" + "🔹"*30 + "\n")
    
    # 演示2：创建 SO100 机器人
    robot2 = simulate_draccus("so100_follower", "COM42")
    
    print("\n" + "="*60)
    print("关键总结：")
    print("="*60)
    print("1. type 在命令行中：用于「选择」要创建哪个类")
    print("2. type 不是构造参数：创建实例时不需要传 type")
    print("3. type 是动态属性：访问时自动查注册表获取")
    print("4. 流程：命令行type → 查注册表 → 创建对应类 → 访问.type返回注册名")
    print("="*60)

