import os
from pathlib import Path
import json
import pandas as pd

#function returns the path of the interested file type
def search_file():
    def file_path(name_prefix):
        #gets the current working directory path
        current_path =os.walk(os.getcwd()) 
        #all the json type files with interested name_prefix are appended to the list 
        file_type = [os.path.normpath(os.path.join(root,file)) for root, dirs, files in current_path for file in files if file.endswith('.json') and file.startswith(name_prefix)]
        #test whether the list is not empty, if empty close the function
        if file_type:
        #check whether the file exists in the list through its index
            return Path(file_type[0])
        else:
            return None
    #return the path of the interested file
    return file_path

#load the json file type into a variable
def load_file(f_path):
    with open(f_path,encoding='utf-8') as f:
        data = json.load(f)
        return data

#parse the dataframe through the json's interested key
def parse_dataframe(json_data,interested_key):
    try:
        #json data with interested key parse into the dataframe
        return pd.DataFrame.from_dict(json_data[interested_key])
    except KeyError as err:
        print(f'Interested key not found',err)
        return None

#check whether the interested columns exists in the parsed dataframe
def search_columns(col_list,df):
        interested_col = []
        missing_col = []
        for col in col_list:
            #interested columns gets appended to the list
            try:
                df[col]
                interested_col.append(col)
            #missing columns are contained in the list
            except KeyError:
                missing_col.append(col)
        if not missing_col:
            #return the dataframe with only interested columns
            return pd.DataFrame(df,columns=interested_col)
        else:
            print(f'column/columns missing {missing_col}')
            return None 
            
 
 #transform/clean the dataframe as required
def transform_df(df):
    interested_headers = {'id':'ProductID',
               'title':'ProductName',
               'category':'Category',
               'price':'Price'
                }
    return df.rename(columns=interested_headers,errors='raise')

#stage the data at a given path
def stage_data(df):
    file_dir  = os.path.dirname(os.path.realpath(__file__))
    #set the interested path
    interested_path = Path(file_dir) / "staged_data"
    #check whether interested path and file exist, if not exists create path/file.
    interested_path.mkdir(parents=True,exist_ok=True)
    staged_path = interested_path / "products.json"
    #write the df to json format'
    df.to_json(staged_path,orient='records')
    return staged_path


interested_columns = ['id','title','category','price']
 
# now call the functions for staging the data
if __name__ == "__main__":
    file_search = search_file()
    f_path = file_search('product')
    if f_path:
        data = load_file(f_path)        
        if data is not None:
            df = parse_dataframe(data,'products')
            if df is not None:
                interested_df = search_columns(interested_columns,df)
                if interested_df is not None:
                    transformed_df = transform_df(interested_df)
                    if not transformed_df.empty:
                        staged_path = stage_data(transformed_df)
                        print('data staged success')
                        
