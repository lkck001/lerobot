"""
类型注解详解：id: str | None = None
=====================================
详细解释 Python 类型注解和默认值的语法
"""

from dataclasses import dataclass
from typing import Optional, Union

print("\n" + "="*70)
print("【核心语法】id: str | None = None 的三个部分")
print("="*70)
print("""
id: str | None = None
│   │          │
│   │          └─→ 默认值（可选参数，不传就是 None）
│   └───────────→ 类型注解（可以是 str 或 None）
└───────────────→ 变量名
""")


print("\n" + "="*70)
print("【实验1】拆解每个部分")
print("="*70)

@dataclass(kw_only=True)
class Example1:
    # 部分1：只有变量名和类型（必须提供参数）
    name: str
    
    # 部分2：变量名 + 类型 + 默认值（可选参数）
    id: str | None = None

# 测试
print("只传必需参数 name：")
obj1 = Example1(name="对象1")
print(f"  obj1 = {obj1}")
print(f"  obj1.name = {obj1.name}")
print(f"  obj1.id = {obj1.id}  # 使用默认值 None")

print("\n传入所有参数：")
obj2 = Example1(name="对象2", id="abc123")
print(f"  obj2 = {obj2}")
print(f"  obj2.name = {obj2.name}")
print(f"  obj2.id = {obj2.id}")


print("\n" + "="*70)
print("【实验2】类型注解 str | None 的含义")
print("="*70)
print("""
str | None 是 Python 3.10+ 的语法，表示"联合类型"
意思是：这个变量可以是 str 类型，也可以是 None
""")

@dataclass(kw_only=True)
class Robot:
    id: str | None = None  # id 可以是字符串或 None

# ✅ 可以传入字符串
robot1 = Robot(id="robot_001")
print(f"传入字符串: robot1.id = {robot1.id}, 类型: {type(robot1.id)}")

# ✅ 可以传入 None
robot2 = Robot(id=None)
print(f"传入 None:   robot2.id = {robot2.id}, 类型: {type(robot2.id)}")

# ✅ 可以不传（使用默认值 None）
robot3 = Robot()
print(f"不传参数:   robot3.id = {robot3.id}, 类型: {type(robot3.id)}")

# ❌ 不能传入其他类型（虽然 Python 运行时不会报错，但类型检查工具会警告）
robot4 = Robot(id=12345)  # 类型检查器会警告：期望 str | None，实际是 int
print(f"传入数字:   robot4.id = {robot4.id}, 类型: {type(robot4.id)} ⚠️ 类型不匹配")


print("\n" + "="*70)
print("【实验3】为什么要用 str | None 而不是直接用 str？")
print("="*70)

@dataclass(kw_only=True)
class Config1:
    # 只用 str：必须传入字符串，不能为 None
    name: str

@dataclass(kw_only=True)
class Config2:
    # 用 str | None：可以传入字符串或 None
    name: str | None = None

print("Config1: name 必须是 str")
try:
    c1 = Config1()  # ❌ 报错！name 是必需参数
except TypeError as e:
    print(f"  ❌ 创建失败: {e}")

c1_ok = Config1(name="配置1")
print(f"  ✅ 正确创建: {c1_ok}")

print("\nConfig2: name 可以是 str 或 None")
c2_none = Config2()  # ✅ 可以不传，默认 None
print(f"  ✅ 不传参数: {c2_none}")

c2_str = Config2(name="配置2")  # ✅ 也可以传字符串
print(f"  ✅ 传入字符串: {c2_str}")


print("\n" + "="*70)
print("【实验4】旧版本 Python 的等价写法")
print("="*70)
print("""
Python 3.10 之前没有 | 运算符，需要用 typing 模块
""")

@dataclass(kw_only=True)
class OldStyle1:
    # 方式1：使用 Optional[str]（推荐）
    id: Optional[str] = None

@dataclass(kw_only=True)
class OldStyle2:
    # 方式2：使用 Union[str, None]
    id: Union[str, None] = None

@dataclass(kw_only=True)
class NewStyle:
    # Python 3.10+ 的新语法
    id: str | None = None

# 三种写法完全等价！
old1 = OldStyle1(id="test1")
old2 = OldStyle2(id="test2")
new = NewStyle(id="test3")

print(f"Optional[str]:     {old1}")
print(f"Union[str, None]:  {old2}")
print(f"str | None:        {new}")
print("三者完全等价，只是写法不同！")


print("\n" + "="*70)
print("【实验5】实际应用场景")
print("="*70)

from pathlib import Path

@dataclass(kw_only=True)
class TeleoperatorConfig:
    """模拟 lerobot 中的配置类"""
    
    # 可选的 ID，用于区分不同的遥控器
    id: str | None = None
    
    # 可选的校准文件目录
    calibration_dir: Path | None = None
    
    # 必需的遥控器类型
    type: str

