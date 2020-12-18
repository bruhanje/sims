DELETE FROM course_grade;
DELETE FROM course;
DELETE FROM student;

INSERT INTO student (sn, no, name,gender)  VALUES
    (101, 'S001',  '张三','男'),
    (102, 'S002',  '李四','女'), 
    (103, 'S003',  '王五','男'),
    (104, 'S004',  '马六','女');

INSERT INTO course (sn, no, name,place,time)  VALUES 
    (101, 'C01',  '高数','一公教','一学期'), 
    (102, 'C02',  '外语','二公教','二学期'),
    (103, 'C03',  '线代','一公教','二学期');


INSERT INTO course_grade (stu_sn, cou_sn, grade)  VALUES 
    (101, 101,  91), 
    (102, 101,  89),
    (103, 101,  90),
    (101, 102,  89);

INSERT INTO student_course(stu_sn,cou_sn,term) VALUES
    (101,101,'第一学期'),
    (102,102,'第二学期'),
    (103,101,'第三学期'),
    (101,102,'第四学期');

    