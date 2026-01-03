#!/usr/bin/env python
"""
详细解释类型注解语法：TeleoperatorConfig | None = None
"""

print("="*70)
print("解析：robot: RobotConfig | None = None")
print("="*70)

# ============================================
# 第1部分：基础语法拆解
# ============================================
print("\n【语法拆解】")
print("-" * 70)
print("""
robot: RobotConfig | None = None
  │         │        │      │
  │         │        │      └─ 默认值（如果不传参数，就用这个值）
  │         │        └──────── 或（可以是 None）
  │         └───────────────── 类型（应该是 RobotConfig）
  └─────────────────────────── 变量名

完整含义：
  变量名：robot
  类型：RobotConfig 或者 None
  默认值：None
""")

# ============================================
# 第2部分：| 符号的含义
# ============================================
print("\n【| 符号的含义】")
print("-" * 70)
print("""
| 表示"或者"（OR）

RobotConfig | None
     ↓         ↓
  类型1      类型2

意思是：这个变量可以是以下两种类型之一：
  1. RobotConfig 对象
  2. None（空值）

类似于：
  - 可以是苹果或者橙子
  - 可以是字符串或者数字
  - 可以是配置对象或者空
""")

# 示例
from typing import Union

def example1(value: int | str):
    """value 可以是 int 或者 str"""
    pass

def example2(value: int | str | None):
    """value 可以是 int、str 或者 None"""
    pass

print("\n类型注解示例：")
print("  value: int | str       ← 可以是整数或字符串")
print("  value: int | None      ← 可以是整数或None")
print("  value: str | int | None ← 可以是字符串、整数或None")

# ============================================
# 第3部分：= None 的含义
# ============================================
print("\n【= None 的含义】")
print("-" * 70)
print("""
= None 表示默认值

robot: RobotConfig | None = None
                          ↑
                        默认值

意思是：
  如果创建对象时不传 robot 参数，就自动设置为 None

例如：
  cfg1 = SetupConfig()                    ← robot 自动为 None
  cfg2 = SetupConfig(robot=my_robot)      ← robot 为 my_robot
""")

# ============================================
# 第4部分：实际示例
# ============================================
print("\n【实际示例】")
print("-" * 70)

from dataclasses import dataclass

# 简化的配置类
@dataclass
class RobotConfig:
    name: str

@dataclass
class TeleoperatorConfig:
    name: str

@dataclass
class SetupConfig:
    teleop: TeleoperatorConfig | None = None
    robot: RobotConfig | None = None

# 测试1：不传任何参数
print("\n测试1: 不传参数")
cfg1 = SetupConfig()
print(f"  cfg1.teleop = {cfg1.teleop}")  # None
print(f"  cfg1.robot = {cfg1.robot}")    # None

# 测试2：只传 robot
print("\n测试2: 只传 robot")
cfg2 = SetupConfig(robot=RobotConfig(name="SO101"))
print(f"  cfg2.teleop = {cfg2.teleop}")  # None
print(f"  cfg2.robot = {cfg2.robot}")    # RobotConfig(name='SO101')

# 测试3：只传 teleop
print("\n测试3: 只传 teleop")
cfg3 = SetupConfig(teleop=TeleoperatorConfig(name="Leader"))
print(f"  cfg3.teleop = {cfg3.teleop}")  # TeleoperatorConfig(name='Leader')
print(f"  cfg3.robot = {cfg3.robot}")    # None

# 测试4：两个都传
print("\n测试4: 两个都传")
cfg4 = SetupConfig(
    robot=RobotConfig(name="SO101"),
    teleop=TeleoperatorConfig(name="Leader")
)
print(f"  cfg4.teleop = {cfg4.teleop}")
print(f"  cfg4.robot = {cfg4.robot}")

