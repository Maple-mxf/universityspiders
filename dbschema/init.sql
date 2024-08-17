drop table school;
create table school
(
    id                       int(11) primary key auto_increment,
    zh_name                  varchar(64) not null,
    logo                     varchar(256),
    province                 varchar(64),
    city                     varchar(64),
    county                   varchar(64),
    address                  varchar(1024),
    edu_level                varchar(16) comment '教育层次，A代表本科 B代表专科',
    edu_category             varchar(16) comment '教育类别 A代表综合类 B代表理工类',
    edu_establish            varchar(16) comment '办学性质 A代表公办',
    official_website         varchar(2048) comment '学校官网,多个网站使用 , 分割',
    admissions_contact_phone varchar(2048) comment '招生电话 多个电话使用逗号分割',
    admissions_contact_email varchar(2048) comment '招生邮箱 多个邮箱使用逗号分割',
    introduction             text comment '学校介绍',
    doctoral_program_num     int(11) comment '博士点总数',
    master_program_num       int(11) comment '硕士点总数',
    arwu_ranking             int(11) comment '软科排名',
    aa_ranking               int(11) comment '校友会排名',
    usn_ranking              int(11) comment 'U.S. News世界大学排名',
    qs_ranking               int(11) comment 'QS排名'
) comment '学校基础信息';
drop table major;
create table major
(
    id              int(11) primary key auto_increment,
    zh_name         varchar(64) not null,
    code            varchar(64) comment '专业代码',
    edu_level       varchar(16) comment '教育层次，A代表本科 B代表专科',
    course_scopes    varchar(16) comment '专业领域 例如工学 艺术学',
    course_category varchar(16) comment '	学科类别： ',
    edu_duration      varchar(16) comment '学制',
    graduate        varchar(16) comment '授予学位',
    introduction    varchar(2048) comment '简介',
    school_id       int(11) comment '学校ID'
) comment '专业信息';
drop table admissions_plan;
create table admissions_plan
(
    id            int(11) primary key auto_increment,
    year          varchar(16),
    province      varchar(16),
    option3       varchar(16) comment '综合',
    option4       varchar(16) comment '普通批次。。。',
    major_zh_name varchar(64) comment '专业名称',
    plan_num      int(11) comment '计划招生人数',
    edu_dur       varchar(32) comment '学制',
    edu_fee       int(11) comment '学费',
    cond          float(10, 2) comment '选课要求',
    min_score     varchar(128) comment '最低分数',
    min_ranking   int(11) comment '最低位次'
);
drop table school_news;
create table school_news
(
    id           int(11) primary key auto_increment,
    publish_date date comment '发布日期',
    title        varchar(32) comment '标题',
    content      text comment '内容',
    school_id    int(11) comment '学校ID'
)
