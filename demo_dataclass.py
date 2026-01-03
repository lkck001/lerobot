"""
@dataclass 装饰器功能演示
======================
演示 dataclass 的各种功能和 kw_only=True 的作用
"""

from dataclasses import dataclass, field
from typing import List

print("\n" + "="*70)
print("【实验1】基本的 @dataclass 装饰器")
print("="*70)

# 不使用 dataclass 的传统类
class PersonTraditional:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email
    
    def __repr__(self):
        return f"PersonTraditional(name={self.name}, age={self.age}, email={self.email})"
    
    def __eq__(self, other):
        if not isinstance(other, PersonTraditional):
            return False
        return self.name == other.name and self.age == other.age and self.email == other.email

# 使用 dataclass 的类（自动生成 __init__, __repr__, __eq__ 等方法）
@dataclass
class PersonDataclass:
    name: str
    age: int
    email: str

# 对比：代码更简洁，功能相同
p1_trad = PersonTraditional("张三", 25, "zhangsan@example.com")
p1_data = PersonDataclass("张三", 25, "zhangsan@example.com")

print(f"传统类创建: {p1_trad}")
print(f"dataclass创建: {p1_data}")
print(f"两者相等性比较: {p1_trad.name == p1_data.name}")

# dataclass 自动提供的 __eq__ 方法
p2_data = PersonDataclass("张三", 25, "zhangsan@example.com")
print(f"dataclass 相等性比较: p1_data == p2_data = {p1_data == p2_data}")


print("\n" + "="*70)
print("【实验2】@dataclass vs @dataclass(kw_only=True)")
print("="*70)

# 默认的 dataclass：可以位置参数或关键字参数
@dataclass
class RobotConfig:
    name: str
    max_speed: float
    port: int

# 可以用位置参数（顺序必须正确）
robot1 = RobotConfig("机器人1", 2.5, 8080)
print(f"位置参数创建: {robot1}")

# 也可以用关键字参数
robot2 = RobotConfig(name="机器人2", max_speed=3.0, port=8081)
print(f"关键字参数创建: {robot2}")

# 混合使用（位置参数必须在关键字参数前面）
robot3 = RobotConfig("机器人3", max_speed=2.0, port=8082)
print(f"混合参数创建: {robot3}")


# 使用 kw_only=True：强制只能使用关键字参数
@dataclass(kw_only=True)
class TeleoperatorConfig:
    name: str
    max_speed: float
    port: int

# ❌ 这样会报错：不能用位置参数
# teleop1 = TeleoperatorConfig("遥控器1", 2.5, 8080)  # TypeError!

# ✅ 必须使用关键字参数
teleop1 = TeleoperatorConfig(name="遥控器1", max_speed=2.5, port=8080)
print(f"kw_only=True 创建: {teleop1}")

print("\n💡 kw_only=True 的好处：")
print("  1. 代码更清晰：一眼就能看出每个参数的含义")
print("  2. 更安全：不会因为参数顺序错误导致bug")
print("  3. 更灵活：添加新参数不会破坏现有代码")


print("\n" + "="*70)
print("【实验3】默认值的使用")
print("="*70)

@dataclass(kw_only=True)
class SetupConfig:
    # 必需参数（没有默认值）
    name: str
    
    # 可选参数（有默认值）
    timeout: int = 30
    debug: bool = False
    max_retries: int = 3

# 只提供必需参数
config1 = SetupConfig(name="配置1")
print(f"使用默认值: {config1}")

# 覆盖某些默认值
config2 = SetupConfig(name="配置2", debug=True, max_retries=5)
print(f"覆盖默认值: {config2}")


print("\n" + "="*70)
print("【实验4】field() 高级功能")
print("="*70)

@dataclass(kw_only=True)
class AdvancedConfig:
    # 基本字段
    name: str
    
    # 使用 field() 设置默认工厂函数（用于可变对象）
    tags: List[str] = field(default_factory=list)
    
    # 使用 field() 设置其他选项
    metadata: dict = field(default_factory=dict)
    
    # 不在 __repr__ 中显示的字段
    internal_id: int = field(default=0, repr=False)
    
    # 不参与比较的字段
    timestamp: float = field(default=0.0, compare=False)

cfg1 = AdvancedConfig(name="配置A")
cfg1.tags.append("标签1")
print(f"配置A: {cfg1}")

cfg2 = AdvancedConfig(name="配置B")
print(f"配置B: {cfg2}")
print(f"注意: cfg2.tags 是空的，不会共享 cfg1 的 tags = {cfg2.tags}")

# timestamp 不参与比较
cfg3 = AdvancedConfig(name="配置A", timestamp=100.0)
cfg4 = AdvancedConfig(name="配置A", timestamp=200.0)
print(f"尽管 timestamp 不同，但 cfg3 == cfg4: {cfg3 == cfg4}")


print("\n" + "="*70)
print("【实验5】继承和混合使用")
print("="*70)

@dataclass(kw_only=True)
class BaseConfig:
    name: str
    version: str = "1.0"

@dataclass(kw_only=True)
class ExtendedConfig(BaseConfig):
    port: int = 8080
    ssl_enabled: bool = False

# 子类继承父类的所有字段
ext_cfg = ExtendedConfig(name="扩展配置", port=9090, ssl_enabled=True)
print(f"继承的配置: {ext_cfg}")
print(f"访问父类字段: version = {ext_cfg.version}")


print("\n" + "="*70)
print("【实验6】实战案例 - 模拟 lerobot 的配置")
print("="*70)

from pathlib import Path

@dataclass(kw_only=True)
class RobotControlConfig:
    # 机器人标识
    id: str | None = None
    
    # 校准文件目录
    calibration_dir: Path | None = None
    
    # 控制参数
    max_velocity: float = 1.0
    max_acceleration: float = 0.5
    
    # 安全参数
    emergency_stop_enabled: bool = True
    
    def __post_init__(self):
        """dataclass 的后处理方法，在 __init__ 之后自动调用"""
        if self.calibration_dir is not None:
            self.calibration_dir = Path(self.calibration_dir)
            print(f"  ✓ 校准目录已转换为 Path 对象")

# 创建配置实例
robot_cfg = RobotControlConfig(
    id="robot_001",
    calibration_dir="./calibration",
    max_velocity=2.5
)

print(f"机器人配置: {robot_cfg}")
print(f"类型检查: calibration_dir 是 Path? {isinstance(robot_cfg.calibration_dir, Path)}")


print("\n" + "="*70)
print("【总结】@dataclass 的主要优点")
print("="*70)
print("""
1. ✨ 自动生成代码：
   - __init__() : 初始化方法
   - __repr__() : 字符串表示
   - __eq__()   : 相等性比较
   
2. 📝 代码更简洁：
   - 传统类需要 20+ 行，dataclass 只需 5 行
   
3. 🔒 kw_only=True 的好处：
   - 强制关键字参数，代码更清晰
   - 参数顺序无关，更灵活
   - 防止参数传递错误
   
4. 🎯 类型提示：
   - 自动支持类型注解
   - IDE 可以提供更好的代码提示
   
5. 🛠️ 灵活性：
   - 默认值、field() 配置
   - __post_init__() 后处理
   - 继承和组合
""")

print("\n" + "="*70)
print("实验完成！")
print("="*70)