# ============================================
# 第5部分：为什么要用 | None
# ============================================
print("\n【为什么要用 | None】")
print("-" * 70)
print("""
在这个项目中，SetupConfig 有两个字段：
  - teleop: 遥控器配置
  - robot: 机器人配置

规则：只能选择一个！
  ✅ 要么配置 teleop
  ✅ 要么配置 robot
  ❌ 不能两个都配置
  ❌ 也不能两个都不配置

所以：
  - 如果选择 robot，则 teleop = None
  - 如果选择 teleop，则 robot = None

这就是为什么类型是：TeleoperatorConfig | None
                              ↑
                    允许为 None，因为可能不用
""")

# ============================================
# 第6部分：对比不同写法
# ============================================
print("\n【对比不同写法】")
print("-" * 70)

print("\n写法1: 必须提供值（没有默认值）")
print("""
@dataclass
class Config1:
    robot: RobotConfig  # ← 必须提供，不能为 None

# 使用：
cfg = Config1(robot=RobotConfig(...))  # ✅ 正确
cfg = Config1()                        # ❌ 错误：缺少必需参数
""")

print("\n写法2: 可以是 None，但必须显式传递")
print("""
@dataclass
class Config2:
    robot: RobotConfig | None  # ← 可以是 None，但没有默认值

# 使用：
cfg = Config2(robot=RobotConfig(...))  # ✅ 正确
cfg = Config2(robot=None)              # ✅ 正确
cfg = Config2()                        # ❌ 错误：缺少必需参数
""")

print("\n写法3: 可以是 None，且默认为 None（你的项目用的）")
print("""
@dataclass
class Config3:
    robot: RobotConfig | None = None  # ← 可以是 None，默认也是 None

# 使用：
cfg = Config3(robot=RobotConfig(...))  # ✅ 正确
cfg = Config3(robot=None)              # ✅ 正确
cfg = Config3()                        # ✅ 正确，自动设为 None
""")

# ============================================
# 第7部分：完整流程示例
# ============================================
print("\n【完整流程示例】")
print("-" * 70)

@dataclass
class SetupConfig:
    teleop: TeleoperatorConfig | None = None
    robot: RobotConfig | None = None
    
    def __post_init__(self):
        """初始化后的验证"""
        # 检查：必须有一个，且只能有一个
        if bool(self.teleop) == bool(self.robot):
            raise ValueError("必须选择 teleop 或 robot 其中之一")
        
        # 设置使用的设备
        self.device = self.robot if self.robot else self.teleop

print("\n测试：只传 robot（正确）")
try:
    cfg = SetupConfig(robot=RobotConfig(name="SO101"))
    print(f"  ✅ 成功创建")
    print(f"     robot = {cfg.robot}")
    print(f"     teleop = {cfg.teleop}")
    print(f"     device = {cfg.device}")
except ValueError as e:
    print(f"  ❌ 错误: {e}")

print("\n测试：两个都不传（错误）")
try:
    cfg = SetupConfig()
    print(f"  ✅ 成功创建")
except ValueError as e:
    print(f"  ❌ 错误: {e}")

print("\n测试：两个都传（错误）")
try:
    cfg = SetupConfig(
        robot=RobotConfig(name="SO101"),
        teleop=TeleoperatorConfig(name="Leader")
    )
    print(f"  ✅ 成功创建")
except ValueError as e:
    print(f"  ❌ 错误: {e}")

# ============================================
# 总结
# ============================================
print("\n" + "="*70)
print("总结")
print("="*70)
print("""
robot: RobotConfig | None = None
  │         │        │      │
  │         │        │      └─ 默认值：如果不传参数，值为 None
  │         │        └──────── 或：可以是 None
  │         └───────────────── 类型：应该是 RobotConfig
  └─────────────────────────── 变量名：robot

完整含义：
  定义一个变量 robot
  类型可以是 RobotConfig 或 None
  如果不传参数，默认为 None

使用场景：
  在你的项目中，setup_motors 可以配置机器人或遥控器
  但只能选一个，所以另一个就是 None
  
  命令行：
    --robot.type=so101 --robot.port=COM24  ← robot 有值，teleop 为 None
    --teleop.type=leader --teleop.port=USB ← teleop 有值，robot 为 None
""")

