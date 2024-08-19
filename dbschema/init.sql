CREATE TABLE `university`
(
    `id`                       int         NOT NULL AUTO_INCREMENT,
    `zh_name`                  varchar(64) NOT NULL,
    `logo`                     varchar(256)  DEFAULT NULL,
    `official_website`         varchar(2048) DEFAULT NULL COMMENT '学校官网,多个网站使用 , 分割',
    `admissions_contact_phone` varchar(2048) DEFAULT NULL COMMENT '招生电话 多个电话使用逗号分割',
    `admissions_contact_email` varchar(2048) DEFAULT NULL COMMENT '招生邮箱 多个邮箱使用逗号分割',
    `arwu_ranking`             int           DEFAULT NULL COMMENT '软科排名',
    `aa_ranking`               int           DEFAULT NULL COMMENT '校友会排名',
    `qs_ranking`               int           DEFAULT NULL COMMENT 'QS排名',
    `usn_ranking`              int           DEFAULT NULL COMMENT 'U.S. News世界大学排名',
    `the_ranking`              int           DEFAULT NULL COMMENT '泰晤士大学排名',
    `edu_level`                varchar(16)   DEFAULT NULL COMMENT '教育层次，A代表本科 B代表专科',
    `edu_category`             varchar(16)   DEFAULT NULL COMMENT '教育类别 A代表综合类 B代表理工类',
    `edu_establish`            varchar(16)   DEFAULT NULL COMMENT '办学性质 A代表公办',
    `tags`                     varchar(256)  DEFAULT NULL COMMENT '学校标签 多个标签使用英文逗号分割',
    `establish_time`           varchar(32)   DEFAULT NULL COMMENT '建校时间',
    `area`                     varchar(16)   DEFAULT NULL COMMENT '面积 以亩为单位',
    `mgr_dept`                 varchar(32)   DEFAULT NULL COMMENT '主管部分',
    `address`                  varchar(1024) DEFAULT NULL,
    `doctoral_program_num`     int           DEFAULT NULL COMMENT '博士点总数',
    `master_program_num`       int           DEFAULT NULL COMMENT '硕士点总数',
    `important_subject_num`    int           DEFAULT NULL COMMENT '国家重点学科数量',
    `province_id`              int           DEFAULT NULL COMMENT '省份ID',
    `province_name`            varchar(16)   DEFAULT NULL COMMENT '省份名称',
    `city_name`                varchar(16)   DEFAULT NULL COMMENT '市',
    `city_id`                  int           DEFAULT NULL COMMENT '市',
    `county_name`              varchar(16)   DEFAULT NULL COMMENT '县名称',
    `county_id`                int           DEFAULT NULL COMMENT '县ID',
    `town_name`                varchar(16)   DEFAULT NULL COMMENT '区名称 镇名称',
    `introduction`             text COMMENT '学校介绍',
    `f985`                     int           DEFAULT NULL COMMENT '是否是985 1代表是 0代表否',
    `f211`                     int           DEFAULT NULL COMMENT '是否是211 1代表是 0代表否',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 141
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='学校基础信息';

CREATE TABLE `major`
(
    `id`              int         NOT NULL AUTO_INCREMENT,
    `zh_name`         varchar(64) NOT NULL,
    `code`            varchar(64)   DEFAULT NULL COMMENT '专业代码',
    `edu_level`       varchar(16)   DEFAULT NULL COMMENT '教育层次，A代表本科 B代表专科',
    `course_scopes`   varchar(16)   DEFAULT NULL COMMENT '专业领域 例如工学 艺术学',
    `course_category` varchar(16)   DEFAULT NULL COMMENT '	学科类别： ',
    `edu_duration`    varchar(16)   DEFAULT NULL COMMENT '学制',
    `graduate`        varchar(16)   DEFAULT NULL COMMENT '授予学位',
    `introduction`    varchar(2048) DEFAULT NULL COMMENT '简介',
    `university_id`   int           DEFAULT NULL COMMENT '学校ID',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 2153358
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='专业信息';

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

CREATE TABLE `admissions_news`
(
    `id`            int NOT NULL AUTO_INCREMENT,
    `publish_date`  date         DEFAULT NULL COMMENT '发布日期',
    `title`         varchar(512) DEFAULT NULL COMMENT '标题',
    `content`       text COMMENT '内容',
    `type_id`       int          DEFAULT NULL,
    `type_name`     varchar(32)  DEFAULT NULL,
    `university_id` int          DEFAULT NULL COMMENT '学校ID',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 215427
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE `university_score`
(
    `id`                     int NOT NULL AUTO_INCREMENT,
    `year`                   varchar(16) DEFAULT NULL COMMENT '年份',
    `admissions_batch_num`   varchar(64) DEFAULT NULL COMMENT '录取批次 本科1批2批等',
    `admissions_type`        varchar(64) DEFAULT NULL COMMENT '录取类型：普通类 ｜地方专项计划｜国家专项计划',
    `min`                    varchar(64) DEFAULT NULL COMMENT '最低分',
    `min_ranking`            varchar(64) DEFAULT NULL COMMENT '最低位次',
    `max`                    varchar(64) DEFAULT NULL COMMENT '最高分',
    `avg`                    varchar(64) DEFAULT NULL COMMENT '平均分',
    `avg_ranking`            varchar(64) DEFAULT NULL COMMENT '平均排名',
    `province_id`            int         DEFAULT NULL COMMENT '省份ID',
    `province_name`          varchar(64) DEFAULT NULL COMMENT '省份名称',
    `subject_category`       varchar(64) DEFAULT NULL COMMENT '学科类别',
    `province_control_score` varchar(64) DEFAULT NULL COMMENT '省控分数线',
    `university_id`          varchar(64) DEFAULT NULL COMMENT '学校ID',
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx` (`university_id`, `year`, `admissions_batch_num`, `admissions_type`, `province_id`,
                      `subject_category`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='院校分数线'


CREATE TABLE `employment_region_rate_metric`
(
    `id`            int NOT NULL AUTO_INCREMENT,
    `university_id` int         DEFAULT NULL,
    `rate`          float(8, 2) DEFAULT NULL COMMENT '比例',
    `province_name` varchar(64) DEFAULT NULL COMMENT '省份地区',
    `year`          varchar(64) DEFAULT NULL COMMENT '年份',
    PRIMARY KEY (`id`),
    UNIQUE KEY `unki` (`university_id`, `year`, `province_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='就业地区流向指标表';

CREATE TABLE `company_attr_rate_metric`
(
    `id`            int NOT NULL AUTO_INCREMENT,
    `university_id` int         DEFAULT NULL,
    `name`          varchar(64) DEFAULT NULL,
    `rate`          float(8, 2) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `unik` (`university_id`, `name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='就业企业性质指标表';

CREATE TABLE `company_metric`
(
    `id`            int NOT NULL AUTO_INCREMENT,
    `university_id` int         DEFAULT NULL,
    `name`          varchar(64) DEFAULT NULL,
    `sort`          int         DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `unik` (`university_id`, `name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='公司指标表';