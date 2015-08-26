import pymongo

if __name__ == '__main__':
    connection = pymongo.connection.Connection()
    db = connection.dsspp

    rows = [
        {'description':'description', 'label':'Consumer_Electronics', 'number':16, 'title':'Consumer Electronics', 'visible':True},
        {'description':'description', 'label':'Food_and_Drink', 'number':20, 'title':'Food and Drink', 'visible':True},
        {'description':'description', 'label':'Environment', 'number':2, 'title':'Environment', 'visible':True},
        {'description':'description', 'label':'News_and_Events', 'number':15, 'title':'News and Events', 'visible':True},
        {'description':'description', 'label':'nodomain', 'number':0, 'title':'No Domain', 'visible':True},
        {'description':'description', 'label':'Cars_and_Transportation', 'number':5, 'title':'Cars and Transportation', 'visible':True},
        {'description':'description', 'label':'Science_and_Mathematics', 'number':8, 'title':'Science and Mathematics', 'visible':True},
        {'description':'description', 'label':'Social_Science', 'number':12, 'title':'Social Science', 'visible':True},
        {'description':'description', 'label':'Games_and_Recreation', 'number':18, 'title':'Games and Recreation', 'visible':True},
        {'description':'description', 'label':'Health', 'number':3, 'title':'Health', 'visible':True},
        {'description':'description', 'label':'Computers_and_Internet', 'number':7, 'title':'Computers and Internet', 'visible':True},
        {'description':'description', 'label':'Society_and_Culture', 'number':11, 'title':'Society and Culture', 'visible':True},
        {'description':'description', 'label':'Sports', 'number':2, 'title':'Sports', 'visible':True},
        {'description':'description', 'label':'Local_Business', 'number':6, 'title':'Local Business', 'visible':True},
        {'description':'description', 'label':'Beauty_and_Style', 'number':10, 'title':'Beauty and Style', 'visible':True},
        {'description':'description', 'label':'Travel', 'number':14, 'title':'Travel', 'visible':True},
        {'description':'description', 'label':'common', 'number':1, 'title':'common terms', 'visible':True},
        {'description':'description', 'label':'Pets', 'number':4, 'title':'Pets', 'visible':True},
        {'description':'description', 'label':'Family_and_Relationships', 'number':17, 'title':'Family and Relationships', 'visible':True},
        {'description':'description', 'label':'Home_and_Garden', 'number':2, 'title':'Home and Garden', 'visible':True},
        {'description':'description', 'label':'combineall', 'number':1, 'title':'Combine All Domains', 'visible':True},
        {'description':'description', 'label':'Arts_and_Humanities', 'number':13, 'title':'Arts and Humanities', 'visible':True},
        {'description':'description', 'label':'Politics', 'number':19, 'title':'Politics', 'visible':True},
    ]

    for row in rows:
        db.domain_list.insert(row)