import csv
import collections

class CandidateParser:

    def parseReaderStages(self, reader):
        data = {}

        stages = {}
        decisions = {}

        for row in reader:
            stages[row[6]] = 1
            decisions[row[7]] = 1
            if not (row[6] == 'Make Offer' and row[7] == 'Declined Offer') \
                and not (row[6] == 'Case Study' and row[7] == 'Withdrawn') \
                and not (row[6] == 'Case Study' and row[7] == 'Rejected'):
                try:
                    candidate = data[row[0]]
                    candidate["stages"].append({"stage":row[6], "decision-status": row[7],
                                             "change-person": row[10], "change-date": row[11], "stage-coordinator": row[12]})
                except KeyError:
                    candidate = {"name": row[1], "email": row[2], "phone": row[3], "opening": row[5],
                                 "stages": [{"stage":row[6], "decision-status": row[7],
                                             "change-person": row[10], "change-date": row[11], "stage-coordinator": row[12]}]}
                    data[row[0]] = candidate

                # if row[11] == "":
                #     print row

                if row[6] == "Make Offer": print "Offer:" + row[1] + ": " + row[11]
                if row[6] == "Prepare Contract": print "Contract:" + row[1] + ": " + row[11]

        # print "Stages ---------"
        # orderedStages = collections.OrderedDict(sorted(stages.items()))
        # for key, stage in orderedStages.iteritems():
        #     print key
        # print "Decisions ------"
        # for key, decision in decisions.iteritems():
        #     print key
        return data


    def stage_count_per_month(self, data_per_month, key, stages, candidate, stage):
        count_per_month = data_per_month.setdefault(key, {})
        stage_description = stage["stage"]
        if (stage_description in stages):

            month = stage["change-date"][0:7]
            try:
                people = count_per_month[month]
            except KeyError:
                count_per_month[month] = []

            if candidate["name"] not in count_per_month[month]:
                count_per_month[month].append(candidate["name"])
        return data_per_month

    def generateReport(self, data_per_month):
        orderedOffers = collections.OrderedDict(sorted(data_per_month["case_studies"].items()))
        report = "month, phone_interviews, competency, case_studies, offers\n"
        for month, offerOwners in orderedOffers.iteritems():
            report = report + month + ", " \
                     + str(len(data_per_month["phone_interviews"].get(month, ""))) + ", " \
                     + str(len(data_per_month["competency"].get(month, ""))) + ", " \
                     + str(len(data_per_month["case_studies"].get(month, ""))) + ", " \
                     + str(len(data_per_month["offers"].get(month, ""))) + ", " \
                     + str(offerOwners) + "\n"

        print report
        return report

    def countStageOccurrencesByMonth(self, data, stage_config):
        data_per_month = {}
        for key, candidate in data.iteritems():
            for stage in candidate["stages"]:
                data_per_month = self.stage_count_per_month(
                    data_per_month, "phone_interviews", ["Phone Interview", "Phone screen",
                                                         "Phone or Video screen", "4. Telephonic Screening"]
                    , candidate, stage)

                data_per_month = self.stage_count_per_month(
                    data_per_month, "case_studies", ["Case Study"]
                    , candidate, stage)

                data_per_month = self.stage_count_per_month(
                    data_per_month, "offers", ["Make Offer", "11. Make offer", "Prepare Contract"]
                    , candidate, stage)

                data_per_month = self.stage_count_per_month(
                    data_per_month, "competency", ["1st Interview - CV, Cultural Fit & Aptitude",
                                                   "1st Interview- Background Interview",
                                                   "1st Interview-Aptitude&BA test",
                                                   "2nd Interview - Competency",
                                                   "2nd Interview- Competency Assessment",
                                                   "BG\CF Int",
                                                   "Background/Experience/Fit",
                                                   "Competency",
                                                   "Competency Assessment",
                                                   "Competency Interview & Aptitude Test",
                                                   "Competency\Background Int & Aptitude"]
                    , candidate, stage)
        return data_per_month

    def parseFileStages(self):

        data = {}
        stage_config = {}

        # with open('data/sample.csv', 'rUb') as csvFile:
        with open('data/data-20-06-2016.csv', 'rUb') as csvFile:
            reader = csv.reader(csvFile)
            data = self.parseReaderStages(reader)

        with open("data/stage-config.csv", 'rUb') as configFile:
            reader = csv.reader(configFile)
            stage_config = self.parseStageConfig(reader)

        stage_config = {}

        data_per_month = self.countStageOccurrencesByMonth(data, stage_config)

        return data_per_month

    def parseStageConfig(self, config_reader):
        next(config_reader, None)
        stage_config = {}
        for row in config_reader:
            try:
                stage_bucket = stage_config[row[1]]
            except KeyError:
                if row[1]:
                    stage_config[row[1]] = []
            if row[1]:
                stage_config[row[1]].append(row[0])

            # month = stage["change-date"][0:7]
            # try:
            #     people = count_per_month[month]
            # except KeyError:
            #     count_per_month[month] = []
            #
            # if candidate["name"] not in count_per_month[month]:
            #     count_per_month[month].append(candidate["name"])
            #


        return stage_config

def main():
    parser = CandidateParser()
    data_per_month = parser.parseFileStages()
    report = parser.generateReport(data_per_month)

    f = open("report.csv", "w")
    f.write(report)
    f.close()

if __name__ == '__main__':
    main()

