import pymongo

if __name__ == "__main__":
    con = pymongo.MongoClient("192.168.68.11", 20000)
    col1 = con.divorceCase3.searchPerformValidate
    col2 = con.divorceCase3.searchPerform
    col3 = con.divorceCase3.searchPerformValidateEvaluate
    col4 = con.divorceCase3.searchPerformEvaluate



    cur2 = col3.find(no_cursor_timeout=True)
    for item in cur2:
        if item["name"] == None:
            continue

        item["tag"] = "4"
        col4.insert(item)

    cur2.close()