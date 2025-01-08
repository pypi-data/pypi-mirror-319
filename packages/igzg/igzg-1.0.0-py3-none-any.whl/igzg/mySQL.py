__version__ = '0.0.5'

def getInsertQuery(tableName:str, dataDict:dict, duplicateUpdate:bool=False, updateItems:list=[])->str:
    '''
    dataDict    = {'col1':'data1','col2':'data2'}
    updateItems = ['col1','col2']
    '''
    query = ''
    itemStr = ','.join(['`'+str(x)+'`' for x in list(dataDict.keys())])
    valueStr= ','.join(['Null' if x is None else "'"+str(x)+"'" for x in list(dataDict.values())])
    updateStr = "ON DUPLICATE KEY UPDATE " + ','.join(["`"+str(x)+"`='"+str(dataDict[x])+"'" for x in updateItems]) if duplicateUpdate else ''
    
    query = rf"""INSERT INTO `{tableName}` ({itemStr}) VALUES ({valueStr}) {updateStr};"""

    return query


def getSelectQuery(tableName:str,  items:list=[], where:list=[], sort:dict={}, distinct:bool=False)->str:
    '''
    items = ['col1', 'col2']
    where = ["`col1` = 'apple'", "`col2` < 13"]
    sort  = {"col1":"ASC", "col1":"DESC"} # value - ASC/DESC
    '''
    query = ''
    itemStr = ','.join(['`'+str(x)+'`' for x in items]) if items != [] else '*'
    whereStr = ("WHERE " + 'AND'.join(['('+str(x)+')' for x in where])) if where != [] else ''
    sortStr = ("ORDER BY " + ','.join(["`"+str(x)+"` "+str(sort[x]).upper()+"" for x in sort.keys()])) if sort != {} else ''
    distinctStr = "DISTINCT" if distinct else ''

    query = rf"""SELECT {distinctStr} {itemStr} FROM `{tableName}` {whereStr} {sortStr};"""

    return query


def getTruncateQuery(tableName:str)->str:
    query = f"TRUNCATE TABLE {tableName};"
    return query


def getDeleteQuery(tableName:str, where:list=[])->str:
    '''
    where = ["`col1` = 'apple'", "`col2` < 13"]
    '''

    query = ''
    whereStr = ("WHERE " + 'AND'.join(['('+str(x)+')' for x in where])) if where != [] else ''

    query = rf"""DELETE FROM `{tableName}` {whereStr};"""

    return query

def getUpdateQuery(tableName:str, dataDict:dict, where:list=[])->str:
    '''
    where = ["`col1` = 'apple'", "`col2` < 13"]
    dataDict    = {'col1':'data1','col2':'data2'}
    '''
    query = ''
    whereStr = ("WHERE " + 'AND'.join(['('+str(x)+')' for x in where])) if where != [] else ''
    setStr = "SET" + ','.join([f"`{x}` = '{dataDict[x]}'" for x in dataDict])

    query = rf"""UPDATE `{tableName}` {setStr} {whereStr};"""

    return query

if __name__ == "__main__":
    print(getDeleteQuery('powder',where=["seq = 1", "name_ko = '코발트'"]))