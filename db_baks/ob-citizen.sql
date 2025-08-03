--
-- PostgreSQL database dump
--

-- Dumped from database version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.2)
-- Dumped by pg_dump version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: Status; Type: TYPE; Schema: public; Owner: microservices
--

CREATE TYPE public."Status" AS ENUM (
    'Pending',
    'Approved',
    'Rejected'
);


ALTER TYPE public."Status" OWNER TO microservices;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Action; Type: TABLE; Schema: public; Owner: microservices
--

CREATE TABLE public."Action" (
    id integer NOT NULL,
    action text NOT NULL,
    assigned_officer_id integer NOT NULL,
    ob_number text NOT NULL,
    resolved boolean DEFAULT false NOT NULL,
    forwarded_to text,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "sub_module_dataId" integer NOT NULL
);


ALTER TABLE public."Action" OWNER TO microservices;

--
-- Name: Action_id_seq; Type: SEQUENCE; Schema: public; Owner: microservices
--

CREATE SEQUENCE public."Action_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Action_id_seq" OWNER TO microservices;

--
-- Name: Action_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: microservices
--

ALTER SEQUENCE public."Action_id_seq" OWNED BY public."Action".id;


--
-- Name: IPRS_Person; Type: TABLE; Schema: public; Owner: microservices
--

CREATE TABLE public."IPRS_Person" (
    id integer NOT NULL,
    id_no text,
    passport_no text,
    first_name text NOT NULL,
    middle_name text,
    last_name text NOT NULL,
    gender text NOT NULL,
    nationality text NOT NULL,
    county_of_birth text,
    district_of_birth text,
    division_of_birth text,
    location_of_birth text,
    date_of_birth timestamp(3) without time zone NOT NULL,
    mug_shot text,
    email text,
    phone_number text,
    county text,
    sub_county text
);


ALTER TABLE public."IPRS_Person" OWNER TO microservices;

--
-- Name: IPRS_Person_id_seq; Type: SEQUENCE; Schema: public; Owner: microservices
--

CREATE SEQUENCE public."IPRS_Person_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."IPRS_Person_id_seq" OWNER TO microservices;

--
-- Name: IPRS_Person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: microservices
--

ALTER SEQUENCE public."IPRS_Person_id_seq" OWNED BY public."IPRS_Person".id;


--
-- Name: ModuleData; Type: TABLE; Schema: public; Owner: microservices
--

CREATE TABLE public."ModuleData" (
    id integer NOT NULL,
    "moduleId" integer NOT NULL,
    "submissionDate" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    attachments text[],
    "formData" jsonb NOT NULL,
    "userId" integer NOT NULL
);


ALTER TABLE public."ModuleData" OWNER TO microservices;

--
-- Name: ModuleData_id_seq; Type: SEQUENCE; Schema: public; Owner: microservices
--

CREATE SEQUENCE public."ModuleData_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ModuleData_id_seq" OWNER TO microservices;

--
-- Name: ModuleData_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: microservices
--

ALTER SEQUENCE public."ModuleData_id_seq" OWNED BY public."ModuleData".id;


--
-- Name: Modules; Type: TABLE; Schema: public; Owner: microservices
--