print("场景1：最简配置（只提供必需参数）")
config1 = TeleoperatorConfig(type="keyboard")
print(f"  {config1}")
print(f"  - id 为 None（未指定）")
print(f"  - calibration_dir 为 None（不需要校准）")

print("\n场景2：指定 ID")
config2 = TeleoperatorConfig(type="gamepad", id="controller_01")
print(f"  {config2}")
print(f"  - 有了 ID，可以区分多个控制器")

print("\n场景3：完整配置")
config3 = TeleoperatorConfig(
    type="space_mouse",
    id="spacemouse_001",
    calibration_dir=Path("./calibration")
)
print(f"  {config3}")
print(f"  - 所有参数都提供了")


print("\n" + "="*70)
print("【实验6】如何使用这些可选值")
print("="*70)

@dataclass(kw_only=True)
class UserProfile:
    name: str
    email: str | None = None
    phone: str | None = None

user = UserProfile(name="张三", email="zhangsan@example.com")

print(f"用户: {user}")
print("\n检查可选字段是否提供：")

# 方式1：使用 if 判断
if user.email is not None:
    print(f"  ✓ 有邮箱: {user.email}")
else:
    print(f"  ✗ 没有邮箱")

if user.phone is not None:
    print(f"  ✓ 有电话: {user.phone}")
else:
    print(f"  ✗ 没有电话")

# 方式2：使用默认值
print(f"\n使用默认值：")
print(f"  邮箱: {user.email or '未提供'}")
print(f"  电话: {user.phone or '未提供'}")


print("\n" + "="*70)
print("【实验7】更复杂的类型注解示例")
print("="*70)

@dataclass(kw_only=True)
class AdvancedTypes:
    # 可以是字符串或 None
    name: str | None = None
    
    # 可以是整数或浮点数
    value: int | float = 0
    
    # 可以是字符串、整数或 None
    id: str | int | None = None
    
    # 列表，每个元素是字符串
    tags: list[str] = None  # 注意：这样写有 bug！
    
    def __post_init__(self):
        # 修复 tags 的默认值问题
        if self.tags is None:
            self.tags = []

obj = AdvancedTypes(name="测试", value=3.14, id=123)
print(f"复杂类型示例: {obj}")
print(f"  name 类型: {type(obj.name).__name__}")
print(f"  value 类型: {type(obj.value).__name__}")
print(f"  id 类型: {type(obj.id).__name__}")


print("\n" + "="*70)
print("【总结】id: str | None = None 的完整解释")
print("="*70)
print("""
┌─────────────────────────────────────────────────────────────────┐
│  id: str | None = None                                          │
│  │   │           │                                              │
│  │   │           └── 默认值是 None（这个参数是可选的）         │
│  │   │                                                           │
│  │   └────────────── 类型可以是 str 或 None                     │
│  │                   - 如果提供值，应该是字符串                 │
│  │                   - 也可以显式传入 None                       │
│  │                   - 不传参数时使用默认值 None                 │
│  │                                                               │
│  └──────────────────── 变量名是 id                              │
└─────────────────────────────────────────────────────────────────┘

💡 关键理解：
1. 类型注解（: str | None）是给程序员和工具看的，不强制执行
2. 默认值（= None）决定了参数是否必需
3. 有默认值 → 可选参数，不传也不会报错
4. 无默认值 → 必需参数，不传会报错

🎯 使用场景：
- 配置类中的可选参数
- 可能为空的数据库字段
- 函数的可选参数
- 可以延迟初始化的属性

⚠️ 常见陷阱：
- 默认值不要用可变对象（如 [] 或 {}）
- 应该用 None，然后在 __post_init__ 中初始化
""")

print("\n" + "="*70)
print("【对比表】不同写法的区别")
print("="*70)
print("""
┌──────────────────────┬─────────┬──────────┬────────────────┐
│ 声明                 │ 必需？  │ 可为None │ 默认值         │
├──────────────────────┼─────────┼──────────┼────────────────┤
│ id: str              │ 是      │ 否       │ 无             │
│ id: str = "default"  │ 否      │ 否       │ "default"      │
│ id: str | None       │ 是      │ 是       │ 无             │
│ id: str | None = None│ 否      │ 是       │ None           │
└──────────────────────┴─────────┴──────────┴────────────────┘

示例：
    name: str              # 必须传入字符串
    age: int = 0           # 可选，默认 0，但不能为 None
    id: str | None         # 必须传入，可以是 str 或 None
    email: str | None = None  # 可选，默认 None，也可以传字符串
""")

print("\n" + "="*70)
print("实验完成！")
print("="*70)

