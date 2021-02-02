import sqlite3
import pandas as pd

#################################################################################################
connection = sqlite3.connect("database_arnab/test.sqlite3")
cursor = connection.cursor()
#################################################################################################


def getTableNames(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor.fetchall()

def getAttributes(cursor, table_name):
    query = "select * from {} limit 1".format(table_name)
    cursor.execute(query)
    attributes = []
    for row in cursor.description:
        attributes.append(row[0])
    return attributes

def queryFromDBinJSON(cursor, query):
    cursor.execute(query)
    attributes = []
    for row in cursor.description:
        attributes.append(row[0])
    # print(attributes)

    row_set = cursor.fetchall()
    json_arr = []
    for row in row_set:
        val = {}
        for i in range(len(row)):
            val[attributes[i]] = row[i]
        json_arr.append(val)
    
    return json_arr

IMAGE_ROOT = "images/caption_site/"
def insertImage(cursor, connection, human_annotation, image_name):
    query = "insert into caption_site_image(human_annotation, image) "
    query += "values(\"{}\", \"{}\");".format(human_annotation, IMAGE_ROOT+image_name)
    # print(query)
    cursor.execute(query)
    connection.commit()
    print(" >>>>>> inserted image: {}, {}".format(human_annotation, image_name))


def insertCaption(cursor, connection, caption_text, caption_model_id, image_id):
    query = "insert into caption_site_caption(caption_text, caption_model_id, image_id) "
    query += "values(\"{}\", \"{}\", \"{}\");".format(caption_text, caption_model_id, image_id)
    cursor.execute(query)
    connection.commit()
    print(" >>>>>> inserted caption: {}, {}, {}".format(caption_text, caption_model_id, image_id))


models = queryFromDBinJSON(cursor, "select * from caption_site_captionmodel")
def getModelId(model_name):
    for model in models:
        if(model["model_name"] == model_name):
            return model["id"]
    return None

def getImageIdusingImageName(cursor, image_name):
    image_path = IMAGE_ROOT + image_name
    query = "select * from caption_site_image where image = \"{}\";".format(image_path)
    result = queryFromDBinJSON(cursor, query)
    if(len(result) == 0):
        print("image not found")
        return -1
    return result[0]['id']

def refreshTable(cursor, connection, table_name):
    query = "delete from "+table_name+";"
    cursor.execute(query)
    connection.commit()

# table_names = getTableNames(cursor)
# print(table_names)

# json_arr = queryFromDBinJSON(cursor, "select * from caption_site_caption;")
# for json in json_arr:
#     print(json)

# image_name = "1258913059_07c613f7ff.png"	
# human_annotation = "Three people sit at a picnic table outside of a building painted like a union jack"	

# image_name = "1258913059_07c613f7ff.png"	
# print(getImageIdusingImageName(cursor, image_name))




#################################################################################################
df = pd.read_csv("database_arnab/Models and Captions - Sheet1.csv")
hd = df.head()
#################################################################################################
# refreshTable(cursor, connection, "caption_site_presetopinionoption")
# refreshTable(cursor, connection, "caption_site_caption")

attr = []
for val in hd:
    attr.append(val)


for index, row in df.iterrows():
    image_name = row["image_name"]
    human_annotation = row["human_annotation"]
    print(image_name, human_annotation)

    if(getImageIdusingImageName(cursor, image_name) == -1):
        insertImage(cursor, connection, human_annotation, image_name)
    else:
        print("image is already in the database")
    image_id = getImageIdusingImageName(cursor, image_name)

    for i in range(2, len(attr)):
        val = attr[i]
        caption_text = row[val]
        caption_model_id = getModelId(val)
        print(val, caption_model_id, ": ", caption_text, "<{}>".format(image_id))

        insertCaption(cursor, connection, caption_text, caption_model_id, image_id)

    print()

