--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: short_link; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.short_link (
    id integer NOT NULL,
    link character varying(2048),
    hash character varying(8)
);


ALTER TABLE public.short_link OWNER TO postgres;

--
-- Name: short_link_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.short_link_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.short_link_id_seq OWNER TO postgres;

--
-- Name: short_link_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.short_link_id_seq OWNED BY public.short_link.id;


--
-- Name: short_link id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.short_link ALTER COLUMN id SET DEFAULT nextval('public.short_link_id_seq'::regclass);


--
-- Name: short_link short_link_hash_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.short_link
    ADD CONSTRAINT short_link_hash_key UNIQUE (hash);


--
-- Name: short_link short_link_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.short_link
    ADD CONSTRAINT short_link_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

