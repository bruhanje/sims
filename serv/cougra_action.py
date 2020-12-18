from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/cougra/query')
async def action_cougra_query(request):
    params = await request.post()
    stu_sn = params.get("stu_sn")
    cou_sn = params.get("cou_sn")
    term = params.get("term")

    '''if stu_sn is None or cou_sn is None or term is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, term must be required")'''

    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        term = '第一学期'
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    try:
        with db_block() as db:
            db.execute("""
            INSERT INTO student_course (stu_sn, cou_sn, term) 
            VALUES ( %(stu_sn)s, %(cou_sn)s, %(term)s)
            """, dict(stu_sn=stu_sn, cou_sn=cou_sn, term=term))
    except psycopg2.errors.UniqueViolation:
        query = urlencode({
            "message": "已经添加该学生的课程学期",
            "return": "/choose"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此学生或课程: {ex}")

    return web.HTTPFound(location="/choose")