import pandas as pd 



def pandas_to_highcharts(df):
    df.index = [t.value // 10 ** 6 for t in df.index]
    json_dict = {}
    for key, value in df.items():
        # print("main")
        json_dict["name"] = key
        data_list = []
        for i in range(len(value.index)):
            temp = [int(value.index[i]), float(value.values[i])]
            # print(value.index[0], " , ", value.values[0])
            data_list.append(temp)
        json_dict["data"] = data_list
    
    return [json_dict]