from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/choose/add')
async def action_choose_add(request):
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


@web_routes.post('/action/choose/edit/{stu_sn}/{cou_sn}')
async def edit_choose_action(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    params = await request.post()
    term = params.get("term")

    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        term = '第一学期'
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    with db_block() as db:
        db.execute("""
        UPDATE student_course SET term=%(term)s
        WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn, term=term))

    return web.HTTPFound(location="/choose")


@web_routes.post('/action/choose/delete/{stu_sn}/{cou_sn}')
def delete_choose_action(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        DELETE FROM student_course
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

    return web.HTTPFound(location="/choose")
