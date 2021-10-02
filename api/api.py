from typing import Optional
from fastapi import FastAPI
import uvicorn

api = FastAPI()


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


if __name__ == '__main__':
    uvicorn.run(api, port=8000, host="0.0.0.0")
