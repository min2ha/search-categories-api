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
    return {"Search result": "List of Categories & Sub-Categories"}



conn = pysolr.Solr('http://192.168.1.160:8984/solr/collections', search_handler='/select', use_qt_param=False)
result = conn.search('type:collection AND collectionAreaId:[* TO *]', **{
    'indent': 'true',
    'rows':'1000',
    'group.field':'collectionAreaId',
    'group.limit':'1000',
    'group':'true'
})

top_category_list = []

for r in result.raw_response['grouped']['collectionAreaId']['groups']:
    top_category_list.append(r['groupValue'])

@api.get("/categories/")
async def read_categories():
    top_categories = {"categories": top_category_list}
    return top_categories


if __name__ == '__main__':
    uvicorn.run(api, port=8000, host="0.0.0.0")
