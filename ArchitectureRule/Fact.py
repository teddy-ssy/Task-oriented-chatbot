from pyknow import *
import schema

class Arrow(Fact):
    """
    箭头

    包含：
    描述，开始的chart，结束的chart，箭头类型，颜色
    """
    description=Field(str,default="None")
    start_chart=Field(str, mandatory=True)
    end_chart=Field(str, mandatory=True)
    arrow_type=Field(schema.Or("single","double"),mandatory=True)
    color=Field(str)

class FlowChart(Fact):
    """
    图形

    包含：
    名字，描述，类型
    """
    description=Field(str,default="None")
    name =Field(str,mandatory=True)
    chart_type=Field(schema.Or("process","decision","start","terminator","document","data","predefined process","store data","internal storage","sequential data","direct data"),default="process")
    color=Field(str)


class GoalIsTo(Fact):
    """
    目标

    包含：
    行为（new chart，new arrow，delete arrow， reset arrow，delete chart, reset chart）
    对象
    """
    intent = Field(schema.Or("new_chart","new_arrow","reset_chart","reset_arrow","delete_chart","delete_arrow","done"),mandatory=True)
    arguments = Field(str,mandatory=True)
