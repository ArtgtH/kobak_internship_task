CREATE TABLE public.extra_report_summands (
    id integer NOT NULL,
    project integer,
    parent_report integer,
    time_in_percent real
);


ALTER TABLE public.extra_report_summands OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 156007)
-- Name: extra_report_summands_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.extra_report_summands_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extra_report_summands_id_seq OWNER TO postgres;

--
-- TOC entry 3385 (class 0 OID 0)
-- Dependencies: 224
-- Name: extra_report_summands_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.extra_report_summands_id_seq OWNED BY public.extra_report_summands.id;


--
-- TOC entry 223 (class 1259 OID 106833)
-- Name: managers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.managers (
    login character varying(20) NOT NULL,
    password character varying(20) NOT NULL
);


ALTER TABLE public.managers OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 73986)
-- Name: project_staff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_staff (
    staff_id integer NOT NULL,
    project_id integer NOT NULL
);


ALTER TABLE public.project_staff OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 73981)
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    description character varying(100)
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 73980)
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.projects ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.projects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 222 (class 1259 OID 74026)
-- Name: report_summands; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_summands (
    id integer NOT NULL,
    project integer,
    parent_report integer,
    time_in_percent real
);


ALTER TABLE public.report_summands OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 74025)
-- Name: report_summands_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_summands_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_summands_id_seq OWNER TO postgres;

--
-- TOC entry 3386 (class 0 OID 0)
-- Dependencies: 221
-- Name: report_summands_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_summands_id_seq OWNED BY public.report_summands.id;


--
-- TOC entry 220 (class 1259 OID 74014)
-- Name: reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reports (
    id integer NOT NULL,
    report_date timestamp without time zone,
    staff integer
);


ALTER TABLE public.reports OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 74013)
-- Name: reports_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reports_id_seq OWNER TO postgres;

--
-- TOC entry 3387 (class 0 OID 0)
-- Dependencies: 219
-- Name: reports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reports_id_seq OWNED BY public.reports.id;


--
-- TOC entry 215 (class 1259 OID 73975)
-- Name: staff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staff (
    id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    tg_name character varying(100) NOT NULL,
    role character varying(100),
    grade character varying(100)
);


ALTER TABLE public.staff OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 73974)
-- Name: staff_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.staff ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.staff_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3203 (class 2604 OID 156011)
-- Name: extra_report_summands id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extra_report_summands ALTER COLUMN id SET DEFAULT nextval('public.extra_report_summands_id_seq'::regclass);


--
-- TOC entry 3202 (class 2604 OID 74029)
-- Name: report_summands id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_summands ALTER COLUMN id SET DEFAULT nextval('public.report_summands_id_seq'::regclass);


--
-- TOC entry 3201 (class 2604 OID 74017)
-- Name: reports id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports ALTER COLUMN id SET DEFAULT nextval('public.reports_id_seq'::regclass);


--
-- TOC entry 3378 (class 0 OID 156008)
-- Dependencies: 225
-- Data for Name: extra_report_summands; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.extra_report_summands (id, project, parent_report, time_in_percent) FROM stdin;
30	2	88	25
31	2	89	25
32	2	90	25
33	2	91	25
34	2	92	25
35	2	93	40
36	2	94	40
37	2	95	40
38	2	96	40
39	2	97	40
\.


--
-- TOC entry 3376 (class 0 OID 106833)
-- Dependencies: 223
-- Data for Name: managers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.managers (login, password) FROM stdin;
Artem	Metra2004
\.


--
-- TOC entry 3371 (class 0 OID 73986)
-- Dependencies: 218
-- Data for Name: project_staff; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_staff (staff_id, project_id) FROM stdin;
1	1
9	1
1	5
10	5
9	6
1	6
10	6
\.


--
-- TOC entry 3370 (class 0 OID 73981)
-- Dependencies: 217
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, description) FROM stdin;
1	ТгБотНаЧасы
2	Проект2
5	ОтсидкаЧетырехПар
6	ОтсидкаАнглийского
\.


--
-- TOC entry 3375 (class 0 OID 74026)
-- Dependencies: 222
-- Data for Name: report_summands; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report_summands (id, project, parent_report, time_in_percent) FROM stdin;
128	1	88	25
129	5	88	25
130	6	88	25
131	1	89	25
132	5	89	25
133	6	89	25
134	1	90	25
135	5	90	25
136	6	90	25
137	1	91	25
138	5	91	25
139	6	91	25
140	1	92	25
141	5	92	25
142	6	92	25
143	1	93	20
144	5	93	20
145	6	93	20
146	1	94	20
147	5	94	20
148	6	94	20
149	1	95	20
150	5	95	20
151	6	95	20
152	1	96	20
153	5	96	20
154	6	96	20
155	1	97	20
156	5	97	20
157	6	97	20
\.


