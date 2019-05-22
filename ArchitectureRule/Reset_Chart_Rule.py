from ArchitectureRule.Fact import *
from SpeechRecogniztion.Speech_Recogniztion import *
from TTS.TTS import *

class ResetChartRule:
    """
    重设chart
    """

    @Rule(
        AS.goal << GoalIsTo(intent="reset_chart", arguments=MATCH.object)
    )
    def reset_chart(self,goal):
        self.retract(goal)
        print("reset chart general")
        Txt2Voice("reset chart")

        def ask_user_for_reset_chart():
            print("what attribute you want to modify?")
            Txt2Voice("what attribute you want to modify?")
            attribute = Start_one_speech()
            print("which chart you want to modify?")
            Txt2Voice("which chart you want to modify?")
            name = Start_one_speech()

            return attribute, name

        attribute,name= ask_user_for_reset_chart()
        #attribute, name = "name", "teddy"
        # name, description, chart_type, color = "teddy","non description","start","red"
        # #self.declare(FlowChart(description=description, name=name, chart_type=chart_type, color=color))
        print("you want modify -" + attribute + "--")
        Txt2Voice("modify " + attribute)
        self.declare(GoalIsTo(intent="reset_chart_" + attribute, arguments=name))#name,description,type,color


    @Rule(
        AS.goal << GoalIsTo(intent="reset_chart_name", arguments=MATCH.name),
        AS.chart << FlowChart(name=MATCH.name,description=MATCH.description,chart_type=MATCH.chart_type,color=MATCH.color)
    )
    def reset_chart_name(self, goal, chart):
        self.retract(goal)
        print("reset chart name")
        Txt2Voice("reset chart name")

        # self.retract(goal)
        def ask_user_for_reset_chart():
            print("give me a new name?")
            Txt2Voice("give me a new name?")
            new_name = Start_one_speech()

            return new_name

        new_name = ask_user_for_reset_chart()
        #new_name = "daddy"
        print("the new name is-" + new_name + "--")
        Txt2Voice("the new name is " + new_name)
        self.modify(chart, name=new_name)
        self.declare(GoalIsTo(intent="done", arguments="None"))


    @Rule(
        AS.goal << GoalIsTo(intent="reset_chart_description", arguments=MATCH.name),
        AS.chart << FlowChart(name=MATCH.name,description=MATCH.description,chart_type=MATCH.chart_type,color=MATCH.color)
    )
    def reset_chart_description(self, goal, chart):
        self.retract(goal)
        print("reset chart name")
        Txt2Voice("reset chart name")
        # self.retract(goal)
        def ask_user_for_reset_chart():
            print("give me a new description?")
            Txt2Voice("give me a new description?")
            new_description = Start_one_speech()

            return new_description

        new_description = ask_user_for_reset_chart()
        #new_description = "daddy"
        print("the new description is-" + new_description + "--")
        Txt2Voice("the new description is " + new_description)
        self.modify(chart, description=new_description)
        self.declare(GoalIsTo(intent="done", arguments="None"))


    @Rule(
        AS.goal << GoalIsTo(intent="reset_chart_type", arguments=MATCH.name),
        AS.chart << FlowChart(name=MATCH.name, description=MATCH.description, chart_type=MATCH.chart_type,
                              color=MATCH.color)
    )
    def reset_chart_type(self, goal, chart):
        self.retract(goal)
        print("reset chart type")
        Txt2Voice("reset chart type")

        # self.retract(goal)
        def ask_user_for_reset_chart():
            print("give me a new type?")
            Txt2Voice("give me a new type?")
            new_type = Start_one_speech()

            return new_type

        new_type = ask_user_for_reset_chart()
        #new_type = "daddy"
        print("the new description is-" + new_type + "--")
        Txt2Voice("the new description is " + new_type)
        self.modify(chart, chart_type=new_type)
        self.declare(GoalIsTo(intent="done", arguments="None"))


    @Rule(
        AS.goal << GoalIsTo(intent="reset_chart_color", arguments=MATCH.name),
        AS.chart << FlowChart(name=MATCH.name, description=MATCH.description, chart_type=MATCH.chart_type,
                              color=MATCH.color)
    )
    def reset_chart_color(self, goal, chart):
        self.retract(goal)
        print("reset chart color")
        Txt2Voice("reset chart color")

        # self.retract(goal)
        def ask_user_for_reset_chart():
            print("give me a new color?")
            Txt2Voice("give me a new color?")
            new_color = Start_one_speech()

            return new_color

        new_color = ask_user_for_reset_chart()
        #new_color = "daddy"
        print("the new color is-" + new_color + "--")
        Txt2Voice("the new color is " + new_color)
        self.modify(chart, color=new_color)
        self.declare(GoalIsTo(intent="done", arguments="None"))