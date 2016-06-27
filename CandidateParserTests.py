import unittest
import csv
import StringIO
from CandidateParser import CandidateParser


class CandidateParserTests(unittest.TestCase):

    def testStageConfigParser(self):
        header = "Stage,Bucket\n"
        f = StringIO.StringIO(header + "1. do something,stage_1\n" \
                                    + "1 - do something,stage_1\n" \
                                    + "2 - something else,stage_2\n"\
                                    + "2:something else,stage_2\n" \
                                    + "nothing to match,\n")
        reader = csv.reader(f)
        p = CandidateParser()

        stage_config = p.parseStageConfig(reader)

        self.assertEqual(stage_config, {"stage_1": ["1. do something", "1 - do something"],
                                        "stage_2": ["2 - something else", "2:something else"]})

    def testSingleCandidateSingleStage(self):

        header = "Candidate ID,Candidate Name,Candidate Email,Candidate Phone,Opening ID,Opening,Stage,Decision Status," \
             + "Decision Reason,Reason Description,Person who changed the stage,Date of change,Stage Coordinator\n"

        f = StringIO.StringIO(header + "785646,Ale M,ale.m@gmail.com,0405100000,LBR80355,"
                              + "Consulting Business Analyst (Consultant/Senior/Lead/Principal levels),"
                              + "4a. Informal Chat,In Process,,,Mel B,2016-03-29,Tom J\n")

        reader = csv.reader(f)
        p = CandidateParser()

        data = p.parseReaderStages(reader)

        self.assertEqual(data["785646"], {"name":"Ale M", "email":"ale.m@gmail.com",
                                          "phone":"0405100000",
                                          "opening":"Consulting Business Analyst (Consultant/Senior/Lead/Principal levels)",
                  "stages":[{"stage":"4a. Informal Chat", "decision-status": "In Process",
                             "change-person": "Mel B", "change-date":"2016-03-29", "stage-coordinator":"Tom J"}]})

    def testSingleCandidateThreeStages(self):

        self.maxDiff = None

        header = "Candidate ID,Candidate Name,Candidate Email,Candidate Phone,Opening ID,Opening,Stage,Decision Status," \
             + "Decision Reason,Reason Description,Person who changed the stage,Date of change,Stage Coordinator\n"

        f = StringIO.StringIO(header + "785646,Ale M,ale.m@gmail.com,0405100000,LBR80355,"
                              + "Consulting Business Analyst (Consultant/Senior/Lead/Principal levels),"
                              + "4a. Informal Chat,In Process,,,Mel B,2016-03-29,Tom J\n"

                              + "785646,Ale M,ale.m@gmail.com,0405100000,LBR80355,"
                              + "Consulting Business Analyst (Consultant/Senior/Lead/Principal levels),"
                              + "5. Formal Chat,In Process,,,Diane Cotterill,2016-04-10,Tom J\n"

                              + "785646,Ale M,ale.m@gmail.com,0405100000,LBR80355,"
                              + "Consulting Business Analyst (Consultant/Senior/Lead/Principal levels),"
                              + "6. Offer,Hired,,,Mel B,2016-05-01,Tom J\n")

        reader = csv.reader(f)
        p = CandidateParser()

        data = p.parseReaderStages(reader)

        self.assertEqual(data["785646"], {"name":"Ale M", "email":"ale.m@gmail.com",
                                          "phone":"0405100000",
                                          "opening":"Consulting Business Analyst (Consultant/Senior/Lead/Principal levels)",
                  "stages":[{"stage":"4a. Informal Chat", "decision-status": "In Process",
                             "change-person": "Mel B", "change-date":"2016-03-29", "stage-coordinator":"Tom J"},
                            {"stage":"5. Formal Chat", "decision-status": "In Process",
                             "change-person": "Diane Cotterill", "change-date":"2016-04-10", "stage-coordinator":"Tom J"},
                            {"stage":"6. Offer", "decision-status": "Hired",
                             "change-person": "Mel B", "change-date":"2016-05-01", "stage-coordinator":"Tom J"}]})

def main():

    unittest.main()

if __name__ == '__main__':
    main()