--
-- TOC entry 3373 (class 0 OID 74014)
-- Dependencies: 220
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports (id, report_date, staff) FROM stdin;
88	2023-11-13 00:00:00	1
89	2023-11-14 00:00:00	1
90	2023-11-15 00:00:00	1
91	2023-11-16 00:00:00	1
92	2023-11-17 00:00:00	1
93	2023-11-20 00:00:00	1
94	2023-11-21 00:00:00	1
95	2023-11-22 00:00:00	1
96	2023-11-23 00:00:00	1
97	2023-11-24 00:00:00	1
98	2023-11-20 00:00:00	1
99	2023-11-21 00:00:00	1
100	2023-11-22 00:00:00	1
101	2023-11-23 00:00:00	1
102	2023-11-24 00:00:00	1
\.


--
-- TOC entry 3368 (class 0 OID 73975)
-- Dependencies: 215
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staff (id, full_name, tg_name, role, grade) FROM stdin;
9	Иван Генадий	@IvanG	Дизайнер UX / UI	senior
10	Володимр	@Vova	Разработчик backend ПО	middle
11	Борис Карась	@boris1999	Проджект менеджер	senior
13	Евгений Георгий	@adsd	Тимлид Web	principle
1	Артём Вичук	@ArtemVichuk	хочу ананас	super
\.


--
-- TOC entry 3388 (class 0 OID 0)
-- Dependencies: 224
-- Name: extra_report_summands_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.extra_report_summands_id_seq', 39, true);


--
-- TOC entry 3389 (class 0 OID 0)
-- Dependencies: 216
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_id_seq', 6, true);


--
-- TOC entry 3390 (class 0 OID 0)
-- Dependencies: 221
-- Name: report_summands_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_summands_id_seq', 172, true);


--
-- TOC entry 3391 (class 0 OID 0)
-- Dependencies: 219
-- Name: reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_id_seq', 102, true);


--
-- TOC entry 3392 (class 0 OID 0)
-- Dependencies: 214
-- Name: staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staff_id_seq', 13, true);


--
-- TOC entry 3217 (class 2606 OID 156013)
-- Name: extra_report_summands extra_report_summands_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extra_report_summands
    ADD CONSTRAINT extra_report_summands_pkey PRIMARY KEY (id);


--
-- TOC entry 3215 (class 2606 OID 106837)
-- Name: managers managers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.managers
    ADD CONSTRAINT managers_pkey PRIMARY KEY (login);


--
-- TOC entry 3209 (class 2606 OID 73990)
-- Name: project_staff project_staff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_staff
    ADD CONSTRAINT project_staff_pkey PRIMARY KEY (staff_id, project_id);


--
-- TOC entry 3207 (class 2606 OID 73985)
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- TOC entry 3213 (class 2606 OID 74031)
-- Name: report_summands report_summands_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_summands
    ADD CONSTRAINT report_summands_pkey PRIMARY KEY (id);


--
-- TOC entry 3211 (class 2606 OID 74019)
-- Name: reports reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (id);


--
-- TOC entry 3205 (class 2606 OID 73979)
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (id);


--
-- TOC entry 3223 (class 2606 OID 156019)
-- Name: extra_report_summands extra_report_summands_parent_report_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extra_report_summands
    ADD CONSTRAINT extra_report_summands_parent_report_fkey FOREIGN KEY (parent_report) REFERENCES public.reports(id) ON DELETE CASCADE;


--
-- TOC entry 3224 (class 2606 OID 156014)
-- Name: extra_report_summands extra_report_summands_project_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extra_report_summands
    ADD CONSTRAINT extra_report_summands_project_fkey FOREIGN KEY (project) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- TOC entry 3218 (class 2606 OID 73996)
-- Name: project_staff project_staff_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_staff
    ADD CONSTRAINT project_staff_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- TOC entry 3219 (class 2606 OID 73991)
-- Name: project_staff project_staff_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_staff
    ADD CONSTRAINT project_staff_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staff(id);


--
-- TOC entry 3221 (class 2606 OID 74037)
-- Name: report_summands report_summands_parent_report_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_summands
    ADD CONSTRAINT report_summands_parent_report_fkey FOREIGN KEY (parent_report) REFERENCES public.reports(id);


--
-- TOC entry 3222 (class 2606 OID 74032)
-- Name: report_summands report_summands_project_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_summands
    ADD CONSTRAINT report_summands_project_fkey FOREIGN KEY (project) REFERENCES public.projects(id);


--
-- TOC entry 3220 (class 2606 OID 74020)
-- Name: reports reports_staff_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_staff_fkey FOREIGN KEY (staff) REFERENCES public.staff(id);


-- Completed on 2023-12-07 18:00:24

--
-- PostgreSQL database dump complete
--

