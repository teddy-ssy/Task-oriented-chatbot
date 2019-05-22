from pyknow import *
import schema

class Arrow(Fact):

    description=Field(str,default="None")
    start_chart=Field(str, mandatory=True)
    end_chart=Field(str, mandatory=True)
    arrow_type=Field(schema.Or("single","double"),mandatory=True)
    color=Field(str)

class FlowChart(Fact):

    description=Field(str,default="None")
    name =Field(str,mandatory=True)
    chart_type=Field(schema.Or("process","decision","start","terminator","document","data","predefined process","store data","internal storage","sequential data","direct data"),default="process")
    color=Field(str)


class GoalIsTo(Fact):

    intent = Field(str,mandatory=True)
    arguments = Field(str,mandatory=True)
