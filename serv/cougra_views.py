from aiohttp import web
from .config import db_block, web_routes, render_html

@web_routes.get("/cougra")
async def view_list_cougra(request):
    with db_block() as db:

        db.execute("""
        SELECT sn AS cou_sn, name as cou_name FROM course ORDER BY name
        """)
        courses = list(db)

        

        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE g.cou_sn=101
        ORDER BY stu_sn, cou_sn;
        """)

        items = list(db)

    return render_html(request, 'cougra_list.html',
                       courses=courses,
                       items=items)


