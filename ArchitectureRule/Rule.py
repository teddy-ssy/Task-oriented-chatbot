from pyknow import *
from ArchitectureRule.Fact import *
from SpeechRecogniztion.Speech_Recogniztion import *

class NewChartRule:
    """
    当intent是new_chart时
    """

    @Rule(
        AS.goal <<GoalIsTo(intent="new_chart",arguments="full"),
        #AS.flowchart <<FlowChart(description=MATCH.description,name=MATCH.name,chart_type=MATCH.chart_type,color=MATCH.color)
        #FlowChart(description=MATCH.description,name=MATCH.name,chart_type=MATCH.chart_type,color=MATCH.color)
    )
    def create_a_new_chart(self,goal,description,name,chart_type,color):
        self.declare(FlowChart(description=description,name=name,chart_type=chart_type,color=color))
        self.retract(goal)
    """
    当：
    如果goal是new_chart,
    
    declare FlowChart
    """

    @Rule(
        AS.goal <<GoalIsTo(intent="new_chart",arguments ="empty")
    )
    def declare_chart(self,goal):
        self.retract(goal)

        def ask_user_for_chart():
            print("define the file name:")
            name = Start_one_speech()

            print("any chart description?")
            description = Start_one_speech()

            print("you can select the chart type:")
            chart_type = Start_one_speech()

            print("give me a color:")
            color = Start_one_speech()
            return name, description,chart_type,color
        #name, description,chart_type,color = ask_user_for_chart()
        name, description, chart_type, color = "teddy","non description","start","red"

        self.declare(FlowChart(description= description,name= name,chart_type=chart_type,color=color))
        print("create a new chart name -"+name+"--")
        self.declare(GoalIsTo(intent="done",arguments="None"))
    """
    当：
    goal是new_chart,empty
    
    declare
    
    """

class ArchitectureRule(NewChartRule,KnowledgeEngine):

    @Rule()
    def startup(self):
        print("start architecture rule base,how to help")
        goal = Start_one_speech()
        if goal =="new chart":
            self.declare(GoalIsTo(intent="new_chart", arguments="empty"))
        else:
            self.declare(GoalIsTo(intent="done", arguments="None"))


    @Rule(
        AS.goal<<GoalIsTo(intent= "done",arguments=MATCH.obj)
    )
    def ask_for_operation(self,goal):
        self.retract(goal)
        print("the intent is done, any more intent ")
        new_goal = Start_one_speech()
        print()
        if new_goal == "new chart":
            self.declare(GoalIsTo(intent="new_chart", arguments="empty"))

