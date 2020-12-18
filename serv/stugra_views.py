from aiohttp import web
from .config import db_block, web_routes, render_html

@web_routes.get("/stugra")
async def view_list_stugra(request):
    with db_block() as db:

        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)

        

        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE g.stu_sn=101
        ORDER BY stu_sn, cou_sn;
        """)

        items = list(db)

    return render_html(request, 'stugra_list.html',
                       students=students,
                       items=items)