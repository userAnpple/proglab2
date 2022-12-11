from spyre import server

import pandas as pd

import glob


class VHI_App(server.App):
    title = "Vegetation Health Index"
    
    # define input interface
    inputs = [{     "type":'dropdown',
                    "label": 'Region',
                    "options" : [ {"label": "Cherkasy", "value": "1"},
                                  {"label": "Chernihiv", "value": "2"},
                                  {"label": "Chernivtsi", "value": "3"},
                                  {"label": "Crimea", "value": "4"},
                                  {"label": "Dnipropetrovs`k", "value": "5"},
                                  {"label": "Donets`k", "value": "6"},
                                  {"label": "Ivano-Frankivs`k", "value": "7"},
                                  {"label": "Kharkiv", "value": "8"},
                                  {"label": "Kherson", "value": "9"},
                                  {"label": "Khmel`nyts`kyy", "value": "10"},
                                  {"label": "Kiev", "value": "11"},
                                  {"label": "Kiev City", "value": "12"},
                                  {"label": "Kirovohrad", "value": "13"},
                                  {"label": "Luhans`k", "value": "14"},
                                  {"label": "L`viv", "value": "15"},
                                  {"label": "Mykolaiv", "value": "16"},
                                  {"label": "Odessa", "value": "17"},
                                  {"label": "Poltava", "value": "18"},
                                  {"label": "Rivne", "value": "19"},
                                  {"label": "Sevastopol`", "value": "20"},
                                  {"label": "Sumy", "value": "21"},
                                  {"label": "Ternopil`", "value": "22"},
                                  {"label": "Transcarpatl", "value": "23"},
                                  {"label": "Vinnytsa", "value": "24"},
                                  {"label": "Volyn", "value": "25"},
                                  {"label": "Zaporizhzhya", "value": "26"},
                                  {"label": "Zhytomyr", "value": "27"}],
                    "key": "region",
                    "action_id": "update_data"},
              {     "type":"dropdown",
                    "label": "VCI/TCI/VHI",
                    "options" : [ {"label": "VCI", "value": "VCI"},
                                  {"label": "TCI", "value": "TCI"},
                                  {"label": "VHI", "value": "VHI"}],
                    "key": "series",
                    "action_id" : "update_data"},
              {     "type": 'text',
                    "label": 'Year',
                    "value" : "1982",
                    "key": 'year',
                    "action_id" : "update_data" },
              {     "type":'slider',
                    "label": 'First week',
                    "key": 'week1',
                    "value" : 1,
                    "min" : 1,
                    "max" : 52,
                    "action_id" : "update_data"},
              {     "type":'slider',
                    "label": 'Last week',
                    "key": 'week2',
                    "value" : 52,
                    "min" : 1,
                    "max" : 52,
                    "action_id" : "update_data"}]
    
    # define controls
    controls = [{    "type" : "hidden",
                     "id" : "update_data"}]

    # define tabs
    tabs = ["Plot", "Table"]
    
    # define output interface
    outputs = [{    "type": "html",
                    "id": "table_validity_of_input",
                    "control_id" : "update_data",
                    "tab": "Table"},
               {    "type": "html",
                    "id": "plot_validity_of_input",
                    "control_id" : "update_data",
                    "tab": "Plot"},
               {    "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
               {    "type" : "table",
                    "id" : "table",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]

    def table_validity_of_input(self, params):
        year = int(params["year"]) # setting up year
        week1 = int(params["week1"]) # setting up first week
        week2 = int(params["week2"]) # setting up last week
        # check validity of data for table
        if(year < 1982 or year > 2022 or week1 > week2):
            return "Invalid input."
        else:
            return "Valid input."
        
    def plot_validity_of_input(self, params):
        year = int(params["year"]) # setting up year
        week1 = int(params["week1"]) # setting up first week
        week2 = int(params["week2"]) # setting up last week
        # check validity of data for table
        if(year < 1982 or year > 2022 or week1 > week2):
            return "Invalid input."
        else:
            return "Valid input"
        
    def table(self, params):
        # get data
        region = params["region"] # setting up a region
        series = params["series"] # setting up a type of series
        year = int(params["year"]) # setting up year
        week1 = int(params["week1"]) # setting up first week
        week2 = int(params["week2"]) # setting up last week
        headers = ["year", "week", "SMN", "SMT", "VCI", "TCI", "VHI"]
        path = glob.glob("{}{}_{}_*.csv".format("./", "dataVHI", region))
        df = pd.read_csv(path[-1], 
                         header = None, 
                         names = headers, 
                         index_col = False)
        # filter through data 
        df = df[df["year"] == year]
        df = df[(df["week"] >= week1) & (df["week"] <= week2)]
        df = df[[series]]
        
        return df
    
    def plot(self, params):
        province = {"1": "Cherkasy", "2": "Chernihiv", "3": "Chernivtsi", "4": "Crimea", "5": "Dnipropetrovs`k",
                    "6": "Donets`k", "7": "Ivano-Frankivs`k", "8": "Kharkiv", "9": "Kherson", "10": "Khmel`nyts`kyy",
                    "11": "Kiev", "12": "Kiev City", "13": "Kirovohrad", "14": "Luhans`k", "15": "L`viv", "16": "Mykolaiv",
                    "17": "Odessa", "18": "Poltava", "19": "Rivne", '20': "Sevastopol`", "21": "Sumy", "22": "Ternopil`",
                    "23": "Transcarpatl", "24": "Vinnytsa", "25": "Volyn", "26": "Zaporizhzhya", "27": "Zhytomyr"}
        # get data
        region = params["region"] # setting up a region
        series = params["series"] # setting up a type of series
        year = int(params["year"]) # setting up year
        week1 = int(params["week1"]) # setting up first week
        week2 = int(params["week2"]) # setting up last week
        headers = ["year", "week", "SMN", "SMT", "VCI", "TCI", "VHI"]
        path = glob.glob("{}{}_{}_*.csv".format("./", "dataVHI", region))
        df = pd.read_csv(path[-1], 
                         header = None, 
                         names = headers, 
                         index_col = False)
        # filter through data
        df = df[df["year"] == year]
        df = df[(df["week"] >= week1) & (df["week"] <= week2)]
        df = df[["week", series]]
        # plot data
        df = df.set_index("week")
        plt_obj = df.plot()
        plt_obj.set_ylabel(series)
        plt_obj.set_xlabel("week")
        plt_obj.set_title("{} {} {}".format(series, province[region], year))
        fig = plt_obj.get_figure()
        
        return fig

app = VHI_App()
app.launch(port=9093)