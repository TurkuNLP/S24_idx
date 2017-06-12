#<text discussionarea="Yhteiskunta" subsections="Maailman menoa" cid="unspecified" deleted="False" views="10" datefrom="20160919" year="2016" title="Kyllä kai tuo ihan selvä tappo oli Asema-aukiolla" date="19.09.2016" anonnick="sjffksddsj" tid="14483456" dateto="20160919" time="19:13" comms="4" sect="Yhteiskunta" subsect="Maailman menoa" ssubsect="" sssubsect="" ssssubsect="" sssssubsect="" ssssssubsect="" urlboard="http://keskustelu.suomi24.fi/t/14483456" urlmsg="http://keskustelu.suomi24.fi/t/14483456">

import re
import sys
import pysolr

kv_re=re.compile('([a-z]+)="(.*?)"')
def key_is_val_into_dict(kvs):
    """kvs is a string which contains many instances of something="something" """
    result={}
    for k,v in kv_re.findall(kvs):
        result[k]=v
    return result

def posts(inp):
    for line in inp:
        line=line.strip()
        if not line:
            continue
        if line.startswith("<text "):
            #We have a new post starting
            post_data=key_is_val_into_dict(line)
            post_words=[]
            post_lemmas=[]
        elif line=="</text>":
            date="-".join(post_data["date"].split(".")[::-1])+"T"+post_data["time"]+":00Z"
            yield {"date":date,"text":" ".join(post_words),"lemma":" ".join(post_lemmas),"title":post_data["title"],"sect":post_data["sect"],"subsect":post_data["subsect"],"thread":post_data["tid"],"user":post_data["anonnick"]}
        else:
            columns=line.split("\t")
            if len(columns)==8:
                post_words.append(columns[0])
                post_lemmas.append(columns[2].replace("|",""))

solr=pysolr.Solr("http://127.0.0.1:8983/solr/s24")
solr.delete(q='*:*')
to_index=[]
counter=0
for pidx,post in enumerate(posts(sys.stdin)):
    post["id"]=pidx
    to_index.append(post)
    if len(to_index)>=10000:
        counter+=len(to_index)
        solr.add(to_index)
        to_index=[]
        print(counter)
        solr.commit()
        #if counter>50000:
        #    break
        
        
            