CREATE TABLE public."Modules" (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    bf boolean DEFAULT false NOT NULL,
    repetition boolean DEFAULT false NOT NULL,
    fields jsonb,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public."Modules" OWNER TO microservices;

--
-- Name: Modules_id_seq; Type: SEQUENCE; Schema: public; Owner: microservices
--

CREATE SEQUENCE public."Modules_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Modules_id_seq" OWNER TO microservices;

--
-- Name: Modules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: microservices
--

ALTER SEQUENCE public."Modules_id_seq" OWNED BY public."Modules".id;


--
-- Name: _prisma_migrations; Type: TABLE; Schema: public; Owner: microservices
--

CREATE TABLE public._prisma_migrations (
    id character varying(36) NOT NULL,
    checksum character varying(64) NOT NULL,
    finished_at timestamp with time zone,
    migration_name character varying(255) NOT NULL,
    logs text,
    rolled_back_at timestamp with time zone,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    applied_steps_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public._prisma_migrations OWNER TO microservices;

--
-- Name: contact_center; Type: TABLE; Schema: public; Owner: microservices
--

CREATE TABLE public.contact_center (
    id integer NOT NULL,
    status public."Status" DEFAULT 'Pending'::public."Status" NOT NULL,
    "sub_module_dataId" integer NOT NULL,
    ob_number text,
    sync_id text,
    comment text
);


ALTER TABLE public.contact_center OWNER TO microservices;

--
-- Name: contact_center_id_seq; Type: SEQUENCE; Schema: public; Owner: microservices
--

CREATE SEQUENCE public.contact_center_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contact_center_id_seq OWNER TO microservices;

--
-- Name: contact_center_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: microservices
--

ALTER SEQUENCE public.contact_center_id_seq OWNED BY public.contact_center.id;


--
-- Name: sub_module; Type: TABLE; Schema: public; Owner: microservices
--

CREATE TABLE public.sub_module (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    bf boolean DEFAULT false NOT NULL,
    repetition boolean DEFAULT false NOT NULL,
    fields jsonb,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "modulesId" integer NOT NULL
);


ALTER TABLE public.sub_module OWNER TO microservices;

--
-- Name: sub_module_data; Type: TABLE; Schema: public; Owner: microservices
--

CREATE TABLE public.sub_module_data (
    id integer NOT NULL,
    "sub_moduleId" integer NOT NULL,
    "submissionDate" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    attachments text[],
    "formData" jsonb NOT NULL,
    "userId" integer NOT NULL,
    status public."Status" DEFAULT 'Pending'::public."Status" NOT NULL,
    sync_id text,
    comment text,
    location text,
    pin text,
    station_id integer,
    ob_number text,
    email text,
    id_no text,
    phone_number text,
    urgency text,
    county text,
    sub_county text
);


ALTER TABLE public.sub_module_data OWNER TO microservices;

--
-- Name: sub_module_data_id_seq; Type: SEQUENCE; Schema: public; Owner: microservices
--

CREATE SEQUENCE public.sub_module_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sub_module_data_id_seq OWNER TO microservices;

--
-- Name: sub_module_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: microservices
--

ALTER SEQUENCE public.sub_module_data_id_seq OWNED BY public.sub_module_data.id;


--
-- Name: sub_module_id_seq; Type: SEQUENCE; Schema: public; Owner: microservices
--

CREATE SEQUENCE public.sub_module_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sub_module_id_seq OWNER TO microservices;

--
-- Name: sub_module_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: microservices
--

ALTER SEQUENCE public.sub_module_id_seq OWNED BY public.sub_module.id;


--
-- Name: Action id; Type: DEFAULT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."Action" ALTER COLUMN id SET DEFAULT nextval('public."Action_id_seq"'::regclass);


--
-- Name: IPRS_Person id; Type: DEFAULT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."IPRS_Person" ALTER COLUMN id SET DEFAULT nextval('public."IPRS_Person_id_seq"'::regclass);


--
-- Name: ModuleData id; Type: DEFAULT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."ModuleData" ALTER COLUMN id SET DEFAULT nextval('public."ModuleData_id_seq"'::regclass);


--
-- Name: Modules id; Type: DEFAULT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."Modules" ALTER COLUMN id SET DEFAULT nextval('public."Modules_id_seq"'::regclass);


--
-- Name: contact_center id; Type: DEFAULT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public.contact_center ALTER COLUMN id SET DEFAULT nextval('public.contact_center_id_seq'::regclass);


--
-- Name: sub_module id; Type: DEFAULT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public.sub_module ALTER COLUMN id SET DEFAULT nextval('public.sub_module_id_seq'::regclass);


--
-- Name: sub_module_data id; Type: DEFAULT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public.sub_module_data ALTER COLUMN id SET DEFAULT nextval('public.sub_module_data_id_seq'::regclass);


--
-- Data for Name: Action; Type: TABLE DATA; Schema: public; Owner: microservices
--

COPY public."Action" (id, action, assigned_officer_id, ob_number, resolved, forwarded_to, "createdAt", "updatedAt", "sub_module_dataId") FROM stdin;
1	11	8	OB/012/1404/4/8/2025	t	DCI	2025-04-08 11:06:56.862	2025-04-08 11:06:56.862	31
2	11	8	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:21:40.936	2025-04-08 11:21:40.936	31
3	11	8	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:21:42.822	2025-04-08 11:21:42.822	31
4	11	8	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.336	2025-04-08 11:26:13.336	31
5	11	8	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.379	2025-04-08 11:26:13.379	31
6	11	13	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.4	2025-04-08 11:26:13.4	31
7	11	13	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.422	2025-04-08 11:26:13.422	31
8	11	8	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.446	2025-04-08 11:26:13.446	31
9	11	16	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.469	2025-04-08 11:26:13.469	31
10	11	12	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.492	2025-04-08 11:26:13.492	31
11	11	8	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.58	2025-04-08 11:26:13.58	31
12	11	8	OB/012/1404/4/8/2025	t	DCI	2025-04-08 11:26:13.717	2025-04-08 11:26:13.717	31
13	11	8	OB/012/1404/4/8/2025	t	DCI	2025-04-08 11:26:13.739	2025-04-08 11:26:13.739	31
14	11	8	OB/012/1404/4/8/2025	t	DCI	2025-04-08 11:26:13.774	2025-04-08 11:26:13.774	31
15	11	8	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.793	2025-04-08 11:26:13.793	31
16	11	8	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:26:13.815	2025-04-08 11:26:13.815	31
17	11	12	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:31:12.405	2025-04-08 11:31:12.405	31
18	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:38:46.352	2025-04-08 11:38:46.352	31
19	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:54:57.859	2025-04-08 11:54:57.859	31
20	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:56:12.785	2025-04-08 11:56:12.785	31
21	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 11:57:07.954	2025-04-08 11:57:07.954	31
22	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 12:04:29.522	2025-04-08 12:04:29.522	31
23	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 14:21:01.028	2025-04-08 14:21:01.028	31
24	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 14:38:36.602	2025-04-08 14:38:36.602	31
25	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 14:45:12.696	2025-04-08 14:45:12.696	31
26	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 15:05:04.529	2025-04-08 15:05:04.529	31
27	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 15:06:16.377	2025-04-08 15:06:16.377	31
28	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 15:07:56.564	2025-04-08 15:07:56.564	31
29	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 15:12:36.673	2025-04-08 15:12:36.673	31
30	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 15:15:30.504	2025-04-08 15:15:30.504	31
31	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 15:16:11.614	2025-04-08 15:16:11.614	31
32	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 15:16:34.422	2025-04-08 15:16:34.422	31
33	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-08 15:30:04.174	2025-04-08 15:30:04.174	31
34	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-09 06:20:52.113	2025-04-09 06:20:52.113	31
35	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-09 06:26:21.676	2025-04-09 06:26:21.676	31
36	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-09 06:47:19.616	2025-04-09 06:47:19.616	31
37	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-09 06:50:27.557	2025-04-09 06:50:27.557	31
38	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-09 06:58:11.061	2025-04-09 06:58:11.061	31
39	11	7	OB/012/1404/4/8/2025	f	\N	2025-04-09 07:01:12.039	2025-04-09 07:01:12.039	31
40	6	7	OB/012/1417/4/9/2025	f	\N	2025-04-09 12:42:51.322	2025-04-09 12:42:51.322	41
41	6	7	OB/012/1417/4/9/2025	f	\N	2025-04-09 12:42:56.448	2025-04-09 12:42:56.448	41
42	11	7	OB/012/1418/4/9/2025	f	\N	2025-04-09 12:47:31.375	2025-04-09 12:47:31.375	42
43	10	13	OB/012/1428/4/15/2025	f	\N	2025-04-15 11:04:27.321	2025-04-15 11:04:27.321	49
44	12	12	OB/012/1429/4/15/2025	f	\N	2025-04-16 07:26:33.799	2025-04-16 07:26:33.799	50
45	11	12	OB/012/1432/4/16/2025	f	\N	2025-04-16 07:35:45.542	2025-04-16 07:35:45.542	51
46	11	12	OB/012/1432/4/16/2025	f	\N	2025-04-16 07:35:56.891	2025-04-16 07:35:56.891	51
47	4	7	OB/012/1433/4/16/2025	f	\N	2025-04-16 07:36:24.099	2025-04-16 07:36:24.099	52
48	4	8	OB/012/1433/4/16/2025	f	\N	2025-04-16 07:36:54.297	2025-04-16 07:36:54.297	52
49	5	7	OB/012/1434/4/16/2025	f	\N	2025-04-16 07:40:09.054	2025-04-16 07:40:09.054	53
50	11	13	OB/012/1367/4/4/2025	f	\N	2025-04-20 09:19:11.258	2025-04-20 09:19:11.258	11
51	11	13	OB/012/1367/4/4/2025	f	\N	2025-04-20 09:19:18.393	2025-04-20 09:19:18.393	11
52	11	16	OB/012/1367/4/4/2025	f	\N	2025-04-20 09:52:46.542	2025-04-20 09:52:46.542	11
53	11	16	OB/012/1367/4/4/2025	f	\N	2025-04-20 09:52:49.367	2025-04-20 09:52:49.367	11
54	11	12	OB/012/1367/4/4/2025	f	DCI	2025-04-20 10:21:00.559	2025-04-20 10:21:00.559	11
55	11	12	OB/012/1367/4/4/2025	f	DCI	2025-04-20 10:21:07.92	2025-04-20 10:21:07.92	11
56	11	12	OB/012/1367/4/4/2025	f	\N	2025-04-20 10:52:46.93	2025-04-20 10:52:46.93	11
57	11	12	OB/012/1367/4/4/2025	f	\N	2025-04-20 10:52:47.952	2025-04-20 10:52:47.952	11
58	11	7	OB/012/1367/4/4/2025	f	\N	2025-04-21 08:14:47.887	2025-04-21 08:14:47.887	11
59	11	8	OB/012/1367/4/4/2025	f	\N	2025-04-21 09:15:07.901	2025-04-21 09:15:07.901	11
60	11	16	OB/012/1367/4/4/2025	f	\N	2025-04-21 09:19:45.992	2025-04-21 09:19:45.992	11
61	11	12	OB/012/1367/4/4/2025	f	\N	2025-04-21 11:16:17.855	2025-04-21 11:16:17.855	11
62	11	7	OB/012/1367/4/4/2025	f	\N	2025-04-21 11:49:09.043	2025-04-21 11:49:09.043	11
63	3	12	OB/069/1442/4/22/2025	f	\N	2025-04-22 06:46:23.993	2025-04-22 06:46:23.993	54
64	11	7	OB/012/1367/4/4/2025	f	DCI	2025-04-22 06:49:15.568	2025-04-22 06:49:15.568	11
65	3	12	OB/233/1443/4/22/2025	f	\N	2025-04-22 07:54:28.361	2025-04-22 07:54:28.361	56
66	3	12	OB/233/1443/4/22/2025	f	\N	2025-04-22 07:54:32.79	2025-04-22 07:54:32.79	56
67	5	13	OB/012/1440/4/17/2025	f	\N	2025-04-22 07:59:20.153	2025-04-22 07:59:20.153	53
68	7	16	OB/012/1444/4/22/2025	f	\N	2025-04-22 08:01:25.138	2025-04-22 08:01:25.138	57
69	7	13	OB/012/1445/4/22/2025	f	\N	2025-04-22 08:40:19.21	2025-04-22 08:40:19.21	58
\.


--
-- Data for Name: IPRS_Person; Type: TABLE DATA; Schema: public; Owner: microservices
--

COPY public."IPRS_Person" (id, id_no, passport_no, first_name, middle_name, last_name, gender, nationality, county_of_birth, district_of_birth, division_of_birth, location_of_birth, date_of_birth, mug_shot, email, phone_number, county, sub_county) FROM stdin;
1	36445676	\N	Michel	Nasimiyu	Cheboi	Female	Kenya	\N	Bungoma East	\N	\N	1999-03-01 21:00:00	\N	\N	\N	\N	\N
2	32622498	\N	Otieno	Chrispine	Shikuku	male	Kenya	\N	Rachuonyo	\N	\N	1994-12-23 21:00:00	\N	\N	\N	\N	\N
3	40049245	\N	Nyamu	\N	Karani	male	Kenya	\N	\N	\N	\N	2003-07-05 21:00:00	\N	\N	\N	\N	\N
4	33641337	\N	Martin	Kamau	Mwathi	male	Kenya	\N	\N	\N	\N	1996-11-26 21:00:00	\N	\N	\N	\N	\N
5	11223541	\N	Charles	Carl Karani	Nyamu	male	Kenya	\N	Starehe	\N	\N	1972-05-01 21:00:00	\N	\N	\N	\N	\N
6	35994553	\N	Faith	\N	Amusibwa	Female	Kenya	\N	\N	\N	\N	1997-06-30 21:00:00	\N	\N	\N	\N	\N
7	35029142	\N	David	Muia	Mutavi	male	Kenya	\N	Thika East	\N	\N	1998-05-12 21:00:00	\N	\N	\N	\N	\N
8	22015136	\N	Phylis	Wanja	Gathoni	Female	Kenya	\N	Nyeri East	\N	\N	1979-12-29 21:00:00	\N	\N	\N	\N	\N
9	34535631	\N	Mutuku		Kyenze	male	Kenya	\N	Kibwezi	\N	\N	1997-03-02 21:00:00	\N	\N	\N	\N	\N
\.


--
-- Data for Name: ModuleData; Type: TABLE DATA; Schema: public; Owner: microservices
--

COPY public."ModuleData" (id, "moduleId", "submissionDate", attachments, "formData", "userId") FROM stdin;
\.


--
-- Data for Name: Modules; Type: TABLE DATA; Schema: public; Owner: microservices
--

COPY public."Modules" (id, name, description, bf, repetition, fields, "createdAt") FROM stdin;
12	GBV	Gender Based Violence	f	f	null	2025-04-03 12:29:05.27
11	Arson	Vandalizing or damaging by burning down	f	f	null	2025-04-03 12:28:40.588
3	Cyber Crime	Criminal activity that are carried out using digital devices and networks	f	f	null	2025-04-03 12:26:00.237
1	Assault	Physical attack on someone	f	f	null	2025-04-03 12:25:20.678
5	Homicide	Intentional or unintentional murder manslaughter or killing of a person	f	f	null	2025-04-03 12:26:41.657
6	Missing Person	Someone whose whereabouts are unkown and their absence raises concerns	f	f	null	2025-04-03 12:27:09.399
7	Motor Vehicle Theft	Stealing or unlawfully taking a vehicle without the owner's consent	f	f	null	2025-04-03 12:27:28.245
8	Rape	Act of forcing someone into sexual intercourse or sexual acts without consent	f	f	null	2025-04-03 12:27:44.165
9	Robbery	Taking property unlawfully from a person or place by force or threat of force	f	f	null	2025-04-03 12:27:58.589
2	Burglary	Unlawful or forced entry into a building to commit a crime	f	f	null	2025-04-03 12:25:35.986
10	Stolen Lost Item	Something that has been taken without permission or cannot be found	f	f	null	2025-04-03 12:28:18.377
4	Death	Permanent End of Life when a person's body stops working completely	f	f	null	2025-04-03 12:26:16.973
\.


--
-- Data for Name: _prisma_migrations; Type: TABLE DATA; Schema: public; Owner: microservices
--

COPY public._prisma_migrations (id, checksum, finished_at, migration_name, logs, rolled_back_at, started_at, applied_steps_count) FROM stdin;
b9d3410e-c199-4723-94ed-6dcc6a084945	e656657e55f2a22fbe81c2a42a98f784e67d8398b6277d23ae34a8af403fe59c	2025-04-03 12:06:57.709169+00	20250113090728_initial	\N	\N	2025-04-03 12:06:55.04068+00	1
9a42e634-9df1-4456-9421-b933585290eb	ea15eaa094b952eb70111e32f39f3b11b55d9d1e67b0be59794dd3455d916eb9	2025-04-08 10:56:35.726879+00	20250408105634_acitons	\N	\N	2025-04-08 10:56:34.040919+00	1
8a56c7a2-45ee-4067-b015-e48fc2cd9abc	0d6aa96dcc49390d04a75b53f70a1eb81400386b463e2a47b0c2b8cc4cd61b5c	2025-04-03 12:06:58.116392+00	20250113092450_clear	\N	\N	2025-04-03 12:06:57.73237+00	1
2302be35-74bc-47e3-9d2c-1c48291046a8	bb5c27b5b0c5e70d4ceeefe2f2f8cec586d2fc0343e0612d70f0b5b57b723597	2025-04-03 12:06:58.238799+00	20250117061227_status	\N	\N	2025-04-03 12:06:58.138286+00	1
b7f64dd3-2b05-43fb-80df-8a254352ca48	82b96ffc1826a193f1337fc54c0c4b489aa9f64638e6e25374c1cb9a34e3dc3f	2025-04-03 12:06:58.475282+00	20250203062601_conatct_center	\N	\N	2025-04-03 12:06:58.261338+00	1
403b00b0-ef81-46e1-8da6-8ec9821ed6a5	4bff39cff8094de7194483d6c801ffd45b4567243845f5c8b469fff90e4f233b	2025-04-03 12:06:58.837044+00	20250203070303_ob	\N	\N	2025-04-03 12:06:58.531503+00	1
49534be1-6127-4d9d-9711-556e0e4d1397	29af5337b9d7d1444a693e6c96bb7fbd689cf83a8997b5efc5feb2053e77716f	2025-04-03 12:06:58.915692+00	20250317083329_sync	\N	\N	2025-04-03 12:06:58.859615+00	1
dde73c1d-92d3-4958-9e78-0dbec455f5ba	513403e625e4c01ebbc986c20a87651721f05831bbb0563e324e8293d228d93a	2025-04-03 12:06:59.027581+00	20250320093615_comment	\N	\N	2025-04-03 12:06:58.937989+00	1
666a5869-b0c8-44a4-882c-48ee0a52999e	66635b82842a7863030e7786787ba6e2b005c8231c818f470b02835bd01383cb	2025-04-03 12:06:59.162357+00	20250324114832_ob	\N	\N	2025-04-03 12:06:59.050092+00	1
41fafc6a-9672-4395-96a4-d1044dfad34f	83972e372d96c6d972442f431574f92659a70fdd3958e72ca26301626028af80	2025-04-03 12:06:59.252048+00	20250324115714_o	\N	\N	2025-04-03 12:06:59.184833+00	1
90ca4ae0-d77b-468b-9f36-bbd164cf7797	a242b72f8e644d8b684201d6f12bd112ff9ae1a376cb9b9715a02925a5ba1040	2025-04-03 12:06:59.834895+00	20250325062106_iprs	\N	\N	2025-04-03 12:06:59.274709+00	1
6670d9f6-d56e-4da8-bd32-ec17c28f5e3e	841c00e4b3f8cebd0407b8c442af49f9b825aaca649a0ec992bed84e86512af2	2025-04-03 12:06:59.993079+00	20250325062341_opp_prd	\N	\N	2025-04-03 12:06:59.86851+00	1
97ecd2b2-6db7-4318-a363-e09ea2013068	473bc7a0ed199513519a51928f56a82808b798a694e0f4a0fd57703e01428edb	2025-04-03 12:07:00.161281+00	20250325093230_email	\N	\N	2025-04-03 12:07:00.01564+00	1
f1e45e1c-bf08-46b3-bf96-4692aa3cb560	9a6447bf6da5a1f1880596da3741b2c7668f5815f51ba9dd77d6857a98bfa1d2	2025-04-03 12:07:00.228813+00	20250401132305_urgency	\N	\N	2025-04-03 12:07:00.183801+00	1
73dcd068-08a3-4f5a-abd8-71409e6c1b3d	5d9ff76f980cc8ee1d0914fe764ed09ad286e6688212ebe83c56bc76ece26ecf	2025-04-03 12:07:20.223824+00	20250403120720_	\N	\N	2025-04-03 12:07:20.064606+00	1
\.


--
-- Data for Name: contact_center; Type: TABLE DATA; Schema: public; Owner: microservices
--

COPY public.contact_center (id, status, "sub_module_dataId", ob_number, sync_id, comment) FROM stdin;
\.


--
-- Data for Name: sub_module; Type: TABLE DATA; Schema: public; Owner: microservices
--

COPY public.sub_module (id, name, description, bf, repetition, fields, "createdAt", "modulesId") FROM stdin;
4	Death		f	f	[{"name": "Who is dead", "type": "select", "options": ["Minor", "Adult"], "required": true}, {"name": "Name", "type": "text", "required": true}, {"name": "Age", "type": "select", "options": ["0 - 5", "6 - 12", "13 - 17"], "dependency": {"value": "Minor", "question": "Who is dead"}}, {"name": "Age", "type": "select", "options": ["18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65 and above"], "dependency": {"value": "Adult", "question": "Who is dead"}}, {"name": "Gender of deceased", "type": "select", "options": ["Male", "Female"], "required": true}, {"name": "Nationality of deceased", "type": "select", "options": ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"], "required": true}, {"name": "Cause of death", "type": "select", "options": ["Accident", "Murder", "Sickness", "Suicide", "Natural Causes", "Unknown"], "required": true}, {"name": "Contact person phone number", "type": "phone"}, {"name": "Contact person name", "type": "text"}, {"name": "Give a brief narrative of what happened", "type": "narrative"}, {"name": "Time and date of occurrence", "type": "datetime", "format": "past", "required": true}]	2025-04-03 12:36:12.157	4
5	Homicide		f	f	[{"name": "Who is dead", "type": "select", "options": ["Adult", "Minor"], "required": true}, {"name": "Name of the deceased", "type": "text", "required": true}, {"name": "Gender of deceased", "type": "select", "options": ["Male", "Female"]}, {"name": "Nationality of deceased", "type": "select", "options": ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"], "required": true}, {"name": "Cause of death", "type": "select", "options": ["Accident", "Murder", "Sickness", "Suicide", "Natural Causes"], "required": true}, {"name": "Contact person phone number", "type": "phone"}, {"name": "Contact person name", "type": "text"}, {"name": "Give a brief narrative of what happened", "type": "narrative"}, {"name": "Time and date of occurrence", "type": "datetime", "format": "past", "required": true}]	2025-04-03 12:37:30.235	5
8	Rape		f	f	[{"name": "Who was raped", "type": "single-choice", "options": ["Minor", "Adult"], "required": true}, {"name": "Name", "type": "text", "required": true}, {"name": "Gender", "type": "select", "options": ["Male", "Female"], "required": true}, {"name": "Age", "type": "select", "options": ["0 - 5", "6 - 12", "13 - 17"], "required": true, "dependency": {"value": "Minor", "question": "Who was raped"}}, {"name": "Age", "type": "select", "options": ["18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65 and above"], "required": true, "dependency": {"value": "Adult", "question": "Who was raped"}}, {"name": "Nationality", "type": "select", "options": ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"], "required": true}, {"name": "Next of kin", "type": "text"}, {"name": "Next of kin phone number", "type": "phone"}, {"name": "Date and time of occurrence", "type": "datetime", "format": "past", "required": true}, {"name": "Give a brief narrative of what happened", "type": "narrative"}, {"name": "Do you have a suspect", "type": "single-choice", "options": ["Yes", "No"], "required": true}, {"name": "Name of the suspect", "type": "text", "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Relationship with the victim", "type": "select", "options": ["Spouse", "Parent", "Sibling", "Relative", "Colleague", "Friend", "Unknown"], "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Description of the suspect", "type": "text", "dependency": {"value": "Yes", "question": "Do you have a suspect"}}]	2025-04-03 12:40:40.62	8
1	Assault		f	f	[{"name": "Who was assaulted", "type": "select", "options": ["Adult", "Minor"], "required": true}, {"name": "Name of the victim", "tpye": "text", "required": true}, {"name": "Gender of the victim", "type": "select", "options": ["Male", "Female"], "required": true}, {"name": "Nationality of the victim", "type": "select", "options": ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"], "required": true}, {"name": "Do you have a suspect", "type": "single-choice", "options": ["Yes", "No"]}, {"name": "Name of the suspect", "type": "text", "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Relationship with the suspect", "type": "select", "options": ["Spouse", "Parent", "Sibling", "Relative", "Colleague", "Friend", "Stranger"], "required": true, "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Description of the suspect", "type": "text", "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Give a brief narrative of what happened", "tpye": "narrative"}, {"name": "date and time of occurrence", "type": "datetime", "format": "past", "required": true}]	2025-04-03 12:31:35.374	1
9	Robbery		f	f	[{"name": "What category of items were stolen", "type": "multi-select", "options": ["Electronics", "Documents", "Household Items", "Livestock", "Office Equipment", "Other"], "required": true}, {"name": "type of electronic", "type": "multi-select", "options": ["television", "laptop", "Fridge", "Other"], "required": true, "dependency": {"value": "Electronics", "question": "What category of items were stolen"}}, {"name": "Television serial number", "type": "text", "dependency": {"value": "television", "question": "type of electronic"}}, {"name": "television make", "type": "select", "options": ["SAMSUNG", "LG", "SONY", "VITRON", "Other"], "required": true, "dependency": {"value": "television", "question": "type of electronic"}}, {"name": "laptop make", "type": "select", "options": ["HP", "DELL", "MACBOOK"], "required": true, "dependency": {"value": "laptop", "question": "type of electronic"}}, {"name": "Laptop serial number", "type": "text", "dependency": {"value": "laptop", "question": "type of electronic"}}, {"name": "fridge make", "type": "select", "options": ["SAMSUNG", "WHIRLPOOL", "HAIER"], "required": true, "dependency": {"value": "Fridge", "question": "type of electronic"}}, {"name": "Fridge serial number", "type": "text", "dependency": {"value": "Fridge", "question": "type of electronic"}}, {"name": "list down", "type": "text", "dependency": {"value": "Other", "question": "type of electronic"}}, {"name": "serial number if any", "type": "text", "dependency": {"value": "Other", "question": "type of electronic"}}, {"name": "type of Documents", "type": "multi-select", "options": ["title deed", "identification card", "passport", "bank card", "driving license"], "required": true, "dependency": {"value": "Documents", "question": "What category of items were stolen"}}, {"name": "name on the document", "type": "text", "dependency": {"value": "Documents", "question": "What category of items were stolen"}}, {"name": "number on the document", "type": "text", "dependency": {"value": "Documents", "question": "What category of items were stolen"}}, {"name": "list of Household Items lost", "type": "text", "dependency": {"value": "Household Items", "question": "What category of items were stolen"}}, {"name": "brief description of the Household Items", "type": "text", "dependency": {"value": "Household Items", "question": "What category of items were stolen"}}, {"name": "Livestock", "type": "multi-select", "options": ["Domesticated Mammals", "Poultry (Birds)", "Aquatic Livestock (Fish & Shellfish)"], "dependency": {"value": "Livestock", "question": "What category of items were stolen"}}, {"name": "Other", "type": "text", "dependency": {"value": "Livestock", "question": "What category of items were stolen"}}, {"name": "List of Office Equipment lost", "type": "text", "dependency": {"value": "Office Equipment", "question": "What category of items were stolen"}}, {"name": "brief description of the Office Equipment", "type": "text", "dependency": {"value": "Office Equipment", "question": "What category of items were stolen"}}, {"name": "Name", "type": "text", "dependency": {"value": "Other", "question": "What category of items were stolen"}}, {"name": "Give a brief narrative of what happened", "type": "narrative"}, {"name": "Do you have a suspect", "type": "single-choice", "options": ["Yes", "No"], "required": true}, {"name": "Name of the suspect", "type": "text", "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Gender of the suspect", "type": "select", "options": ["Male", "Female"], "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Description of the suspect", "type": "text", "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Date and time of occurrence", "type": "datetime", "format": "past", "required": true}]	2025-04-03 12:41:37.887	9
6	Missing Person		f	f	[{"name": "Who is missing", "type": "single-choice", "options": ["Adult", "Minor"], "required": true}, {"name": "Name", "type": "text", "required": true}, {"name": "Gender", "type": "select", "options": ["Male", "Female"], "required": true}, {"name": "Age", "type": "select", "options": ["0 - 5", "6 - 12", "13 - 17"], "required": true, "dependency": {"value": "Minor", "question": "Who is missing"}}, {"name": "Age", "type": "select", "options": ["18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65 and above"], "required": true, "dependency": {"value": "Adult", "question": "Who is missing"}}, {"name": ".", "type": "grouped", "input_fields": [{"name": "Weight (kgs)", "type": "select", "options": ["Below 10", "10 - 20", "21 - 40", "41 - 60", "61 - 80", "81 - 100", "101 - 120", "Above 120"], "required": true}, {"name": "Height(feet)", "type": "select", "options": ["below 3'3", "3'3 - 4'3", "4'3 - 4'11", "4'11 - 5'5", "5'5 - 5'11", "5'11 - 6'5", "above - 6'5"], "required": true}]}, {"name": "Attach a photo", "type": "image"}, {"name": "A brief description of the person", "type": "narrative"}, {"name": "When last seen", "type": "datetime", "format": "past", "required": true}, {"name": "Mental Condition", "type": "select", "options": ["Normal", "Autistic", "Bipolar", "Depression", "PTSD", "Suicidal", "Schizophrenia", "Other"], "required": true}, {"name": "Language person speaks", "type": "checkbox", "options": ["Kiswahili", "English", "Kikuyu", "Kamba", "luhya", "luo", "kalenjin"], "required": true}, {"name": "Nationality of the missing person", "type": "select", "options": ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"], "required": true}, {"name": "Name of next of kin", "type": "text", "required": true}, {"name": "Next of kin mobile no", "type": "phone", "required": true}]	2025-04-03 12:38:35.004	6
10	Stolen Lost Item		f	f	[{"name": "What category of items were stolen", "type": "multi-select", "options": ["Electronics", "Documents", "Household Items", "Livestock", "Office Equipment", "Other"], "required": true}, {"name": "type of electronic", "type": "multi-select", "options": ["television", "laptop", "Fridge", "Other"], "required": true, "dependency": {"value": "Electronics", "question": "What category of items were stolen"}}, {"name": "Television serial number", "type": "text", "dependency": {"value": "television", "question": "type of electronic"}}, {"name": "television make", "type": "select", "options": ["SAMSUNG", "LG", "SONY", "VITRON", "Other"], "required": true, "dependency": {"value": "television", "question": "type of electronic"}}, {"name": "laptop make", "type": "select", "options": ["HP", "DELL", "MACBOOK"], "required": true, "dependency": {"value": "laptop", "question": "type of electronic"}}, {"name": "Laptop serial number", "type": "text", "dependency": {"value": "laptop", "question": "type of electronic"}}, {"name": "fridge make", "type": "select", "options": ["SAMSUNG", "WHIRLPOOL", "HAIER"], "required": true, "dependency": {"value": "Fridge", "question": "type of electronic"}}, {"name": "Fridge serial number", "type": "text", "dependency": {"value": "Fridge", "question": "type of electronic"}}, {"name": "list down", "type": "text", "required": true, "dependency": {"value": "Other", "question": "type of electronic"}}, {"name": "serial number if any", "type": "text", "dependency": {"value": "Other", "question": "type of electronic"}}, {"name": "type of Documents", "type": "multi-select", "options": ["title deed", "identification card", "passport", "bank card", "Licenses"], "required": true, "dependency": {"value": "Documents", "question": "What category of items were stolen"}}, {"name": "name on the document", "type": "text", "dependency": {"value": "Documents", "question": "What category of items were stolen"}}, {"name": "number on the document", "type": "text", "dependency": {"value": "Documents", "question": "What category of items were stolen"}}, {"name": "list of Household Items lost", "type": "multi-select", "options": ["Appliances", "Tableware", "Storage", "Cleaning Supplies", "Cookware Utensils"], "required": true, "dependency": {"value": "Household Items", "question": "What category of items were stolen"}}, {"name": "brief description of the Household Items", "type": "text", "dependency": {"value": "Household Items", "question": "What category of items were stolen"}}, {"name": "Livestock", "type": "multi-select", "options": ["Domesticated Mammals", "Poultry (Birds)", "Aquatic Livestock (Fish & Shellfish)"], "dependency": {"value": "Livestock", "question": "What category of items were stolen"}}, {"name": "Other", "type": "text", "dependency": {"value": "Livestock", "question": "What category of items were stolen"}}, {"name": "List of Office Equipment lost", "type": "multi-select", "options": ["Office Machines", "Communication Equipments", "Office Furniture", "Stationary and Supplies", "IT Equipment and Accessories", "Office Security Equipment", "Cleaning and Mantainance", "Office Decor"], "required": true, "dependency": {"value": "Office Equipment", "question": "What category of items were stolen"}}, {"name": "brief description of the Office Equipment", "type": "text", "dependency": {"value": "Office Equipment", "question": "What category of items were stolen"}}, {"name": "Name", "type": "text", "dependency": {"value": "Other", "question": "What category of items were stolen"}}, {"name": "Give a brief narrative of what happened", "type": "narrative"}, {"name": "Date and time of occurrence", "type": "datetime", "format": "past", "required": true}]	2025-04-03 12:42:47.265	10
7	Motor Vehicle Theft		f	f	[{"name": "Body type", "type": "select", "options": ["Saloon", "Sedan", "Sports car", "SUV", "Minivan", "Truck", "Jeep", "MPV"], "required": true}, {"name": "Registration number", "type": "text", "required": true}, {"name": "Make", "type": "select", "options": ["Ford", "Honda", "Toyota", "Volvo", "Mazda", "Mercedes", "Isuzu", "Chevrolet", "Lexus", "BMW", "Landrover", "Range Rover"], "required": true}, {"name": "Model", "type": "text", "required": true}, {"name": "Color", "type": "text", "required": true}, {"name": "Car description", "type": "text"}, {"name": "Date and time of occurrence", "type": "datetime", "format": "past", "required": true}, {"name": "Give a brief narrative of what happened", "type": "narrative"}]	2025-04-03 12:39:53.122	7
11	Arson		f	f	[{"name": "Give a brief narrative of what happened", "type": "narrative"}, {"name": "Type of property", "type": "select", "options": ["Commercial", "Residential", "School", "Hospital", "Factory"], "required": true}, {"name": "Plot No", "tpye": "text"}, {"name": "Are you the property owner", "type": "single-choice", "options": ["Yes", "No"], "required": true}, {"name": "Was the property occupied", "type": "single-choice", "options": ["Yes", "No"], "required": true, "dependency": {"value": "Yes", "question": "Are you the property owner"}}, {"name": "Number of people occupying", "type": "text", "dependency": {"value": "Yes", "question": "Was the property occupied"}}, {"name": "Name of the owner", "type": "text", "required": true, "dependency": {"value": "No", "question": "Are you the property owner"}}, {"name": "date and time of occurrence", "type": "datetime", "format": "past", "required": true}]	2025-04-03 12:43:34.766	11
3	Cyber Crime		f	f	[{"name": "Select Incident", "type": "select", "options": ["Child pornography", "Cyber bullying", "Computer fraud and forgery", "False publication", "Cyber harassment"], "required": true}, {"name": "Who is the victim", "type": "single-choice", "options": ["Minor", "Me"], "required": true}, {"name": "Relationship", "type": "select", "options": ["Parent", "Guardian", "Relative", "Sibling"], "required": true, "dependency": {"value": "Minor", "question": "Who is the victim"}}, {"name": "give a brief narrative of what happened", "type": "narrative"}, {"name": "Do you have a suspect", "type": "single-choice", "options": ["Yes", "No"]}, {"name": "Name of the suspect", "type": "text", "required": true, "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Give details about the suspect", "type": "text", "required": true, "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "When did this happen", "type": "datetime", "format": "past", "required": true}]	2025-04-03 12:33:13.302	3
2	Burglary		f	f	[{"name": "select type of property broken into", "type": "single-choice", "options": ["Commercial", "Residential", "Office", "Others"], "required": true}, {"name": "Property Name", "type": "tetx", "dependency": {"value": "Commercial", "question": "select type of property broken into"}}, {"name": "LR Number", "type": "tetx", "dependency": {"value": "Commercial", "question": "select type of property broken into"}}, {"name": "What category of items were stolen", "type": "multi-select", "options": ["Electronics", "Documents", "Household Items", "Livestock", "Office Equipment", "Other"], "dependency": {"value": "Commercial", "question": "select type of property broken into"}}, {"name": "Property Name", "type": "tetx", "dependency": {"value": "Residential", "question": "select type of property broken into"}}, {"name": "LR Number", "type": "tetx", "dependency": {"value": "Residential", "question": "select type of property broken into"}}, {"name": "What category of items were stolen", "type": "multi-select", "options": ["Electronics", "Documents", "Household Items", "Livestock", "Office Equipment", "Other"], "dependency": {"value": "Residential", "question": "select type of property broken into"}}, {"name": "Property Name", "type": "tetx", "dependency": {"value": "Office", "question": "select type of property broken into"}}, {"name": "Property Number", "type": "tetx", "dependency": {"value": "Office", "question": "select type of property broken into"}}, {"name": "What category of items were stolen", "type": "multi-select", "options": ["Documents", "Household Items", "Office Equipment", "Other"], "dependency": {"value": "Office", "question": "select type of property broken into"}}, {"name": "type of electronic", "type": "multi-select", "options": ["television", "laptop", "Fridge", "Other"], "dependency": {"value": "Electronics", "question": "What category of items were stolen"}}, {"name": "Television serial number", "type": "text", "dependency": {"value": "television", "question": "type of electronic"}}, {"name": "television make", "type": "multi-select", "options": ["SAMSUNG", "LG", "SONY", "VITRON", "Other"], "dependency": {"value": "television", "question": "type of electronic"}}, {"name": "laptop make", "type": "select", "options": ["HP", "DELL", "MACBOOK"], "dependency": {"value": "laptop", "question": "type of electronic"}}, {"name": "Laptop serial number", "type": "text", "dependency": {"value": "laptop", "question": "type of electronic"}}, {"name": "fridge make", "type": "select", "options": ["SAMSUNG", "WHIRLPOOL", "HAIER"], "dependency": {"value": "Fridge", "question": "type of electronic"}}, {"name": "Fridge serial number", "type": "text", "dependency": {"value": "Fridge", "question": "type of electronic"}}, {"name": "list down", "type": "text", "dependency": {"value": "Other", "question": "type of electronic"}}, {"name": "serial number if any", "type": "text", "dependency": {"value": "Other", "question": "type of electronic"}}, {"name": "type of Documents", "type": "multi-select", "options": ["title deed", "identification card", "passport", "bank card", "driving license"], "dependency": {"value": "Documents", "question": "What category of items were stolen"}}, {"name": "name on the document", "type": "text", "dependency": {"value": "Documents", "question": "What category of items were stolen"}}, {"name": "number on the document", "type": "text", "dependency": {"value": "Documents", "question": "What category of items were stolen"}}, {"name": "list of Household Items lost", "type": "multi-select", "options": ["Appliances", "Tableware", "Storage", "Cleaning Supplies", "Cookware Utensils"], "dependency": {"value": "Household Items", "question": "What category of items were stolen"}}, {"name": "brief description of the Household Items", "type": "text", "dependency": {"value": "Household Items", "question": "What category of items were stolen"}}, {"name": "Livestock", "type": "multi-select", "options": ["Domesticated Mammals", "Poultry (Birds)", "Aquatic Livestock (Fish & Shellfish)"], "dependency": {"value": "Livestock", "question": "What category of items were stolen"}}, {"name": "Other", "type": "text", "dependency": {"value": "Livestock", "question": "What category of items were stolen"}}, {"name": "List of Office Equipment lost", "type": "multi-select", "options": ["Office Machines", "Communication Equipments", "Office Furniture", "Stationary and Supplies", "IT Equipment and Accessories", "Office Security Equipment", "Cleaning and Mantainance", "Office Decor"], "dependency": {"value": "Office Equipment", "question": "What category of items were stolen"}}, {"name": "brief description of the Office Equipment", "type": "text", "dependency": {"value": "Office Equipment", "question": "What category of items were stolen"}}, {"name": "Name", "type": "text", "dependency": {"value": "Other", "question": "What category of items were stolen"}}, {"name": "Give a brief narrative of what happened", "type": "narrative"}, {"name": "Date and time of occurrence", "type": "date"}]	2025-04-03 12:32:43.456	2
12	GBV		f	f	[{"name": "Type of GBV", "type": "single-choice", "options": ["Sexual Violence", "Physical Violence", "Pyschological or Emotional Violence", "Economic or Financial Violence", "Harmful Traditional Practices", "Digital or Online Violence"], "required": true}, {"name": "Sexual Violence", "type": "select", "options": ["Rape", "Attempted Rape", "Defilement", "Forced Prostitution", "Female Genital Mutilation", "Incest"], "required": true, "dependency": {"value": "Sexual Violence", "question": "Type of GBV"}}, {"name": "Physical Violence", "type": "select", "options": ["Burning", "Chocking or Struggling", "Kicking", "Hitting", "Throwing objects", "Use of Weapon", "Hair pulling", "Biting"], "required": true, "dependency": {"value": "Physical Violence", "question": "Type of GBV"}}, {"name": "Pyschological or Emotional Violence", "type": "select", "options": ["Verbal Abuse", "Gas Lighting", "Threats", "Stalking"], "required": true, "dependency": {"value": "Pyschological or Emotional Violence", "question": "Type of GBV"}}, {"name": "Economic or Financial Violence", "type": "select", "options": ["Property Grabbing", "Restrivtion from Employment", "Denial of Financial Support", "Forced Debt"], "required": true, "dependency": {"value": "Economic or Financial Violence", "question": "Type of GBV"}}, {"name": "Harmful Traditional Practices", "type": "select", "options": ["Widow Cleansing", "Forced Marriage", "Children Marriage", "Forced Body scaring"], "required": true, "dependency": {"value": "Harmful Traditional Practices", "question": "Type of GBV"}}, {"name": "Digital or Online Violence", "type": "select", "options": ["Deep Fake Abuse", "Catfishing", "Cyber Stalking", "Online Harrasment", "Trolling", "Sextortion"], "required": true, "dependency": {"value": "Digital or Online Violence", "question": "Type of GBV"}}, {"name": "Platform In Digital or Online Violence", "type": "select", "options": ["Twitter", "Tiktok", "Facebook", "Instagram", "Thread", "Telegram"], "required": true, "dependency": {"value": "Digital or Online Violence", "question": "Type of GBV"}}, {"name": "Accompany any link if any", "type": "text", "dependency": {"value": "Digital or Online Violence", "question": "Type of GBV"}}, {"name": "Name of the casualty", "type": "text", "required": true}, {"name": "Age", "type": "single-choice", "options": ["Adult", "Minor"], "required": true}, {"name": "Gender", "type": "select", "options": ["Male", "Female"], "required": true}, {"name": "Minor", "type": "select", "options": ["0 - 5", "6 - 12", "13 - 17"], "required": true, "dependency": {"value": "Minor", "question": "Age"}}, {"name": "Adult", "type": "select", "options": ["18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65 and above"], "required": true, "dependency": {"value": "Adult", "question": "Age"}}, {"name": "Nationality", "type": "select", "options": ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"], "required": true}, {"name": "Next of kin", "type": "text"}, {"name": "Next of kin phone number", "type": "phone"}, {"name": "Date and time of occurrence", "type": "datetime", "format": "past", "required": true}, {"name": "Give a brief narrative of what happened", "type": "narrative"}, {"name": "Do you have a suspect", "type": "single-choice", "options": ["Yes", "No"]}, {"name": "Name of the suspect", "type": "text", "required": true, "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Relationship with the casualty", "type": "select", "options": ["Spouse", "Parent", "Sibling", "Relative", "Colleague", "Friend", "Stranger"], "dependency": {"value": "Yes", "question": "Do you have a suspect"}}, {"name": "Description of the suspect", "type": "text", "dependency": {"value": "Yes", "question": "Do you have a suspect"}}]	2025-04-03 12:44:16.339	12
\.


--
-- Data for Name: sub_module_data; Type: TABLE DATA; Schema: public; Owner: microservices
--

COPY public.sub_module_data (id, "sub_moduleId", "submissionDate", attachments, "formData", "userId", status, sync_id, comment, location, pin, station_id, ob_number, email, id_no, phone_number, urgency, county, sub_county) FROM stdin;
3	11	2025-04-03 13:06:43.906	{}	{"Plot No": null, "Type of property": "Residential", "Name of the owner": "IE SOLUTIONS ", "Are you the property owner": "No", "date and time of occurrence": "2025-04-03 03:18", "Give a brief narrative of what happened": null}	6	Approved	3	Report validated and approved	47, Shanzu Rd	Lat: -1.2526199, long: 36.7824647	1	OB/012/1360/4/3/2025	michelcheboi23@gmail.com	36445676	721860391	High	\N	\N
4	7	2025-04-03 13:17:20.38	{}	{"Color": "Blue", "Model": "X3", "Body type": "SUV", "Car description": "Big Blue SUV", "Registration number": "KDG 666F", "Date and time of occurrence": "2025-04-02 23:58", "A brief narrative of what happened": "I left my house at around 0900 hrs to do some shopping and some full body massage at Sarit center.I took 3 hrs to get done and when I went out I realized my car was missing in the parking lot."}	7	Approved	4	Report validated and approved	47, Shanzu Rd	Lat: -1.2526099, long: 36.7824667	1	OB/012/1361/4/3/2025	otienoshikuku@gmail.com	32622498	706254126	Medium	\N	\N
5	7	2025-04-03 13:25:54.442	{}	{"Color": "Black", "Model": "E200", "Body type": "Sedan", "Car description": "New with a matte black wrap", "Registration number": "KGM 333M", "Date and time of occurrence": "2025-04-03 16:00", "A brief narrative of what happened": "After having my lunch at java I realised my car was missing, I had packed it at the Sarit carpark. Upon checking the area I noticed there were no signs of forced entry such as broken glass. I have confirmed that the vehicle was not towed or moved without my authorisation."}	6	Approved	5	Report validated and approved	Sarit Centre	Lat: -1.2613921, long: 36.8026507	1	OB/012/1362/4/3/2025	michelcheboi23@gmail.com	36445676	721860391	Medium	\N	\N
6	11	2025-04-03 13:32:52.579	{}	{"Plot No": "12", "Type of property": "Residential", "Was the property occupied": "Yes", "Are you the property owner": "Yes", "Number of people occupying": "16", "date and time of occurrence": "2025-01-21 12:00", "Give a brief narrative of what happened": "cooking gone bad"}	25	Approved	6	Report validated and approved	15, S Colonnade	Lat: 51.503799484932756, long: -0.015499440490696573	4	OB/069/1363/4/3/2025	nyamukarani@gmail.com	40049245	798077064	Low	\N	\N
8	6	2025-04-03 13:34:12.85	{}	{"Age": "18 - 24", "Name": "Sylvia Nasike", "Gender": "Female", "Height(feet)": "4'3 - 4'11", "Weight (kgs)": "41 - 60", "When last seen": "2025-04-02 23:00", "Who is missing": "Adult", "Mental Condition": "Suicidal", "Name of next of kin": "Julius Barasa", "Next of kin mobile no": "+254746311275", "Language person speaks": ["Kiswahili", "English"], "A brief description of the person": "She was last seen wearing blue trousers,black top and black jacket, she was wearing white sneakers and she had black braids "}	6	Approved	8	Report validated and approved	VRJ5+RHF	Lat: -0.1179317, long: 34.8089097	3	OB/177/1364/4/3/2025	michelcheboi23@gmail.com	36445676	721860391	High	\N	\N
7	1	2025-04-03 13:33:27.541	{}	{"Who was assaulted": "Adult", "Name of the victim": "Ann", "Gender of the victim": "Female", "Do you have a suspect": "No", "date and time of occurrence": "2025-04-03 15:30", "Give a brief narrative of what happened": "A man beat Ann badly despite our efforts trying to restrain him"}	7	Approved	7	Report validated and approved	47, Shanzu Rd	Lat: -1.2526083, long: 36.7824345	1	OB/012/1365/4/3/2025	otienoshikuku@gmail.com	32622498	706254126	High	\N	\N
11	11	2025-04-04 05:56:05.679	{}	{"Plot No": "30", "Type of property": "Commercial", "Name of the owner": "martin", "Are you the property owner": "No", "date and time of occurrence": "2025-04-03 12:00", "Give a brief narrative of what happened": "fire"}	3	Approved	11	Report validated and approved	47, Shanzu Rd	Lat: -1.2525268, long: 36.7826357	1	OB/012/1367/4/4/2025	haptartech@gmail.com	33641337	0702433995	High	\N	\N
9	4	2025-04-03 13:39:57.912	{}	{"Name": "vsjzikwbwbshz", "Who is dead": "Adult", "Cause of death": "Sickness", "Gender of deceased": "Female", "Contact person name": "vajiskzndnd", "Contact person phone number": "+254742816766", "Time and date of occurrence": "2025-04-03 12:00", "Give a brief narrative of what happened": "nsososijsbs"}	6	Approved	9	Report validated and approved	2953+RC	Lat: 0.0095649, long: 34.3535019	2	OB/233/1366/4/3/2025	michelcheboi23@gmail.com	36445676	721860391	Low	Kiambu	Kiambu
10	5	2025-04-03 13:49:30.888	{}	{"Who is dead": "Minor", "Cause of death": "Accident", "Gender of deceased": "Female", "Contact person name": "jssiosowjshxhxsh", "Name of the deceased": "jansnndkdxkndnd", "Contact person phone number": "+254763187576", "Time and date of occurrence": "2025-04-03 12:00", "Give a brief narrative of what happened": "wjisixidjsbsnxbdjx"}	6	Rejected	\N	Your report does not contain a narrative that makes sense	W6QV+8Q	Lat: -0.06163346323835246, long: 34.2444347217679	2	\N	michelcheboi23@gmail.com	36445676	721860391	N/A	Kiambu	Kiambu
13	3	2025-04-04 05:59:33.209	{}	{"Select Incident": "False publication", "Who is the victim": "Me", "Name of the suspect": "Neville Chamberlain", "When did this happen": "2024-04-03 14:00", "Do you have a suspect": "Yes", "Give details about the suspect": "Former PM UK", "give a brief narrative of what happened": "a false story about my ability to change shape and fly at will"}	15	Approved	13	Report validated and approved	PR38+JP8	Lat: -1.2963882, long: 36.8173246	1	OB/012/1368/4/4/2025	karaninyamu@gmail.com	11223541	722520566	Low	Nairobi	Ruaraka Sub County 
12	3	2025-04-04 05:59:33.121	{}	{"Select Incident": "False publication", "Who is the victim": "Me", "Name of the suspect": "Neville Chamberlain", "When did this happen": "2024-04-03 14:00", "Do you have a suspect": "Yes", "Give details about the suspect": "Former PM UK", "give a brief narrative of what happened": "a false story about my ability to change shape and fly at will"}	15	Approved	12	Report validated and approved	PR38+JP8	Lat: -1.2963882, long: 36.8173246	1	OB/012/1369/4/4/2025	karaninyamu@gmail.com	11223541	722520566	Low	Nairobi	Ruaraka Sub County 
14	4	2025-04-04 06:27:38.378	{}	{"Name": "Sylvia Chebet", "Who is dead": "Minor", "Cause of death": "Sickness", "Gender of deceased": "Female", "Contact person name": "Brian Kiptoo", "Contact person phone number": "+254721578686", "Time and date of occurrence": "2025-04-04 09:10", "Give a brief narrative of what happened": null}	6	Approved	14	Report validated and approved	47, Shanzu Rd	Lat: -1.2526215, long: 36.7824111	1	OB/012/1370/4/4/2025	michelcheboi23@gmail.com	36445676	721860391	High	Kiambu	Kiambu
15	11	2025-04-04 06:34:09.21	{}	{"Plot No": "7", "Type of property": "Commercial", "Name of the owner": "Jasmine Jane", "Are you the property owner": "No", "date and time of occurrence": "2025-04-03 12:00", "Give a brief narrative of what happened": "while doing shopping at the market,we heard an explotion ,a gas had explored which burnt down the whole shop."}	5	Approved	15	Report validated and approved	47, Shanzu Rd	Lat: -1.2524975, long: 36.782653	1	OB/012/1371/4/4/2025	amusifaith@gmail.com	35994553	707839700	High	\N	\N
16	10	2025-04-04 06:35:34.923	{}	{"laptop make": "DELL", "type of electronic": ["laptop"], "Laptop serial number": "DL556", "Date and time of occurrence": "2025-04-04 03:30", "What category of items were stolen": ["Electronics"], "Give a brief narrative of what happened": "My laptop got stolen at Spring Valley Supermarket"}	7	Approved	16	Report validated and approved	47, Shanzu Rd	Lat: -1.2526062, long: 36.7826005	1	OB/012/1372/4/4/2025	otienoshikuku@gmail.com	32622498	706254126	Medium	\N	\N
17	1	2025-04-04 06:41:36.005	{}	{"Who was assaulted": "Adult", "Name of the victim": "Kate Muthoni", "Gender of the victim": "Female", "Do you have a suspect": null, "date and time of occurrence": "2025-04-02 12:00", "Give a brief narrative of what happened": "While walking in the streets in Town,two men came to me,hit me  and snatched my bag . "}	5	Approved	17	Report validated and approved	47, Shanzu Rd	Lat: -1.2525243, long: 36.7826435	1	OB/012/1373/4/4/2025	amusifaith@gmail.com	35994553	707839700	High	\N	\N
18	2	2025-04-04 06:46:49.017	{}	{"LR Number": "78", "Property Name": "shanzu gardens", "Property Number": null, "television make": ["SAMSUNG"], "type of electronic": ["television"], "Television serial number": "8689347B", "Date and time of occurrence": "2025-04-02 12:00", "list of Household Items lost": null, "List of Office Equipment lost": ["Office Machines", "Communication Equipments"], "What category of items were stolen": ["Office Equipment", "Electronics"], "select type of property broken into": "Residential", "Give a brief narrative of what happened": "I came from a business trip, coming home I found my house had been broken into.", "brief description of the Household Items": null, "brief description of the Office Equipment": "Two landlines phones,one desktop "}	5	Approved	18	Report validated and approved	47, Shanzu Rd	Lat: -1.2524685, long: 36.7826614	1	OB/012/1374/4/4/2025	amusifaith@gmail.com	35994553	707839700	Medium	\N	\N
19	7	2025-04-04 06:49:59.572	{}	{"Color": "Black", "Model": "C200", "Body type": "Sedan", "Car description": "New with a black matte wrap", "Registration number": "KGM 333M", "Date and time of occurrence": "2025-04-04 09:00", "A brief narrative of what happened": "I left my car at the packing safely locked and went to the bank, when I came back I found it missing and there was no sign of forced entry such as broken glass"}	6	Approved	19	Report validated and approved	7427+R69	Lat: 1.2520325, long: 35.113105	4	OB/069/1375/4/4/2025	michelcheboi23@gmail.com	36445676	721860391	High	Kiambu	Kiambu
20	3	2025-04-04 06:51:42.308	{}	{"Select Incident": "Computer fraud and forgery", "Who is the victim": "Me", "When did this happen": "2025-04-02 11:00", "Do you have a suspect": "No", "give a brief narrative of what happened": "I tried to log in to my Instagram account only to find out that they was some one was using my account and I can no longer access it "}	5	Approved	20	Report validated and approved	47, Shanzu Rd	Lat: -1.2525417, long: 36.7826292	1	OB/012/1376/4/4/2025	amusifaith@gmail.com	35994553	707839700	Low	\N	\N
21	4	2025-04-04 07:03:40.861	{}	{"Name": "Jannie judy", "Who is dead": "Adult", "Cause of death": "Sickness", "Gender of deceased": "Female", "Contact person name": "Hellen Desau", "Contact person phone number": "+254725468534", "Time and date of occurrence": "2025-04-04 04:05", "Give a brief narrative of what happened": "My friend called me saying she wasn't My friend called me saying he was not feeling well.I went quickly with a taxi to see her whereabouts,I found her laying down helplessly convulsing,we took her quickly to the hospital unfortunately she died on the way"}	5	Approved	21	Report validated and approved	47, Shanzu Rd	Lat: -1.2525273, long: 36.7826347	1	OB/012/1377/4/4/2025	amusifaith@gmail.com	35994553	707839700	High	\N	\N
22	6	2025-04-04 07:44:45.646	{}	{"Age": "25 - 34", "Name": "Charles Kiprono", "Gender": "Male", "Height(feet)": "5'5 - 5'11", "Weight (kgs)": "61 - 80", "Attach a photo": null, "When last seen": "2025-04-03 23:00", "Who is missing": "Adult", "Mental Condition": "Depression", "Name of next of kin": "Janet Chebet ", "Next of kin mobile no": "+254763157275", "Language person speaks": ["Kiswahili", "English"], "A brief description of the person": null}	6	Approved	22	Report validated and approved	VRJ5+RHF	Lat: -0.1179317, long: 34.8089097	3	OB/177/1378/4/4/2025	michelcheboi23@gmail.com	36445676	721860391	Medium	Kiambu	Kiambu
23	12	2025-04-04 08:10:36.522	{}	{"Name": " Samin Mohammed ", "Gender": "Female", "Next of kin": "Abdalaah Shunu", "Type of GBV": "Harmful Traditional Practices", "Physical Violence": null, "Do you have a suspect": "No", "Next of kin phone number": "+254758631287", "Date and time of occurrence": "2025-04-03 15:00", "Harmful Traditional Practices": "Children Marriage", "Give a brief narrative of what happened": "a seventeen year old girl was forced to marriage and on denying she was murdered and burnt "}	5	Approved	23	Report validated and approved	47, Shanzu Rd	Lat: -1.2522299, long: 36.7825722	2	OB/233/1379/4/4/2025	amusifaith@gmail.com	35994553	707839700	High	\N	\N
24	4	2025-04-04 17:43:17.136	{}	{"Name": "Goe", "Who is dead": "Adult", "Cause of death": "Unknown", "Gender of deceased": "Male", "Contact person name": "Soe", "Contact person phone number": "+254711111111", "Time and date of occurrence": "2025-04-04 17:55", "Give a brief narrative of what happened": "We found this guy dead by the road side"}	7	Approved	24	Report validated and approved	49, Parklands Rd	Lat: -1.2683794, long: 36.812734	1	OB/012/1380/4/4/2025	otienoshikuku@gmail.com	32622498	706254126	High	\N	\N
60	9	2025-04-22 09:30:39.347	{}	{"laptop make": "MACBOOK", "type of electronic": ["laptop"], "Name of the suspect": "Gerald ", "Laptop serial number": "cccc", "Do you have a suspect": "Yes", "Gender of the suspect": "Male", "Description of the suspect": "shirt red and short", "Date and time of occurrence": "2025-04-22 02:21", "What category of items were stolen": ["Electronics"], "Give a brief narrative of what happened": "xxxxxx"}	25	Approved	60	Report validated and approved	15, Churchill Pl	Lat: 51.50400356768404, long: -0.015435905344555191	4	OB/069/1447/4/22/2025	nyamukarani@gmail.com	40049245	798077064	Medium	\N	\N
62	7	2025-04-22 11:24:03.672	{}	{"Color": "Orange", "Model": "Mustang'", "Body type": "Sports car", "Car description": "An orange big mascullar sedan car", "Registration number": "KDJ 555G", "Date and time of occurrence": "2025-04-21 23:58", "Give a brief narrative of what happened": "came out from the shop and it was gone"}	7	Approved	62	Report validated and approved	Sarit Centre	Lat: -1.2611605, long: 36.80197769999999	1	OB/012/1450/4/22/2025	otienoshikuku@gmail.com	32622498	706254126	Medium	Homa Bay	Karachwonyo
25	4	2025-04-07 06:41:53.822	{}	{"Name": "Frank Kisese", "Who is dead": "Adult", "Cause of death": "Unknown", "Gender of deceased": "Male", "Contact person name": "Magdalene Waweru ", "Contact person phone number": "+254725437694", "Time and date of occurrence": "2025-04-07 04:00", "Give a brief narrative of what happened": "On Monday at around 4am Frank was found unresponsive in his house. Emergency services were contacted immediately and upon arrival medics confirmed the individual was deceased. The cause of death is currently unknown."}	6	Approved	25	Report validated and approved	PQXP+237	Lat: -1.2524883, long: 36.78545329999999	1	OB/012/1381/4/7/2025	michelcheboi23@gmail.com	36445676	721860391	High	Kiambu	Kiambu
26	1	2025-04-07 06:44:06.769	{}	{"Who was assaulted": "Adult", "Name of the victim": "Peter Macharia", "Gender of the victim": "Male", "Do you have a suspect": "No", "date and time of occurrence": "2025-04-06 23:00", "Give a brief narrative of what happened": "bsnskzisijensbdnzjzjzjz"}	6	Rejected	\N	Your report does not contain a narrative that makes sense	22, Brookside Dr	Lat: -1.2561635, long: 36.79194040000001	1	\N	michelcheboi23@gmail.com	36445676	721860391	N/A	Kiambu	Kiambu
27	11	2025-04-08 06:56:46.915	{}	{"Plot No": "456-f", "Type of property": "Residential", "Name of the owner": "D&G ltd", "Are you the property owner": "No", "date and time of occurrence": "2025-04-08 03:30", "Give a brief narrative of what happened": null}	7	Approved	27	Report validated and approved	47, Shanzu Rd	Lat: -1.2526225, long: 36.7824851	1	OB/012/1390/4/8/2025	otienoshikuku@gmail.com	32622498	706254126	High	\N	\N
28	1	2025-04-08 07:13:48.83	{}	{"Who was assaulted": "Adult", "Name of the victim": "Max Kiberenge", "Gender of the victim": "Male", "Do you have a suspect": "No", "date and time of occurrence": "2025-04-08 04:00", "Give a brief narrative of what happened": "bakskisjxbsnwjs"}	6	Rejected	\N	Your report does not contain a narrative that makes sense	47, Shanzu Rd	Lat: -1.2525866, long: 36.7824462	1	\N	michelcheboi23@gmail.com	36445676	721860391	N/A	Kiambu	Kiambu
29	3	2025-04-08 07:26:20.5	{}	{"Relationship": "Guardian", "Select Incident": "Child pornography", "Who is the victim": "Minor", "Name of the suspect": "Gladys Maraga", "When did this happen": "2025-04-07 04:00", "Do you have a suspect": "Yes", "Give details about the suspect": "My House assistant.A tall dark,huge lady", "give a brief narrative of what happened": "I realized that my house assistant usually watch pornography videos at around 1600 hrs .This has been  happening for a while now since I have been watching on the CCTV camera."}	5	Approved	29	Report validated and approved	Google Building 43	Lat: 37.4219983, long: -122.084	2	OB/233/1391/4/8/2025	amusifaith@gmail.com	35994553	707839700	Medium	\N	\N
30	5	2025-04-08 08:03:11.223	{}	{"Who is dead": "Adult", "Cause of death": "Accident", "Gender of deceased": "Male", "Contact person name": "Patrick Asilwa", "Name of the deceased": "John Kawi", "Contact person phone number": "+254707865236", "Time and date of occurrence": "2025-04-08 09:30", "Give a brief narrative of what happened": "While walking besides the road ,a car and a lorry were over speeding and in a twinkle,they collided ..John died in the spot"}	5	Approved	30	Report validated and approved	47, Shanzu Rd	Lat: -1.2526221, long: 36.7824032	3	OB/177/1392/4/8/2025	amusifaith@gmail.com	35994553	707839700	High	\N	\N
31	11	2025-04-08 09:03:39.037	{}	{"Plot No": null, "Type of property": "Residential", "Was the property occupied": "No", "Are you the property owner": "Yes", "date and time of occurrence": "2025-04-08 12:00", "Give a brief narrative of what happened": "fire"}	1	Approved	31	Report validated and approved	Kinsasha Rd	Lat: -1.2739646, long: 36.8324717	1	OB/012/1404/4/8/2025	9davidmuia@gmail.com	35029142	796217595	High	Kericho	Bureti
32	1	2025-04-08 11:39:34.646	{}	{"Who was assaulted": "Adult", "Name of the victim": "Tarus Kiprono", "Gender of the victim": "Male", "Do you have a suspect": "No", "date and time of occurrence": "2025-04-08 04:00", "Give a brief narrative of what happened": null}	6	Approved	32	Report validated and approved	Sarit Centre	Lat: -1.2611605, long: 36.80197769999999	1	OB/012/1408/4/8/2025	michelcheboi23@gmail.com	36445676	721860391	High	Kiambu	Kiambu
33	1	2025-04-08 11:52:10.889	{}	{"Who was assaulted": "Adult", "Name of the victim": "Jillian Mugega", "Gender of the victim": "Female", "Do you have a suspect": "No", "date and time of occurrence": "2025-04-08 04:12", "Give a brief narrative of what happened": "my cow got stolen and I was going to look for it I met my friend and we started talking and went to her place "}	6	Approved	33	Report validated and approved	22, Brookside Dr	Lat: -1.2561635, long: 36.79194040000001	1	OB/012/1409/4/8/2025	michelcheboi23@gmail.com	36445676	721860391	Low	Kiambu	Kiambu
34	7	2025-04-08 12:20:20.681	{}	{"Color": "Black ", "Model": "XC60 ", "Body type": "Sedan", "Car description": "New", "Registration number": "KGM 333M", "Date and time of occurrence": "2025-04-08 15:00", "A brief narrative of what happened": "stolen at sarit"}	6	Approved	34	Report validated and approved	Sarit Centre	Lat: -1.2613921, long: 36.8026507	1	OB/012/1410/4/8/2025	michelcheboi23@gmail.com	36445676	721860391	Medium	Kiambu	Kiambu
35	5	2025-04-08 12:21:45.626	{}	{"Who is dead": "Adult", "Cause of death": "Sickness", "Gender of deceased": "Male", "Contact person name": "Mercy Achieng", "Name of the deceased": "Sospeter Ragemo", "Contact person phone number": "+254765444585", "Time and date of occurrence": "2025-04-08 14:00", "Give a brief narrative of what happened": null}	6	Approved	35	Report validated and approved	VRJ7+C4H	Lat: -0.1189354, long: 34.8128595	3	OB/177/1411/4/8/2025	michelcheboi23@gmail.com	36445676	721860391	High	Kiambu	Kiambu
36	11	2025-04-08 13:34:29.172	{}	{"Plot No": "1234", "Type of property": "Residential", "Name of the owner": "Kimani", "Are you the property owner": "No", "date and time of occurrence": "2025-04-07 12:00", "Give a brief narrative of what happened": "propertsetbon fire"}	8	Approved	36	Report validated and approved	JQ5C+85	Lat: -1.3916987, long: 36.7704295	1	OB/012/1412/4/8/2025	phylis.gathoni@intelligentso.com	22015136	728716539	High	Kajiado	Kajiado North.
37	4	2025-04-09 06:47:29.08	{}	{"Name": "Brian Kiptoo ", "Who is dead": "Minor", "Cause of death": "Accident", "Gender of deceased": "Male", "Contact person name": "Mercy Cherono", "Contact person phone number": "+254754289665", "Time and date of occurrence": "2025-04-09 09:16", "Give a brief narrative of what happened": null}	6	Approved	37	Report validated and approved	The Pearl	Lat: 1.2481932, long: 35.1103736	4	OB/069/1413/4/9/2025	michelcheboi23@gmail.com	36445676	721860391	Medium	Kiambu	Kiambu
61	7	2025-04-22 10:04:15.03	{}	{"Color": "black n blue", "Model": "i8", "Body type": "Sports car", "Car description": null, "Registration number": "cxxx", "Date and time of occurrence": "2025-04-22 12:00", "A brief narrative of what happened": "came back from shop and it was gone"}	25	Approved	61	Report validated and approved	The Master Shipwright's House | The Shipwright	Lat: 51.486740358027326, long: -0.02543035137511973	4	OB/069/1448/4/22/2025	nyamukarani@gmail.com	40049245	798077064	Medium	\N	\N
38	12	2025-04-09 06:51:27.518	{}	{"Age": "Adult", "Adult": "18 - 24", "Gender": "Female", "Next of kin": "Teresa Bosibori", "Type of GBV": "Physical Violence", "Sexual Violence": "Rape", "Physical Violence": "Chocking or Struggling", "Name of the suspect": "Eugene Mutua", "Name of the casualty": "Alice Kemunto", "Do you have a suspect": "Yes", "Next of kin phone number": "+254707839500", "Description of the suspect": "a tall dark first year student.", "Date and time of occurrence": "2025-04-07 15:00", "Relationship with the casualty": "Colleague", "Give a brief narrative of what happened": "A first year student was found dead in a tank at 2.00 p.m after a long search.Autopsy was taken and it was declared that it was due to strangulation "}	5	Approved	38	Report validated and approved	47, Shanzu Rd	Lat: -1.252542, long: 36.782636	1	OB/012/1414/4/9/2025	amusifaith@gmail.com	35994553	707839700	High	\N	\N
39	11	2025-04-09 07:01:44.119	{}	{"Plot No": "f h", "Type of property": "School", "Name of the owner": "shy", "Was the property occupied": "No", "Are you the property owner": "Yes", "date and time of occurrence": "2025-04-02 12:00", "Give a brief narrative of what happened": "ch"}	25	Approved	39	Report validated and approved	Chiromo Ln	Lat: -1.2675001, long: 36.812022	4	OB/069/1415/4/9/2025	nyamukarani@gmail.com	40049245	798077064	High	\N	\N
40	1	2025-04-09 07:07:12.838	{}	{"Who was assaulted": "Adult", "Name of the victim": "Naomi Naomi", "Gender of the victim": "Female", "Do you have a suspect": "No", "date and time of occurrence": "2025-04-08 12:00", "Give a brief narrative of what happened": "She was attacked on her way home"}	8	Approved	40	Report validated and approved	85, Kyuna Cres	Lat: -1.2485304949450449, long: 36.78306173533201	1	OB/012/1416/4/9/2025	phylis.gathoni@intelligentso.com	22015136	728716539	Medium	Kajiado	Kajiado North.
41	6	2025-04-09 12:33:17.677	{}	{"Age": "6 - 12", "Name": "Kabado Junior ", "Gender": "Male", "Height(feet)": "4'3 - 4'11", "Weight (kgs)": "21 - 40", "Attach a photo": null, "When last seen": "2025-04-08 23:00", "Who is missing": "Minor", "Mental Condition": "Normal", "Name of next of kin": "Kabado Snr", "Next of kin mobile no": "+254764845548", "Language person speaks": ["Kiswahili", "English"], "A brief description of the person": "was wearing black trousers and blue t-shirt "}	6	Approved	41	Report validated and approved	Sarit Centre	Lat: -1.2611605, long: 36.80197769999999	1	OB/012/1417/4/9/2025	michelcheboi23@gmail.com	36445676	721860391	Medium	Kiambu	Kiambu
42	11	2025-04-09 12:44:34.076	{}	{"Plot No": null, "Type of property": "Residential", "Was the property occupied": "Yes", "Are you the property owner": "Yes", "Number of people occupying": "8", "date and time of occurrence": "2025-04-09 12:00", "Give a brief narrative of what happened": "Fire started from the kitchen and spread to the rest of the house "}	6	Approved	42	Report validated and approved	47, Shanzu Rd	Lat: -1.2526215, long: 36.7824879	1	OB/012/1418/4/9/2025	michelcheboi23@gmail.com	36445676	721860391	High	Kiambu	Kiambu
43	6	2025-04-10 12:33:19.804	{}	{"Age": "25 - 34", "Name": "Cleopatra Kimani", "Gender": "Female", "Height(feet)": "4'11 - 5'5", "Weight (kgs)": "41 - 60", "Attach a photo": null, "When last seen": "2025-04-09 20:00", "Who is missing": "Adult", "Mental Condition": "Normal", "Name of next of kin": "Paul Kimani", "Next of kin mobile no": "+254766588488", "Language person speaks": ["Kiswahili", "English"], "A brief description of the person": null}	6	Approved	43	Report validated and approved	Sarit Centre	Lat: -1.2611605, long: 36.80197769999999	1	OB/012/1424/4/10/2025	michelcheboi23@gmail.com	36445676	721860391	Medium	Kiambu	Kiambu
44	7	2025-04-10 13:14:35.855	{}	{"Color": "Black", "Model": "E250", "Body type": "Sedan", "Car description": "Has a black matte wrap ", "Registration number": "KGM 333M", "Date and time of occurrence": "2025-04-10 15:00", "A brief narrative of what happened": "stolen from where I had parked at sarit as I was doing some errands in the bank"}	6	Approved	44	Report validated and approved	Sarit Centre	Lat: -1.2613921, long: 36.8026507	1	OB/012/1425/4/10/2025	michelcheboi23@gmail.com	36445676	721860391	Medium	Kiambu	Kiambu
45	6	2025-04-11 08:45:31.775	{}	{"Age": "25 - 34", "Name": "Richard Osei", "Gender": "Male", "Height(feet)": "4'11 - 5'5", "Weight (kgs)": "41 - 60", "Attach a photo": null, "When last seen": "2025-04-10 18:00", "Who is missing": "Adult", "Mental Condition": "Normal", "Name of next of kin": "Paul Osei", "Next of kin mobile no": "+254728464667", "Language person speaks": ["Kiswahili", "English"], "A brief description of the person": null}	6	Approved	45	Report validated and approved	VRJ7+C4H	Lat: -0.1189354, long: 34.8128595	3	OB/177/1426/4/11/2025	michelcheboi23@gmail.com	36445676	721860391	Medium	Kiambu	Kiambu
46	7	2025-04-13 20:23:10.182	{}	{"Color": "yellow", "Model": "saloon ", "Body type": "Jeep", "Car description": "Karina Saloon", "Registration number": "KBD006F", "Date and time of occurrence": "2025-04-11 17:00", "A brief narrative of what happened": "I was at Sarit center shopping when I left my car parked to find that it was stolen"}	5	Approved	46	Report validated and approved	PPJW+4J3	Lat: -1.2696684, long: 36.74664419999999	1	OB/012/1427/4/13/2025	amusifaith@gmail.com	35994553	707839700	Medium	\N	\N
47	10	2025-04-14 11:10:59.166	{}	{"Date and time of occurrence": "10/04/2025", "What category of items were stolen": "laptop bag with laptop on it ", "Give a brief narrative of what happened": "I was heading home from town when I left my laptop bag in the vehicle KBC 2456K a PSV"}	5	Approved	47	Successfully Approved	47, Shanzu Rd	Lat: -1.2526055, long: 36.7824619	2	OB/233/1449/4/22/2025	amusifaith@gmail.com	35994553	707839700	Low	\N	\N
48	8	2025-04-14 11:20:35.449	{}	{"Age": "6 - 12", "Name": "Jumma Haida", "Gender": "Female", "Nationality": "Kenya", "Next of kin": "Haseeb Handi", "Who was raped": "Minor", "Do you have a suspect": "No", "Next of kin phone number": "0723566543", "Date and time of occurrence": "08/04/2025", "Give a brief narrative of what happened": "Jumma was raped while heading home after coming from church choir practice at around 3.00 p.m .."}	5	Approved	48	Successfully Approved	47, Shanzu Rd	Lat: -1.252613, long: 36.7824766	1	OB/012/1451/4/23/2025	amusifaith@gmail.com	35994553	707839700	Low	\N	\N
49	10	2025-04-15 07:20:28.871	{}	{"Other": null, "Livestock": null, "television make": "SAMSUNG", "type of Documents": ["identification card", "title deed", "Licenses"], "type of electronic": ["television"], "name on the document": "National Identity Card,NCBA bank card,KCB bank card,Driving Licence", "number on the document": "4", "Television serial number": "777796437B", "Date and time of occurrence": "2025-04-15 13:00", "list of Household Items lost": null, "What category of items were stolen": ["Documents", "Electronics"], "Give a brief narrative of what happened": "I went to my house just after dropping my visitor off approximately 30 minutes or so.I came back only to realize that my Tv had been stolen and some documents were stolen too.", "brief description of the Household Items": null}	5	Approved	49	Report validated and approved	47, Shanzu Rd	Lat: -1.2524481, long: 36.782531	1	OB/012/1428/4/15/2025	amusifaith@gmail.com	35994553	707839700	Low	\N	\N
50	12	2025-04-15 07:31:39.775	{}	{"Age": "Minor", "Minor": "13 - 17", "Gender": "Female", "Next of kin": "Gilan  Desare", "Type of GBV": "Harmful Traditional Practices", "Physical Violence": "Burning", "Name of the casualty": "Azeezah Mohammed ", "Do you have a suspect": "No", "Next of kin phone number": "+254725631258", "Date and time of occurrence": "2025-04-14 15:00", "Harmful Traditional Practices": "Children Marriage", "Economic or Financial Violence": null, "Give a brief narrative of what happened": "A 15 years old girl was beaten up by her parents after refusing to get married to an old man"}	5	Approved	50	Report validated and approved	47, Shanzu Rd	Lat: -1.2526206, long: 36.782443	1	OB/012/1429/4/15/2025	amusifaith@gmail.com	35994553	707839700	High	\N	\N
51	11	2025-04-16 07:28:15.229	{}	{"Plot No": "567-k", "Type of property": "Residential", "Name of the owner": "DFT llc.", "Are you the property owner": "No", "date and time of occurrence": "2025-04-16 12:00", "Give a brief narrative of what happened": null}	7	Approved	51	Report validated and approved	47, Shanzu Rd	Lat: -1.2529667, long: 36.7828217	1	OB/012/1432/4/16/2025	otienoshikuku@gmail.com	32622498	706254126	High	Homa Bay	Karachwonyo
52	4	2025-04-16 07:34:16.11	{}	{"Name": "jannelle Jason", "Who is dead": "Adult", "Cause of death": "Sickness", "Gender of deceased": "Female", "Contact person name": "Hellen Awour ", "Contact person phone number": "+254725364582", "Time and date of occurrence": "2025-04-16 11:00", "Give a brief narrative of what happened": "I came from work only to find out my sick aunt  dead"}	5	Approved	52	Report validated and approved	Google Building 43	Lat: 37.4219983, long: -122.084	1	OB/012/1433/4/16/2025	amusifaith@gmail.com	35994553	707839700	Medium	\N	\N
55	10	2025-04-20 08:45:38.665	{}	{"fridge make": null, "laptop make": null, "television make": "VITRON", "type of electronic": ["television"], "Fridge serial number": null, "Laptop serial number": null, "Television serial number": null, "Date and time of occurrence": "2025-03-19 22:00", "What category of items were stolen": ["Electronics"], "Give a brief narrative of what happened": ""}	3	Approved	55	Report validated and approved	QP36+279	Lat: -1.2469202, long: 36.7105634	1	OB/012/1441/4/22/2025	haptartech@gmail.com	33641337	702433995	Low	Nairobi	Westlands Sub County 
54	3	2025-04-18 08:14:38.796	{}	{"Select Incident": "Computer fraud and forgery", "Who is the victim": "Me", "Name of the suspect": "khal", "When did this happen": "2025-04-18 12:00", "Do you have a suspect": "No", "Give details about the suspect": "criminal", "give a brief narrative of what happened": "someone gained access to my laptop"}	3	Approved	54	Report validated and approved	QP36+279	Lat: -1.2469645, long: 36.7105565	4	OB/069/1442/4/22/2025	haptartech@gmail.com	33641337	702433995	Low	Nairobi	Westlands Sub County 
56	3	2025-04-22 07:52:51.803	{}	{"Select Incident": "Cyber bullying", "Who is the victim": "Me", "When did this happen": "2025-04-22 12:00", "Do you have a suspect": "No", "give a brief narrative of what happened": null}	2	Approved	56	Report validated and approved	47, Shanzu Rd	Lat: -1.2526321, long: 36.782395	2	OB/233/1443/4/22/2025	mkyenze17@gmail.com	34535631	797275002	Low	Makueni	Kibwezi east
53	5	2025-04-16 07:34:22.773	{}	{"Who is dead": "Adult", "Cause of death": "Accident", "Gender of deceased": "Male", "Contact person name": "Sarah Wafula", "Name of the deceased": "Justus Mutua", "Contact person phone number": "+254731673494", "Time and date of occurrence": "2025-04-16 10:00", "Give a brief narrative of what happened": "He was knocked down by a car at the kyuna roundabout, he lost a lot of blood and died on the spot"}	6	Approved	53	approved successfully	PQXP+C9P	Lat: -1.2514162, long: 36.7859454	1	OB/012/1440/4/17/2025	michelcheboi23@gmail.com	36445676	721860391	High	Kiambu	Kiambu
57	7	2025-04-22 07:58:46.878	{}	{"Color": "Crimson red", "Model": "CX 5", "Body type": "SUV", "Car description": "New", "Registration number": "KGM 333M", "Date and time of occurrence": "2025-04-22 10:00", "A brief narrative of what happened": "was stolen at sarit while I was having my breakfast,left it in the parking securely locked but when I came back it was not there and there were no signs of forced entry like broken glass"}	6	Approved	57	Report validated and approved	Sarit Centre	Lat: -1.2613921, long: 36.8026507	1	OB/012/1444/4/22/2025	michelcheboi23@gmail.com	36445676	721860391	Medium	Kiambu	Kiambu
58	7	2025-04-22 08:17:59.256	{}	{"Color": "sleek silver", "Model": "Corolla ", "Body type": "Saloon", "Car description": "A sleek silver sedan,featuring a 1.8 L petrol engine,automatic transmission and a comfortable black fabric interior.", "Registration number": "KDC 143J", "Date and time of occurrence": "2025-04-22 10:00", "A brief narrative of what happened": "Had gone to shop when I left my car at the parking lot.After about one hour or so I was done only to realize that my car was missing "}	5	Approved	58	Report validated and approved	47, Shanzu Rd	Lat: -1.2526328, long: 36.7823876	1	OB/012/1445/4/22/2025	amusifaith@gmail.com	35994553	707839700	Medium	\N	\N
59	11	2025-04-22 08:40:38.515	{}	{"Plot No": null, "Type of property": "Residential", "Was the property occupied": "Yes", "Are you the property owner": "Yes", "Number of people occupying": "23", "date and time of occurrence": "2025-04-22 11:27", "Give a brief narrative of what happened": null}	6	Approved	59	Report validated and approved	47, Shanzu Rd	Lat: -1.2526361, long: 36.7824712	1	OB/012/1446/4/22/2025	michelcheboi23@gmail.com	36445676	721860391	High	Kiambu	Kiambu
\.


--
-- Name: Action_id_seq; Type: SEQUENCE SET; Schema: public; Owner: microservices
--

SELECT pg_catalog.setval('public."Action_id_seq"', 69, true);


--
-- Name: IPRS_Person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: microservices
--

SELECT pg_catalog.setval('public."IPRS_Person_id_seq"', 9, true);


--
-- Name: ModuleData_id_seq; Type: SEQUENCE SET; Schema: public; Owner: microservices
--

SELECT pg_catalog.setval('public."ModuleData_id_seq"', 1, false);


--
-- Name: Modules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: microservices
--

SELECT pg_catalog.setval('public."Modules_id_seq"', 12, true);


--
-- Name: contact_center_id_seq; Type: SEQUENCE SET; Schema: public; Owner: microservices
--

SELECT pg_catalog.setval('public.contact_center_id_seq', 1, false);


--
-- Name: sub_module_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: microservices
--

SELECT pg_catalog.setval('public.sub_module_data_id_seq', 62, true);


--
-- Name: sub_module_id_seq; Type: SEQUENCE SET; Schema: public; Owner: microservices
--

SELECT pg_catalog.setval('public.sub_module_id_seq', 12, true);


--
-- Name: Action Action_pkey; Type: CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."Action"
    ADD CONSTRAINT "Action_pkey" PRIMARY KEY (id);


--
-- Name: IPRS_Person IPRS_Person_pkey; Type: CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."IPRS_Person"
    ADD CONSTRAINT "IPRS_Person_pkey" PRIMARY KEY (id);


--
-- Name: ModuleData ModuleData_pkey; Type: CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."ModuleData"
    ADD CONSTRAINT "ModuleData_pkey" PRIMARY KEY (id);


--
-- Name: Modules Modules_pkey; Type: CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."Modules"
    ADD CONSTRAINT "Modules_pkey" PRIMARY KEY (id);


--
-- Name: _prisma_migrations _prisma_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public._prisma_migrations
    ADD CONSTRAINT _prisma_migrations_pkey PRIMARY KEY (id);


--
-- Name: contact_center contact_center_pkey; Type: CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public.contact_center
    ADD CONSTRAINT contact_center_pkey PRIMARY KEY (id);


--
-- Name: sub_module_data sub_module_data_pkey; Type: CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public.sub_module_data
    ADD CONSTRAINT sub_module_data_pkey PRIMARY KEY (id);


--
-- Name: sub_module sub_module_pkey; Type: CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public.sub_module
    ADD CONSTRAINT sub_module_pkey PRIMARY KEY (id);


--
-- Name: IPRS_Person_id_no_key; Type: INDEX; Schema: public; Owner: microservices
--

CREATE UNIQUE INDEX "IPRS_Person_id_no_key" ON public."IPRS_Person" USING btree (id_no);


--
-- Name: Action Action_sub_module_dataId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."Action"
    ADD CONSTRAINT "Action_sub_module_dataId_fkey" FOREIGN KEY ("sub_module_dataId") REFERENCES public.sub_module_data(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: ModuleData ModuleData_moduleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public."ModuleData"
    ADD CONSTRAINT "ModuleData_moduleId_fkey" FOREIGN KEY ("moduleId") REFERENCES public."Modules"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: contact_center contact_center_sub_module_dataId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public.contact_center
    ADD CONSTRAINT "contact_center_sub_module_dataId_fkey" FOREIGN KEY ("sub_module_dataId") REFERENCES public.sub_module_data(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sub_module_data sub_module_data_sub_moduleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public.sub_module_data
    ADD CONSTRAINT "sub_module_data_sub_moduleId_fkey" FOREIGN KEY ("sub_moduleId") REFERENCES public.sub_module(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: sub_module sub_module_modulesId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: microservices
--

ALTER TABLE ONLY public.sub_module
    ADD CONSTRAINT "sub_module_modulesId_fkey" FOREIGN KEY ("modulesId") REFERENCES public."Modules"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

