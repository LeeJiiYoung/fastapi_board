from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class PostCreate(BaseModel):
    title: str
    content: str

posts: dict[int, dict] = {}
next_id = 1

# 등록
@app.post("/posts")
def create_post(req: PostCreate):
    global next_id
    post = {"id": next_id, **req.model_dump()}
    posts[next_id] = post
    next_id += 1
    return post

# 리스트 조회
@app.get("/posts")
def list_posts():
    return list(posts.values())

# 단건 조회
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="게시글이 없습니다")
    return posts[post_id]

# 수정
@app.put("/posts/{post_id}")
def update_post(post_id: int, req: PostCreate):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="게시글이 없습니다")
    posts[post_id].update(req.model_dump())
    return posts[post_id]

# 삭제
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="게시글이 없습니다")
    del posts[post_id]
    return {"message": "삭제되었습니다"}

@app.get("/board", response_class=HTMLResponse)
def board_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="board.html",
        context={"posts": list(posts.values())},
    )

@app.post("/board")
def board_submit(title: str = Form(), content: str = Form()):
    create_post(PostCreate(title=title, content=content))
    return RedirectResponse("/board", status_code=303)

@app.get("/")
def hello():
    return {"Hello": "hi hi hi"}