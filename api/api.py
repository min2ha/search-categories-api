from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI
import pysolr
import uvicorn

api = FastAPI()

class Category(BaseModel):

    collectionAreaId: int
    name = 'Collection no X'
    description = 'Collection no X'
    id : int
    type : str

class Collection(BaseModel):
    id : int
    type : str
    name : str
    description : str
    collectionAreaId : int # covers and Categories - matters query grouping ONLY 

class CollectionList(BaseModel):
    __root__: List[Collection]



@api.get("/")
def read_root():
    return {"Hello": "Search Categories API"}


@api.get("/categories/{category_id}")
def read_category(category_id: int, q: Optional[str] = None):
    return {"category_id": category_id, "q": q}


@api.route('/search', methods=['GET', 'POST'])
# @login_required
def search():
    # form = SearchForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #    return redirect((url_for('search_results', query=form.search.data)))  # or what you want
    # return render_template('search.html', form=form)
    print('Please wait while the program is loading...')
    return {"Search result": "List of Categories & Sub-Categories"}



conn = pysolr.Solr('http://192.168.1.160:38983/solr/collections', search_handler='/select', use_qt_param=False)
result = conn.search('*:*', **{
    
     # fl=collectionAreaId&
     # fq=collectionAreaId:[*%20TO%20*]-collectionAreaId:(2945)&
     # indent=on&
     # facet=true&
     # facet.limit=-1&
     # facet.pivot.mincount=1&
     # facet.pivot=collectionAreaId,id&
     # q=*:*&
     # wt=json
    
    

    'fl':'collectionAreaId',
    'fq':'collectionAreaId:[* TO *]-collectionAreaId:(2945)',

    'facet':'true',
    'facet.limit':'-1',
    'facet.pivot.mincount':'1',
    'facet.pivot':'collectionAreaId,id,description,name',

    'indent': 'true',

    'wt':'json'


})

print('SOLR Pivot data for Categories...')

# {'field': 'description', 'value': 'This collection was initiated in 2016 and ...
print(result.raw_response['facet_counts']['facet_pivot']['collectionAreaId,id,description,name'][1]['pivot'][0]['pivot'])

# JSON array - brackets
# 'pivot': [{'field': 'name', 'value': 'Online Enthusiast Communities in the UK'
# [{'field': 'name', 'value': 'Online Enthusiast Communities in the UK', 'count': 1}]
print(result.raw_response['facet_counts']['facet_pivot']['collectionAreaId,id,description,name'][1]['pivot'][0]['pivot'][0]['pivot'])

# not JSON array !!!!!!!! - no brackets
# {'field': 'name', 'value': 'Online Enthusiast Communities in the UK', 'count': 1}
print(result.raw_response['facet_counts']['facet_pivot']['collectionAreaId,id,description,name'][1]['pivot'][0]['pivot'][0]['pivot'][0])

# not JSON array ! - specific JSON  field value !!!!!!!!
# Online Enthusiast Communities in the UK
print(result.raw_response['facet_counts']['facet_pivot']['collectionAreaId,id,description,name'][1]['pivot'][0]['pivot'][0]['pivot'][0]['value'])


top_category_list = []

#for r in result.raw_response['grouped']['collectionAreaId']['groups']:
#    top_category_list.append(r['groupValue'])

@api.get("/categories/")
async def read_categories():
    print('Please wait while the program is loading...')
    top_categories = {"categories": top_category_list}
    return top_categories


if __name__ == '__main__':
    uvicorn.run(api, port=8000, host="0.0.0.0")
