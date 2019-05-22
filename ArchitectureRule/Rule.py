from ArchitectureRule.New_Chart_Rule import *
from ArchitectureRule.Reset_Chart_Rule import *
from TTS.TTS import *

class ArchitectureRule(NewChartRule,
                       ResetChartRule,
                       KnowledgeEngine):

    @Rule()
    def startup(self):
        print("start architecture rule base,how to help")
        Txt2Voice("how to help")
        goal = Start_one_speech()
        #goal = "new chart"
        if goal =="new chart":
            self.declare(GoalIsTo(intent="new_chart", arguments="empty"))
        elif goal=="reset chart":
            self.declare(GoalIsTo(intent="reset_chart", arguments="None"))
        else:
            self.declare(GoalIsTo(intent="done", arguments="None"))


    @Rule(
        AS.goal << GoalIsTo(intent= "done",arguments=MATCH.obj)
    )
    def ask_for_operation(self,goal):
        self.retract(goal)
        print("the intent is done, any more intent ")
        Txt2Voice("any more intent ")
        new_goal = Start_one_speech()
        #new_goal = "reset chart"
        if new_goal == "new chart":
            self.declare(GoalIsTo(intent="new_chart", arguments="empty"))
        elif new_goal == "reset chart":
            self.declare(GoalIsTo(intent="reset_chart", arguments="None"))
        else:
            self.declare(GoalIsTo(intent="done", arguments="None"))

