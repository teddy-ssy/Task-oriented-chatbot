
import random


class NLG():
    #answer template
    def __init__(self):
        self.answer_template={}

        self.answer_template["unitCode"] = ["the unit #unitCode"]#unitCode
        self.answer_template["onOffer"]=["#unitCode is #onOffer on offer"]#unitCode #onOffer
        self.answer_template["level"] = ["#unitCode is a #level unit"]#unitCode #level
        self.answer_template["faculty"] = ["#unitCode offered by #faculty"]

        self.answer_template["lectures_name"] = ["#unitCode teach by #lectures_name","the #lectures_name"] #leactures_name replace to he or she
        self.answer_template["lectures_position"] = ["#youcanfind #lectures_name at #lectures_position" ]#
        self.answer_template["lectures_faculty"] = ["#youcanfind #lectures_name at #lectures_faculty"]
        self.answer_template["lectures_address"] = ["#youcanfind #lectures_name at #lectures_address"]
        self.answer_template["lectures_country"] = ["#lectures_name from #lectures_country"]
        self.answer_template["lectures_phone"] = ["#lectures_name phone number is #lectures_phone"]
        self.answer_template["lectures_mobile"] = ["#lectures_name mobile number is #lectures_mobile"]
        self.answer_template["lectures_email"] = ["#lectures_name email is #lectures_email"]
        self.answer_template["lectures_url"] = ["#lectures_name web link is #lectures_url"]
        self.answer_template["lectures_contactNot"] = [""]

        self.answer_template["tutors"] = ["#unitCode teach by #tutors","the #tutors"]
        self.answer_template["sessionOption"] = ["#unitCode offer in #sessionOption"]
        self.answer_template["link"] = ["the link of #unitCode is #link"]
        self.answer_template["campus"] = ["the #unitCode noramally start at #campus"]
        self.answer_template["prerequisites"] = ["the prerequisites of #unitCode is #prerequisites"]
        self.answer_template["prohibitions"] = ["the prohibitions of #unitCode is #prohibitions"]
        self.answer_template["description"] = ["the description of #unitCode is #description"]
        self.answer_template["assumedKnowledge"] = ["the assumeKnowledge of the #unitCode is #assumeKnowledge"]
        self.answer_template["timeTable"] = ["the timetable of #unitCode is #timeTable"]
        self.answer_template["activity"] = ["#unitCode have #activity activities"]
        self.answer_template["learningOutcome"] = ["the learning outcome of #unitCode is #learningOutcome"]

        self.answer_template["name"] = ["#name"]
        self.answer_template["group"] = ["#name is #group work"]
        self.answer_template["assignmentMethod_weight"] = ["#name take #assignemntMethod_weight"]
        self.answer_template["dueweek"] = ["#name due aat week #dueweek"]
        self.answer_template["outcomes"] = ["the outcome of #name is #outcomes"]
        self.answer_template["wieht"] = ["#name weight #outcome percent of final mark"]

        self.answer_template["assessmentDescription"] = ["the assessment description of #assignemntMethod_name is #assessmentDescription"]
        self.answer_template["assessmentFeedback"] = ["the #assignemntMethod_name will feedback by #assessmentFeedback"]

        self.answer_template["gradingType"] = ["the grading type of #unitCode is #gradingType"]
        self.answer_template["gradingDescription"] = ["the grading description of #uitCode is #gradingDescription"]

        self.answer_template["policies"] = ["#unitCode follow the assessment ploicy #policies"]
        self.answer_template["prescribedText"] = ["#unitCode require #prescribedText as the presecibred text"]
        self.answer_template["recommendedReference"] = ["the #recommendedReference is the recommend reference for #unitCode"]

        self.answer_template["schedules_week"] = ["of week #schedules_week"]
        self.answer_template["schedules_description"] = ["the description #schedules_week is #schedules_description"]

        self.answer_template["courseRelation_course"] = ["the related course of #unitCode are #courseRelation_course"]
        self.answer_template["courseRelation_yearOffered"] = [""]

        self.answer_template["goals_attribute"] = [""]
        self.answer_template["goals_practiced"] = [""]
        self.answer_template["goals_assessed"] = [""]


    def add_template(self,attribute,template):
        if attribute in self.answer_template.keys():
            self.answer_template[attribute].append(template)
        else:
            self.answer_template[attribute]=[template]

    def get_template(self,dict_database,dict_user):
        result=[]
        for k in dict_database.keys():# k is a string v is a list
            if k in self.answer_template.keys():
                for item in dict_database[k]:
                    temp =[]
                    for template in self.answer_template[k]:
                        #print(template)
                        template_list = template.split(" ")
                        num=0
                        keys =[]
                        for key in dict_user:
                            keys.append(key)
                        #print(keys)
                        for i in range(len(dict_user.keys())):
                            for unit in template_list:
                                if unit.__contains__("#" + keys[i]):
                                    num=num+1
                                else:
                                    pass
                        if num == len(dict_user.keys()):
                            temp.append(template_list)
                    #print(len(temp))
                    sub_template = temp[random.randint(0,len(temp)-1)]


                    for i in range(len(sub_template)):
                        if sub_template[i].__contains__("#"):
                            if sub_template[i].__contains__("#" + k):
                                if item == "yes":
                                    sub_template[i] =""
                                else :
                                    sub_template[i] = item
                                #print(template_list)
                            else:
                                for K in dict_user.keys():
                                    if sub_template[i].__contains__("#" + K):
                                        sub_template[i] = dict_user[K]
                                        #print(template_list)
                    result.append(sub_template)
        #print(result)
        return result

    def find_template_by(self,attribute1,attributes2):
        if attribute1 in self.answer_template.keys():
            #template = self.answer_template[attribute1][random.randint(0, len(self.answer_template[attribute1]) - 1)]
            templates = self.answer_template[attribute1]
            results=[]
            for template in templates:
                template_list = template.split(" ")
                num = 0
                keys = []
                for key in attributes2:
                    keys.append(key)
                # print(keys)
                for i in range(len(attributes2)):
                    for unit in template_list:
                        if unit.__contains__("#" + keys[i]):
                            num = num + 1
                        else:
                            pass
                if num == len(attributes2):
                    results.append(template_list)
            template = results[random.randint(0, len(results) - 1)]
        #print(template)
        return template

    def intergate_two_template(self,template1,template2):
        for item1 in template1:
            for i in range(len(template2)):
                if item1 == template2[i] and item1.__contains__("#"):
                    template2[i] = "it"
        result = template1+["and"]+template2
        #print(result)
        return result

    def get_finial_template(self,dict_database,dict_user):
        result = []
        for k in dict_database.keys():  # k is a string v is a list
            result.append(self.find_template_by(k,dict_user.keys()))
        template=[]
        for temp in result:
            template= self.intergate_two_template(template,temp)
        #print(template)
        return template

    def find_template_by_one(self, attribute1):
        temp = []
        if attribute1 in self.answer_template.keys():
            #template = self.answer_template[attribute1][random.randint(0, len(self.answer_template[attribute1]) - 1)]
            templates = self.answer_template[attribute1]
            for template in templates:
                #print(template)
                list = template.split(" ")
                num=0
                for item in list:
                    if item.__contains__("#"):
                        num = num+1
                if num==1:
                    temp.append(template)
        if temp==[]:
            return None
        return temp[random.randint(0, len(temp) - 1)]

    def fill_slot(self,dict_database,dict_user):
        temp = self.get_finial_template(dict_database,dict_user)
        template = temp
        for slot in range(len(template)):
            if template[slot].__contains__("#"):
                if template[slot].split("#")[-1] in self.answer_template.keys():
                    temps = self.find_template_by_one(template[slot].split("#")[-1])
                    #print(temp)
                    if temps is None:
                        if template[slot].split("#")[-1] in dict_database:
                            if dict_database[template[slot].split("#")[-1]][0]=="yes":
                                template[slot] =""
                            else:
                                template[slot] = dict_database[template[slot].split("#")[-1]][0]
                        elif template[slot].split("#")[-1] in dict_user:
                            if dict_user[template[slot].split("#")[-1]][0]=="yes":
                                template[slot] = ""
                            else:
                                template[slot] = dict_user[template[slot].split("#")[-1]][0]
                    else:
                        temps=temps.split(" ")
                        for item in range(len(temps)):
                            if temps[item].__contains__("#"):
                                if temps[item].split("#")[-1] in dict_database:
                                    temps[item] = dict_database[temps[item].split("#")[-1]]
                                elif temps[item].split("#")[-1] in dict_user:
                                    temps[item] = dict_user[temps[item].split("#")[-1]]
                        #template[slot]=temps
                        #print(temps)
                        temp1=template[0:slot]
                        #print(temp1)
                        temp2=template[slot+1:]
                        #print(temp2)
                        template=temp1+temps+temp2
                        #print(template)

        #print(template[1:])
        return template[1:],dict_database,dict_user



def test():
    nlg_model = NLG()
    dict_database = {"onOffer": ["yes"], "level": ["postgraduate"]}
    dict_user = {"unitCode": "comp5426"}

    # "assement":
    answer, dict_database, dict_user = nlg_model.fill_slot(dict_database, dict_user)

    print(answer)
    print(dict_database)
    print(dict_user)

#test()

