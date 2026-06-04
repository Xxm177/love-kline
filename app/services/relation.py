def build_relation_index(messages):
     total=0
     result=[]
     for item in messages:
         total+=item["score"]
         result.append(
             {
                 "time":item["time"],
                 "index":total
             }
         )
     return result


