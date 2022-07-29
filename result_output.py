from pathlib import Path
import pathlib
import json
import time
import logging
import os

class ResultOutput:
    index=-1
    
    pat = pathlib.Path(__file__).parent.resolve()
    result_resource=open(str(pat)+"/resultTemplate.json")
    output=json.load(result_resource)
    result_resource.close()
    testcases=[]
    testcase_method=""
    #current_testcase_method=""
    summary= {
        "totalTests": 0,
        "Passed": 0,
        "Failed": 0,
        "Errored": 0,
        "eval":1
    }
    eval_message={}
    #index =0
    def __init__(self,args):
        # logging.info("step 1")
        # print("entered init block")
        time.sleep(1)
        try:
            #logging.info("step 2")
            logging.info("Opening file resultTemplate.json")
            result_resource=open(str(os.path.dirname(os.path.realpath(__file__)).replace('\\','/'))+"/resultTemplate.json")
            logging.info("opening file resultTemplate.json complete")
            logging.info("loading contents of resultTemplate.json")
            self.output=json.load(result_resource)
            #logging.info("step 3")
            logging.info("loaded contents of resultTemplate.json")
            result_resource.close()
            logging.info("closed file resultTemplate.json")
            #logging.info("step 4")
        except Exception as e:
            logging.info(str(e))   

        # try:
        #     json.loads(args)
        # except Exception as e:
        #     logging.info(str(e))
        #     logging.info("Malformed json input argumnets")            
        
        try: 
            if "token" in json.loads(args).keys():
            #logging.info("step 5")
#                 print(json.loads(args).keys())
                self.output["context"]["token"]=json.loads(args)['token']
                #logging.info("step 6")
            else:
            #logging.info("step 7")
                self.output["context"]["args"]=json.loads(args)
                #logging.info("step 8")
        except Exception as e:
            logging.info(str(e))
            logging.info("Malformed json input argumnets") 

        #method_list = [attribute for attribute in dir(class_object) if callable(getattr(class_object, attribute)) and attribute.startswith('testcase') is True]

        #self.testcases=testcase_list
        #logging.info("step 11")

    def update_pre_result(self,testcase_method,description="",expected=""):
        #print("self.testcase_method",self.testcase_method)
        #print("testcase_method",testcase_method)
        self.current_testcase_method=testcase_method
        template={"index":0,
            "testCase": "",
            "expected": "",
            "actual": "",
            "status": "",
            "comments": "",
            "ref": ""
            }
        if self.testcase_method != testcase_method:
            self.index+=1
            self.testcase_method=testcase_method
            template["index"]=self.index
            template["testCase"]="{{"+str(testcase_method)+"_description"+"}}"
            template["expected"]="{{"+str(testcase_method)+"_expected"+"}}"
            template["actual"]="{{"+str(testcase_method)+"_actual"+"}}"
            template["status"]=0
            template["comments"]="{{"+str(testcase_method)+"_comments"+"}}"
            template["ref"]="{{"+str(testcase_method)+"_ref"+"}}"
            self.testcases.append(template)
            self.testcases[self.index]["testCase"]=description
            self.testcases[self.index]["expected"]=expected
            self.summary["totalTests"]+=1
            

    def update_result(self,result,expected=None,actual=None,comment=None,ref=None):
        if actual !=None:
            self.testcases[self.index]["expected"]=expected 
        if comment !=None:
            self.testcases[self.index]["comments"]=comment
        if actual !=None:
            self.testcases[self.index]["actual"]=actual 
        if ref !=None:
            self.testcases[self.index]["ref"]=ref        
        self.testcases[self.index]["status"]=result

        if result == 1:
            self.summary["Passed"]+=1
            #self.summary["totalTests"]+=1
        elif result == 0:
            self.summary["Failed"]+=1
            #self.summary["totalTests"]+=1
        elif result == -1:
            self.summary["Errored"]+=1
            self.summary["eval"]=0
            #self.summary["totalTests"]+=1
        #print(self.testcases)
        return 

    def result_final(self):
        self.output["testCases"]=self.testcases
        self.output["summary"]["totalTests"]=self.summary["totalTests"]
        self.output["summary"]["Passed"]=self.summary["Passed"]
        self.output["summary"]["Failed"]=self.summary["Failed"]
        self.output["summary"]["Errored"]=self.summary["Errored"]
        self.output["evaluation"]["status"]=self.summary["eval"]
        self.output["evaluation"]["message"]=self.eval_message
        return self.output

