from NLU.string_matching import *
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
from NLU import constants


class NER():
    #answer template
    def __init__(self):
        self.answer_template={}

        #template

        self.answer_template["unitname"] = ["the unit of #unitname", "I want to the #unitname",
                                            "can you tell me the #unitname idea",
                                            "give me the full name of #unitname",
                                            "please tell me the reference of #unitname",
                                            "the teacher of #unitname is good", "when can i chiose the #unitname",
                                            "is #unitname on offer", "is #unitname a night school course",
                                            "tell me how many people in #unitname",
                                            "how many student fall in #unitname",
                                            "I think the #unitname is a greate unit"]  # unitCode
        """
        self.answer_template["coursename"] = ["the course of #coursename", "I want to the #coursename",
                                            "can you tell me the #coursename idea",
                                            "give me the full name of #coursename",
                                            "please tell me the reference of #coursename",
                                            "the teacher of #coursename is good", "when can i chiose the #coursename",
                                            "is #coursename on offer", "is #coursename a night school course",
                                            "tell me how many people in #coursename",
                                            "how many student enrol in #coursename",
                                            "I think the #coursename is a greate course"]  # unitCode
        """
        #entity
        self.dict= csv2dictionary(constants.entiry_dict_path)
        self.entity_dict = {}
        for key, value in self.dict.items():
            #if value=="unitname":
                #self.entity_dict[key]=value
            if value=="unitname":
                self.entity_dict[key]=value


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


    def fill_slot(self):
        result=[]
        dict_user = self.entity_dict
        value_list =list(dict_user.values())
        name_list = list(dict_user.keys())
        for item in name_list:
            template = NER.find_template_by_one(self, value_list[0]).split(" ")
            #print(template)
            if template != None:
                for slot in range(len(template)):
                    #print(template[slot])
                    if template[slot].__contains__("#"):
                        if template[slot].split("#")[-1] == value_list[0]:
                            #print(value_list[0])
                            template[slot] = item
                            re = ' '.join(template)
                            #print(re)
                            result.append(re)
        return result,name_list

    def final_raw_data(self,result,name_list):

        rawquestion=[]

        for i in range(len(result)):
            question = result[i]
            entitystr = name_list[i]
            begin = question.find(entitystr)
            #print(result[i])
            #sentence.append(result[i])
            #print(begin)
            #start.append(begin)
            #print(begin+len(entitystr))
            #end.append(begin+len(entitystr))
            collect =(begin,begin+len(entitystr),"unitname")
            dict2={"entities": [collect]}
            collect2 = (result[i],dict2)
            rawquestion.append(collect2)

        return rawquestion


    def training(self,model=None, output_dir=None, n_iter=100):

        rawquestion, coursename =  NER.fill_slot(self)
        TRAIN_DATA =  NER.final_raw_data(self,rawquestion, coursename)
        if model is not None:
            nlp = spacy.load(model)  # load existing spaCy model
            #print("Loaded model '%s'" % model)
        else:
            nlp = spacy.blank("en")  # create blank Language class
            #print("Created blank 'en' model")

        # create the built-in pipeline components and add them to the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if "ner" not in nlp.pipe_names:
            ner = nlp.create_pipe("ner")
            nlp.add_pipe(ner, last=True)
        # otherwise, get it so we can add labels
        else:
            ner = nlp.get_pipe("ner")

        # add labels
        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        # get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
        with nlp.disable_pipes(*other_pipes):  # only train NER
            # reset and initialize the weights randomly – but only if we're
            # training a new model
            if model is None:
                nlp.begin_training()
            for itn in range(n_iter):
                random.shuffle(TRAIN_DATA)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.5,  # dropout - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses)
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            nlp.to_disk(output_dir)
            #print("Saved model to", output_dir)

    def predict(self,output_dir=None,sentence= None):
        #print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc = nlp2(sentence)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        item_list =[(ent.text, ent.label_) for ent in doc.ents]
        #print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
        return NER.nermatching(self,sentence,item_list)

    def nermatching(self,sentence,item_List):
        sentence = sentence.lower()
        sentence_list = sentence.split(' ')
        sentence_slot = []

        for item in sentence_list:
            sentence_slot.append('O')

        for value,key in item_List:#machine learning #course
            num = sentence.find(value)
            #print(num)
            if num != -1:
                # print("y")
                start = 0
                for i in range(len(sentence_list)):
                    for iter in value.split(' '):
                        # print(sentence_list[i])
                        if sentence_list[i].__contains__(iter):
                            if sentence_list[i].__contains__(value.split(' ')[0]):
                                sentence_slot[i] = "B-" + key
                                start = 1
                            elif start ==1:
                                sentence_slot[i] = "I-" + key

        return sentence_slot


def test():
    ner_question = NER()

    ner_question.training(output_dir=constants.ner_model_path, n_iter=200)

    slot = ner_question.predict(output_dir=constants.ner_model_path, sentence=("the algorithm of machine algorithm"))
    print(slot)

#test()









