def hello():
    """打招呼函数

    Returns:
        str: 问候语
    """
    return "Hello, World!"

def add(a: int, b: int) -> int:
    """加法函数

    Args:
        a: 第一个整数
        b: 第二个整数

    Returns:
        int: 两数之和
    """
    return a + b

def find_max(numbers: list) -> int:
    """找出列表中的最大值

    Args:
        numbers: 数字列表

    Returns:
        int: 最大值

    Raises:
        ValueError: 如果列表为空
    """
    if not numbers:
        raise ValueError("列表不能为空")
    return max(numbers)

class Calculator:
    """简单计算器类"""

    def __init__(self):
        self.result = 0

    def add(self, x: int) -> int:
        """加上 x"""
        self.result += x
        return self.result

    def subtract(self, x: int) -> int:
        """减去 x"""
        self.result -= x
        return self.result

    def reset(self):
        """重置结果为 0"""
        self.result = 0
