create table university
(
    id                       int(11) primary key auto_increment,
    zh_name                  varchar(64) not null,
    logo                     varchar(256),

    official_website         varchar(2048) comment '学校官网,多个网站使用 , 分割',
    admissions_contact_phone varchar(2048) comment '招生电话 多个电话使用逗号分割',
    admissions_contact_email varchar(2048) comment '招生邮箱 多个邮箱使用逗号分割',

    arwu_ranking             int(11) comment '软科排名',
    aa_ranking               int(11) comment '校友会排名',
    qs_ranking               int(11) comment 'QS排名',
    usn_ranking              int(11) comment 'U.S. News世界大学排名',
    the_ranking              int(11) comment '泰晤士大学排名',

    edu_level                varchar(16) comment '教育层次，A代表本科 B代表专科',
    edu_category             varchar(16) comment '教育类别 A代表综合类 B代表理工类',
    edu_establish            varchar(16) comment '办学性质 A代表公办',
    tags                     varchar(256) comment '学校标签 多个标签使用英文逗号分割',

    establish_time           varchar(32) comment '建校时间',
    area                     varchar(16) comment '面积 以亩为单位',
    mgr_dept                 varchar(32) comment '主管部分',
    address                  varchar(1024),

    doctoral_program_num     int(11) comment '博士点总数',
    master_program_num       int(11) comment '硕士点总数',
    important_subject_num    int(11) comment '国家重点学科数量',


    province_id              int(11) comment '省份ID',
    province_name            varchar(16) comment '省份名称',
    city_name                varchar(16) comment '市',
    city_id                  int(11) comment '市',
    county_name              varchar(16) comment '县名称',
    county_id                int(16) comment '县ID',
    town_name                varchar(16) comment '区名称 镇名称',

    introduction             text comment '学校介绍',

    f985                     int(2) comment '是否是985 1代表是 0代表否',
    f211                     int(2) comment '是否是211 1代表是 0代表否'

) comment '学校基础信息';

create table major
(
    id              int(11) primary key auto_increment,
    zh_name         varchar(64) not null,
    code            varchar(64) comment '专业代码',
    edu_level       varchar(16) comment '教育层次，A代表本科 B代表专科',
    course_scopes   varchar(16) comment '专业领域 例如工学 艺术学',
    course_category varchar(16) comment '	学科类别： ',
    edu_duration    varchar(16) comment '学制',
    graduate        varchar(16) comment '授予学位',
    introduction    varchar(2048) comment '简介',
    university_id   int(11) comment '学校ID'
) comment '专业信息';

CREATE TABLE `major_score`
(
    `id`                    int NOT NULL AUTO_INCREMENT,
    `str_id`                varchar(32) DEFAULT NULL COMMENT '原始字符串ID，标识唯一性',
    `subject_name`          varchar(64) DEFAULT NULL COMMENT '学科名称',
    `avg`                   varchar(16) DEFAULT NULL COMMENT '平均分',
    `max`                   varchar(16) DEFAULT NULL COMMENT '最大分',
    `min`                   varchar(16) DEFAULT NULL COMMENT '最低分',
    `min_ranking`           varchar(16) DEFAULT NULL COMMENT '最低位次',
    `batch_num_name`        varchar(32) DEFAULT NULL COMMENT '批次 本科1批 2批',
    `subject_scopes_name`   varchar(32) DEFAULT NULL COMMENT '学科领域',
    `subject_category_name` varchar(32) DEFAULT NULL COMMENT '学科类型名称',
    `major_id`              int         DEFAULT NULL COMMENT '专业ID',
    `university_id`         int         DEFAULT NULL COMMENT '学校ID',
    `year`                  varchar(16) DEFAULT NULL COMMENT '年份',
    `province_id`           int         DEFAULT NULL COMMENT '省份ID',
    `province_name`         varchar(32) DEFAULT NULL COMMENT '省份名称',
    `min_range`             varchar(64) DEFAULT NULL COMMENT '最低分范围',
    `min_rank_range`        varchar(64) DEFAULT NULL COMMENT '最低位次范围',
    PRIMARY KEY (`id`),
    UNIQUE KEY `strid` (`str_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='专业分数线';

CREATE TABLE `admissions_plan`
(
    `id`                 int NOT NULL AUTO_INCREMENT,
    `major_name`         varchar(64) DEFAULT NULL COMMENT '专业名称',
    `admissions_stu_num` int         DEFAULT NULL COMMENT '计划招生人数',
    `edu_fee`            varchar(64) DEFAULT NULL COMMENT '学费',
    `university_id`      int         DEFAULT NULL COMMENT '学校ID',
    `major_code`         varchar(32) DEFAULT NULL COMMENT '专业代码编号',
    `batch_num_name`     varchar(32) DEFAULT NULL COMMENT '批次 本科1批 2批',
    `subject_name`       varchar(16) DEFAULT NULL COMMENT '学科 文科理科',
    `year`               varchar(16) DEFAULT NULL,
    `province_id`        int         DEFAULT NULL,
    `province_name`      varchar(16) DEFAULT NULL COMMENT '省份',
    `cond`               varchar(64) DEFAULT NULL COMMENT '选科要求',
    `edu_dur`            varchar(64) DEFAULT NULL COMMENT '学制 4年 ｜ 5年',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_k` (`university_id`, `year`, `major_name`, `province_id`, `batch_num_name`, `subject_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

create table admissions_news
(
    id            int(11) primary key auto_increment,
    publish_date  date comment '发布日期',
    title         varchar(32) comment '标题',
    content       text comment '内容',
    type_id       int(11) comment '',
    type_name     varchar(32) comment '',
    university_id int(11) comment '学校ID'
)
