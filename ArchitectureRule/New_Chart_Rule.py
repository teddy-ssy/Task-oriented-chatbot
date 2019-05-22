from ArchitectureRule.Fact import *
from SpeechRecogniztion.Speech_Recogniztion import *
from TTS.TTS import *

class NewChartRule:
    """
    当intent是new_chart时
    """

    @Rule(
        AS.goal << GoalIsTo(intent="new_chart", arguments="empty")
    )
    def declare_chart(self, goal):
        self.retract(goal)

        def ask_user_for_chart():
            print("define the file name:")
            Txt2Voice("define the file name:")
            name = Start_one_speech()

            print("any chart description?")
            Txt2Voice("any chart description?")
            description = Start_one_speech()

            print("you can select the chart type:")
            Txt2Voice("you can select the chart type:")
            chart_type = Start_one_speech()

            print("give me a color:")
            Txt2Voice("give me a color:")
            color = Start_one_speech()
            return name, description, chart_type, color

        name, description,chart_type,color = ask_user_for_chart()
        #name, description, chart_type, color = "teddy", "non description", "start", "red"

        self.declare(FlowChart(description=description, name=name, chart_type=chart_type, color=color))
        print("create a new chart name -" + name + "--")
        Txt2Voice("create a new chart name is " + name )
        self.declare(GoalIsTo(intent="done", arguments="None"))
